"""Shared helpers for the re-engagement loop scripts.

Inputs are CSV exports of the member sheet's tabs, one file per tab, in a
folder (default: ./data). File names are the tab names in lower case with
spaces replaced by underscores: members.csv, status_history.csv, drafts.csv,
touchpoints.csv, conversions.csv, run_log.csv.
"""

from __future__ import annotations

import csv
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

TRUTHY = {"yes", "y", "true", "1", "x"}


def load_rules(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_tab(folder: str | Path, name: str) -> list[dict]:
    path = Path(folder) / f"{name}.csv"
    if not path.exists():
        return []
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = dict(r)
            # Also expose each column under a normalized name ("Last contact" -> "last_contact"),
            # so owners can keep their own headers ("Date", "Member") alongside the skill's.
            for k, v in r.items():
                if k:
                    row.setdefault(re.sub(r"[^a-z0-9]+", "_", k.strip().lower()).strip("_"), v)
            rows.append(row)
    return rows


def load_members(folder: str | Path, rules: dict) -> dict[str, dict]:
    """Members keyed by member_id, with the owner's column names mapped to the skill's."""
    mapping = rules.get("columns") or {}
    out = {}
    for row in read_tab(folder, "members"):
        m = {}
        for key, col in mapping.items():
            m[key] = (row.get(col) or "").strip() if col else ""
        for key in ("member_id", "name"):
            if not m.get(key):
                m[key] = (row.get(key) or "").strip()
        if m.get("member_id"):
            out[m["member_id"]] = m
    return out


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value[:19] if "T" in value else value, fmt).date()
        except ValueError:
            continue
    return None


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in TRUTHY


def in_holdout(member_id: str, digits: list[int]) -> bool:
    nums = re.findall(r"\d", member_id or "")
    return bool(nums) and int(nums[-1]) in set(digits)


def stage_rank(stage: str, stages: list[str]) -> int | None:
    lookup = {s.strip().lower(): i for i, s in enumerate(stages)}
    return lookup.get((stage or "").strip().lower())


def stage_on(history: list[dict], member_id: str, day: date) -> str | None:
    """The member's stage on the latest history row on or before `day`."""
    best, best_day = None, None
    for row in history:
        if row.get("member_id") != member_id:
            continue
        d = parse_date(row.get("date"))
        if d and d <= day and (best_day is None or d > best_day):
            best, best_day = row.get("stage"), d
    return best


def days_between(a: date, b: date) -> int:
    return (b - a).days


def today_or(value: str | None) -> date:
    return parse_date(value) if value else date.today()


__all__ = [
    "load_rules", "read_tab", "load_members", "parse_date", "truthy", "in_holdout",
    "stage_rank", "stage_on", "days_between", "today_or", "timedelta",
]
