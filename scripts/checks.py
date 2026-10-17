"""Deterministic checks on the day's drafts (step 2, run by Claude).

Flags: not_in_sheet, opted_out, skip, holdout, cap, over_daily_limit, no_reason.
Drafts with none of these get `ok` (Claude then adds judgment flags by reading them).

Usage:
    python scripts/checks.py --rules rules.yaml --data data --date 2026-10-18 [--out data/checks_new.csv]
"""

from __future__ import annotations

import argparse
import csv
import sys

from common import (days_between, in_holdout, load_members, load_rules, parse_date,
                    read_tab, today_or, truthy)

FIELDS = ["date", "draft_id", "member_id", "flag", "reason"]


def run(rules: dict, data: str, day) -> list[dict]:
    members = load_members(data, rules)
    drafts = [d for d in read_tab(data, "drafts")
              if parse_date(d.get("date")) == day and d.get("status") not in ("Held back", "Skipped")]
    touch = read_tab(data, "touchpoints")
    pick = rules.get("pick", {})
    measure = rules.get("measure", {})
    gap = int(pick.get("min_days_between_contacts", 14))
    max_run = int(pick.get("max_per_run", 5))
    skip_words = [w.lower() for w in pick.get("skip_if_notes_contain", [])]
    digits = measure.get("holdout_digits", [0, 5])

    rows = []
    for i, d in enumerate(drafts):
        mid = (d.get("member_id") or "").strip()
        flags = []
        m = members.get(mid)
        if not m:
            flags.append(("not_in_sheet", f"{mid or 'blank id'} is not in Members"))
        else:
            if truthy(m.get("opted_out")):
                flags.append(("opted_out", "member opted out"))
            notes = (m.get("notes") or "").lower()
            if truthy(m.get("skip")) or any(w in notes for w in skip_words):
                flags.append(("skip", "marked skip or excluded by notes rule"))
            last = parse_date(m.get("last_contacted"))
            if last and days_between(last, day) < gap:
                flags.append(("cap", f"contacted {days_between(last, day)} days ago; minimum is {gap}"))
        if in_holdout(mid, digits):
            flags.append(("holdout", "member is in the hold-back group"))
        for t in touch:
            if t.get("member_id") == mid and (t.get("direction") or "out") == "out":
                td = parse_date(t.get("date"))
                if td and 0 <= days_between(td, day) < gap and not any(f[0] == "cap" for f in flags):
                    flags.append(("cap", f"message sent {days_between(td, day)} days ago; minimum is {gap}"))
        if i >= max_run:
            flags.append(("over_daily_limit", f"draft {i + 1} of {len(drafts)}; limit is {max_run}"))
        if not (d.get("rule") or "").strip() or not (d.get("reason") or "").strip():
            flags.append(("no_reason", "no rule or reason recorded for this pick"))
        if not flags:
            flags.append(("ok", "passed rule checks; read the draft for tone and assumptions"))
        for flag, reason in flags:
            rows.append({"date": day.isoformat(), "draft_id": d.get("draft_id", ""),
                         "member_id": mid, "flag": flag, "reason": reason})
    return rows


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rules", default="rules.yaml")
    p.add_argument("--data", default="data")
    p.add_argument("--date")
    p.add_argument("--out")
    a = p.parse_args(argv)
    rows = run(load_rules(a.rules), a.data, today_or(a.date))
    out = open(a.out, "w", newline="", encoding="utf-8") if a.out else sys.stdout
    w = csv.DictWriter(out, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)
    if a.out:
        out.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
