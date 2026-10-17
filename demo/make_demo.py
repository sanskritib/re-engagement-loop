"""Generate a fictional demo community so the loop can be tried safely.

Everything here is made up: the community, the names, the dates, the money.
It simulates three weeks of the loop so the scorecard has something to show,
and today's drafts include two that should be flagged (one contacted too
recently, one in the hold-back group).

Usage:
    python demo/make_demo.py --date 2026-10-18
Writes demo/data/*.csv and demo/rules.yaml.
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
FIRST = ["Ava", "Ben", "Cara", "Dev", "Eli", "Fay", "Gus", "Hana", "Ivo", "Jun", "Kai", "Lena",
         "Milo", "Nia", "Omar", "Pia", "Quin", "Rae", "Sol", "Tess", "Uma", "Vik", "Wren", "Xia",
         "Yusuf", "Zoe", "Ari", "Bo", "Cy", "Dana", "Ezra", "Fern", "Gia", "Hugo", "Iris", "Jude",
         "Kit", "Lio", "Mae", "Ned"]
LAST = ["Okafor", "Lindqvist", "Moreau", "Tanaka", "Reyes", "Novak", "Haddad", "Brennan", "Sato",
        "Kowalski", "Mensah", "Ivers", "Duarte", "Falk", "Gill", "Hart", "Ito", "Juarez", "Kerr", "Lund"]
GOALS = ["finish a first draft of my book", "run a half marathon", "launch my consulting offer",
         "post on LinkedIn weekly", "get to 10 paying clients", "ship my side project",
         "read 20 books this year", "hire my first assistant", "", ""]
STAGES = ["Red", "Yellow", "Green"]
PRICES = [1000, 1500, 2000, 3000]


def write(path: Path, fields: list[str], rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--seed", type=int, default=7)
    a = p.parse_args(argv)
    today = date.fromisoformat(a.date)
    rnd = random.Random(a.seed)
    start = today - timedelta(days=21)
    data = HERE / "data"

    members = []
    for i in range(60):
        mid = f"M-{i + 1:04d}"
        joined = today - timedelta(days=rnd.randint(60, 600))
        members.append({
            "member_id": mid,
            "name": f"{FIRST[i % len(FIRST)]} {LAST[(i * 7 + i // 40) % len(LAST)]}",
            "channel": "skool",
            "contact": "",
            "profile_link": f"https://www.skool.com/northstar-demo/@{FIRST[i % len(FIRST)].lower()}-{i + 1}",
            "joined": joined.isoformat(),
            "last_active": "",
            "stage": "",
            "renewal_date": (joined + timedelta(days=365 * ((today - joined).days // 365 + 1))).isoformat(),
            "plan_value": rnd.choice(PRICES),
            "last_contacted": "",
            "opted_out": "yes" if i == 12 else "",
            "skip": "",
            "goal": rnd.choice(GOALS),
            "notes": "Moderator" if i == 3 else "",
        })
    # A row for a teammate testing the loop in a test community. Fill in the real profile link.
    members.append({**members[0], "member_id": "M-0061", "name": "Test Member (teammate)",
                     "profile_link": "<test community profile link>", "goal": "test the loop end to end",
                     "plan_value": 0, "opted_out": "", "notes": "tester", "joined": (today - timedelta(days=90)).isoformat()})

    # Simulate 21 days: stages drift, Fo contacts some quiet members, holds back others.
    stage = {m["member_id"]: rnd.choices(STAGES, weights=[5, 2, 3])[0] for m in members}
    stage["M-0061"] = "Red"
    history, drafts, touch, conv, runlog = [], [], [], [], []
    contacted, held, last_contact = {}, {}, {}
    for n in range(22):
        day = start + timedelta(days=n)
        for mid, s in stage.items():
            history.append({"date": day.isoformat(), "member_id": mid, "stage": s})
        if day == today:
            break
        quiet = [mid for mid, s in stage.items() if s == "Red" and mid not in held
                 and (mid not in last_contact or (day - last_contact[mid]).days >= 14)
                 and mid != "M-0061" and mid not in ("M-0004", "M-0013")]
        rnd.shuffle(quiet)
        picks = 0
        for k, mid in enumerate(quiet):
            if mid[-1] in "05":
                held[mid] = day
                drafts.append({"draft_id": f"D-{day.isoformat()}-H{k}", "date": day.isoformat(), "member_id": mid,
                               "name": "", "rule": "quiet_14d", "reason": "quiet; held back for comparison",
                               "status": "Held back", "final_text": "", "approved_at": "", "sent_at": ""})
                continue
            if picks >= 2:
                continue
            picks += 1
            contacted.setdefault(mid, day)
            last_contact[mid] = day
            did = f"D-{day.isoformat()}-{picks:02d}"
            drafts.append({"draft_id": did, "date": day.isoformat(), "member_id": mid, "name": "",
                           "rule": "quiet_14d", "reason": "no activity for 14+ days", "status": "Sent",
                           "final_text": "(simulated)", "approved_at": day.isoformat(), "sent_at": day.isoformat()})
            touch.append({"date": day.isoformat(), "member_id": mid, "channel": "skool", "direction": "out",
                          "draft_id": did, "summary": "check-in (simulated)", "replied": "", "reply_date": ""})
        runlog.append({"timestamp": f"{day.isoformat()}T08:20:00", "step": "review", "agent": "fo", "status": "ok",
                       "drafts": picks, "checked": picks, "sent": picks,
                       "note": f"review_minutes={rnd.choice([6, 7, 8, 9, 11])} (simulated)"})
        # Movement: contacted members move up more often than held-back ones (simulated assumption).
        for mid in list(stage):
            p_up = 0.035 if mid in contacted else (0.012 if mid in held else 0.01)
            if stage[mid] != "Red" and mid not in contacted and rnd.random() < 0.05:
                stage[mid] = STAGES[STAGES.index(stage[mid]) - 1]
                continue
            if stage[mid] != "Green" and rnd.random() < p_up:
                stage[mid] = STAGES[STAGES.index(stage[mid]) + 1]
                if stage[mid] == "Green" and rnd.random() < 0.6:
                    value = next(m["plan_value"] for m in members if m["member_id"] == mid)
                    conv.append({"date": day.isoformat(), "member_id": mid, "type": "renewal", "value": value})

    # Fill current-state columns on Members.
    for m in members:
        mid = m["member_id"]
        m["stage"] = stage[mid]
        m["last_active"] = (today - timedelta(days=rnd.randint(15, 60) if stage[mid] == "Red"
                                              else rnd.randint(0, 13))).isoformat()
        if mid in contacted:
            m["last_contacted"] = last_contact[mid].isoformat()
    next(m for m in members if m["member_id"] == "M-0061")["last_active"] = (today - timedelta(days=20)).isoformat()

    # Today's drafts, before the check: the tester, two real picks, and two that must be flagged.
    def red_quiet(mid):
        return stage[mid] == "Red" and mid not in held and mid != "M-0061" \
            and (mid not in last_contact or (today - last_contact[mid]).days >= 14) \
            and mid not in ("M-0004", "M-0013")
    picks_today = [mid for mid in stage if red_quiet(mid) and mid[-1] not in "05"][:2]
    holdout_case = next((mid for mid in stage if mid[-1] in "05" and mid != "M-0061"), None)
    cap_case = sorted(last_contact, key=lambda k: last_contact[k])[-1]
    five_days_ago = (today - timedelta(days=5)).isoformat()
    touch.append({"date": five_days_ago, "member_id": cap_case, "channel": "skool", "direction": "out",
                  "draft_id": "", "summary": "follow-up (simulated)", "replied": "", "reply_date": ""})
    next(m for m in members if m["member_id"] == cap_case)["last_contacted"] = five_days_ago
    today_ids = ["M-0061"] + picks_today + [cap_case] + ([holdout_case] if holdout_case else [])
    for k, mid in enumerate(today_ids, start=1):
        drafts.append({"draft_id": f"D-{today.isoformat()}-{k:02d}", "date": today.isoformat(), "member_id": mid,
                       "name": next(m["name"] for m in members if m["member_id"] == mid), "rule": "quiet_14d",
                       "reason": "no activity for 14+ days", "status": "Drafted", "final_text": "",
                       "approved_at": "", "sent_at": ""})

    write(data / "members.csv", list(members[0].keys()), members)
    write(data / "status_history.csv", ["date", "member_id", "stage"], history)
    write(data / "drafts.csv", ["draft_id", "date", "member_id", "name", "rule", "reason", "status",
                                "final_text", "approved_at", "sent_at"], drafts)
    write(data / "touchpoints.csv", ["date", "member_id", "channel", "direction", "draft_id", "summary",
                                     "replied", "reply_date"], touch)
    write(data / "conversions.csv", ["date", "member_id", "type", "value"], conv)
    write(data / "run_log.csv", ["timestamp", "step", "agent", "status", "drafts", "checked", "sent", "note"], runlog)

    rules = yaml.safe_load(open(HERE.parent / "rules.example.yaml", encoding="utf-8"))
    rules["columns"] = {k: k for k in rules["columns"]}
    rules["pick"]["skip_if_notes_contain"] = ["Moderator"]
    with open(HERE / "rules.yaml", "w", encoding="utf-8") as f:
        f.write("# Demo rules, generated by make_demo.py from rules.example.yaml. Fictional.\n")
        yaml.safe_dump(rules, f, sort_keys=False, allow_unicode=True)
    print(f"Wrote demo data for {today} to {data}")


if __name__ == "__main__":
    main()
