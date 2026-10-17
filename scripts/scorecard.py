"""The daily scorecard (step 2, run by Claude).

Reads the exported tabs and rules.yaml and prints one Scorecard row plus a
two-sentence summary for the top of the outreach doc and the morning call.

Usage:
    python scripts/scorecard.py --rules rules.yaml --data data --date 2026-10-18 [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys

from common import (days_between, load_rules, parse_date, read_tab, stage_on, stage_rank,
                    timedelta, today_or)

FIELDS = ["date", "review_minutes", "baseline_minutes", "drafts", "approved", "sent",
          "contacted_moved_up", "contacted_total", "holdout_moved_up", "holdout_total",
          "revenue_attributed", "revenue_target", "note"]


def first_dates(rows, key="member_id", date_key="date", keep=lambda r: True):
    out = {}
    for r in rows:
        if not keep(r):
            continue
        d = parse_date(r.get(date_key))
        mid = r.get(key)
        if d and mid and (mid not in out or d < out[mid]):
            out[mid] = d
    return out


def moved_up(cohort, history, stages, day, window):
    """How many members in a cohort moved up a stage within `window` days of their start date.

    A member is counted once they have moved up, or once their window has passed without moving."""
    moved = total = 0
    for mid, start in cohort.items():
        if start > day:
            continue
        before = stage_rank(stage_on(history, mid, start) or "", stages)
        now = stage_rank(stage_on(history, mid, min(day, start + timedelta(days=window))) or "", stages)
        if before is None or now is None:
            continue
        if now > before:
            moved += 1
            total += 1
        elif days_between(start, day) >= window:
            total += 1
    return moved, total


def revenue(cohort, conversions, day, window):
    total = 0.0
    converted = 0
    for mid, start in cohort.items():
        got = 0.0
        for c in conversions:
            if c.get("member_id") != mid:
                continue
            d = parse_date(c.get("date"))
            if d and start <= d <= min(day, start + timedelta(days=window)):
                try:
                    got += float(str(c.get("value") or 0).replace("$", "").replace(",", ""))
                except ValueError:
                    pass
        if got:
            converted += 1
        total += got
    return total, converted


def run(rules: dict, data: str, day) -> dict:
    measure = rules.get("measure", {})
    stages = measure.get("stages", [])
    window = int(measure.get("moved_up_window_days", 14))
    attr = int(measure.get("attribution_days", 30))

    history = read_tab(data, "status_history")
    drafts = read_tab(data, "drafts")
    touch = read_tab(data, "touchpoints")
    conv = read_tab(data, "conversions")
    runlog = read_tab(data, "run_log")

    today_drafts = [d for d in drafts if parse_date(d.get("date")) == day and d.get("status") != "Held back"]
    yday = day - timedelta(days=1)
    yday_drafts = [d for d in drafts if parse_date(d.get("date")) == yday and d.get("status") != "Held back"]
    approved = sum(1 for d in yday_drafts if d.get("status") in ("Approved", "Sent"))
    sent = sum(1 for d in yday_drafts if d.get("status") == "Sent")

    review_minutes = ""
    for r in runlog:
        ts = parse_date(r.get("timestamp"))
        if r.get("step") == "review" and ts == yday:
            m = re.search(r"review_minutes=(\d+(?:\.\d+)?)", r.get("note") or "")
            if m:
                review_minutes = m.group(1)

    contacted = first_dates(touch, keep=lambda r: (r.get("direction") or "out") == "out")
    held = first_dates(drafts, keep=lambda r: r.get("status") == "Held back")

    c_up, c_total = moved_up(contacted, history, stages, day, window)
    h_up, h_total = moved_up(held, history, stages, day, window)

    c_rev, _ = revenue(contacted, conv, day, attr)
    h_rev, _ = revenue(held, conv, day, attr)
    baseline_rev = (h_rev / len(held)) * len(contacted) if held else 0.0
    attributed = max(0.0, c_rev - baseline_rev)

    notes = []
    if len(held) < 5:
        notes.append("fewer than 5 members held back so far; comparison is not reliable yet")
    if not review_minutes:
        notes.append("no review time logged for yesterday")

    row = {
        "date": day.isoformat(),
        "review_minutes": review_minutes,
        "baseline_minutes": measure.get("baseline_minutes", ""),
        "drafts": len(today_drafts),
        "approved": approved,
        "sent": sent,
        "contacted_moved_up": c_up,
        "contacted_total": c_total,
        "holdout_moved_up": h_up,
        "holdout_total": h_total,
        "revenue_attributed": round(attributed, 2),
        "revenue_target": measure.get("revenue_target", ""),
        "note": "; ".join(notes),
    }
    row["summary"] = summary(row)
    return row


def pct(a, b):
    return f"{round(100 * a / b)}%" if b else "n/a"


def summary(r: dict) -> str:
    parts = []
    if r["review_minutes"]:
        parts.append(f"Yesterday's review took {r['review_minutes']} minutes, against {r['baseline_minutes']} by hand.")
    parts.append(f"{r['sent']} messages went out yesterday and there are {r['drafts']} drafts today.")
    parts.append(
        f"Of contacted members, {r['contacted_moved_up']} of {r['contacted_total']} moved up a stage "
        f"({pct(r['contacted_moved_up'], r['contacted_total'])}); of members held back, "
        f"{r['holdout_moved_up']} of {r['holdout_total']} ({pct(r['holdout_moved_up'], r['holdout_total'])})."
    )
    target = r["revenue_target"]
    target_txt = f" of the ${int(float(target)):,} target" if target not in ("", None) else ""
    parts.append(f"Revenue attributed to outreach so far: ${r['revenue_attributed']:,.0f}{target_txt}.")
    if r["note"]:
        parts.append(f"Note: {r['note']}.")
    return " ".join(parts)


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rules", default="rules.yaml")
    p.add_argument("--data", default="data")
    p.add_argument("--date")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    row = run(load_rules(a.rules), a.data, today_or(a.date))
    if a.json:
        print(json.dumps(row, indent=2))
        return 0
    w = csv.DictWriter(sys.stdout, fieldnames=FIELDS, extrasaction="ignore")
    w.writeheader()
    w.writerow(row)
    print()
    print(row["summary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
