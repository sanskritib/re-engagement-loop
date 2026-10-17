---
name: re-engagement-loop
description: Run a daily re-engagement loop for a community or audience. Fo finds members going quiet, drafts a personal note for each, reviews the drafts with the owner on a morning call, and sends only what the owner approves. Claude checks every draft and keeps the scorecard. Use when an owner wants quiet members followed up on without doing it by hand.
version: 0.1.0
---

# Re-engagement loop

Three steps run on their own schedules and pass work to each other through two shared files: the **member sheet** (a Google Sheet) and the **outreach doc** (a Google Doc). The agents never call each other directly. If a step does not run, the next step notices and says so.

| Step | Default time | Who | Reads | Writes |
| --- | --- | --- | --- | --- |
| 1. Draft | 02:00 | Fo | Members, Touchpoints, rules, Editor's Notes | Outreach doc, Drafts tab, Status history tab, Run log |
| 2. Check | 05:00 | Claude | Outreach doc, Drafts, Members, Touchpoints, Status history, rules | Checks tab, Scorecard tab, flags in the doc, Run log |
| 3. Review and send | 08:00 (owner's time) | Fo | Outreach doc, Checks, Scorecard | Outreach doc, Drafts, Touchpoints, Run log |

Times are in the owner's time zone and come from `rules.yaml`.

Read the section for your role only. **If you are Fo, follow "Fo". If you are Claude, follow "Claude (checker)".** Both follow "Rules for everyone".

---

## Rules for everyone

These cannot be switched off in `rules.yaml`.

1. **Nothing is sent without the owner's explicit approval** of that specific message. Approval happens on the call or in writing in the outreach doc. A summary email or text is never approval.
2. **Only contact people in the member sheet**, through the channel listed for them, and never more often than `pick.min_days_between_contacts`.
3. **Skip anyone who has opted out, is in the hold-back group, or is marked `skip`.**
4. **Separate what you saw from what you assume.** "Last active 21 days ago" is seen. "Probably busy with work" is an assumption and must be labeled as one. Missing data means unknown, not inactive.
5. **No guilt, pressure, fake urgency or invented offers.** The owner's tone settings apply on top of this.
6. **Never post publicly** in the community. Direct messages only.
7. **Never change `rules.yaml`.** Propose changes to the owner; the owner edits the file.
8. **Log every run** to the Run log tab, including runs that did nothing or failed.
9. **Do not put member data anywhere other than the owner's own sheet and doc.**

---

## Shared files

### Member sheet tabs

Column names are configurable in `rules.yaml` under `columns`. Defaults:

**Members** (owner's data, kept current by the owner's existing sync)
`member_id, name, channel, contact, profile_link, joined, last_active, stage, renewal_date, plan_value, last_contacted, opted_out, skip, goal, notes`

**Status history** (one row per member per day, written by Fo in step 1)
`date, member_id, stage`

**Drafts** (one row per draft, the machine-readable ledger)
`draft_id, date, member_id, name, rule, reason, status, final_text, approved_at, sent_at`
Status moves: `Drafted → Checked → Approved → Sent`, or `→ Skipped`. A member in the hold-back group who matched a rule gets a row with status `Held back` and no draft; that row is the comparison group's start date.

**Touchpoints** (one row per message sent or received)
`date, member_id, channel, direction, draft_id, summary, replied, reply_date`

**Conversions** (renewals and upgrades, kept by the owner's sync or by hand)
`date, member_id, type, value`
`type` is `renewal`, `upgrade` or `new`. `value` is the money it brought in.

**Checks** (written by Claude)
`date, draft_id, member_id, flag, reason`
Flags: `ok, cap, over_daily_limit, opted_out, holdout, skip, unknown_data, assumption_unlabeled, tone, pressure, no_reason, not_in_sheet`

**Scorecard** (written by Claude, one row per day)
`date, review_minutes, baseline_minutes, drafts, approved, sent, contacted_moved_up, contacted_total, holdout_moved_up, holdout_total, revenue_attributed, revenue_target, note`

**Run log** (written by everyone)
`timestamp, step, agent, status, drafts, checked, sent, note`
`status` is `ok`, `nothing_to_do`, `skipped_missing_input` or `failed`.

### Outreach doc layout

```
# Outreach — <date>

## Scorecard
<one paragraph from the Scorecard tab, written by Claude>

## Since yesterday
<what changed: replies, stage moves, anything sent>

## Drafts
### D-<date>-<nn> · <name>
- Status: Drafted
- Seen: <facts from the sheet, with dates>
- Assumed: <labeled assumptions, or "none">
- Rule: <which rule picked them>
- Why now: <one line>
- Draft:
  > <message>
- Claude flags: <filled in by Claude in step 2>
- Owner notes: <filled in on the call>

## Editor's Notes
<standing feedback from the owner; Fo reads this before every draft run>
```

### Hold-back group

To measure honestly, some quiet members are deliberately not contacted. A member is in the hold-back group when the last digit of the number in their `member_id` is in `measure.holdout_digits` (default `0` and `5`, about 20%). This rule is fixed so Fo can apply it without code and Claude can check it.

---

## Fo

### Step 1: Draft (night)

1. Read `rules.yaml`, the Members, Touchpoints and Drafts tabs, and the Editor's Notes section of the outreach doc.
2. Append today's stage for every member to Status history.
3. Pick members who match `pick.rules` and are not excluded by "Rules for everyone" 2 and 3. Pick at most `pick.max_per_run`, highest priority first (`pick.priority`). For each member who matched a rule but is in the hold-back group, add a Drafts row with status `Held back`, the rule, and no draft, unless they already have one in the last `measure.attribution_days`.
4. For each pick, write a block in the outreach doc (layout above) and a Drafts row with status `Drafted`. The draft:
   - is written for this person from what the sheet says about them;
   - follows `tone` and everything in Editor's Notes;
   - is signed as the owner;
   - stays under `tone.max_words`.
5. Update "Since yesterday".
6. Write one Run log row. If nothing matched, log `nothing_to_do` and leave the doc saying so.

### Step 3: Review and send (morning)

1. Read the outreach doc, Drafts, Checks and Scorecard.
2. If no Checks rows exist for today's drafts, tell the owner at the start of the call: "Claude's check didn't run today." Continue.
3. Call the owner at `owner.call_time` on `owner.phone`.
4. On the call:
   - Open with the scorecard in two sentences.
   - Go through each draft: who, why now, what you wrote, and any Claude flag.
   - Apply the owner's changes to the doc while you talk, and say what you changed.
   - Ask for a clear decision on each draft: approve, change, or skip.
   - If the owner gives standing feedback ("never mention price"), add it to Editor's Notes.
   - If the owner asks for a rule change, note it under Owner notes. Do not edit `rules.yaml`.
5. If the owner does not answer after `owner.call_retries` attempts, email and text a short summary to `owner.email` and `owner.phone`. Send nothing to members that day.
6. For each approved draft: send it through the member's channel adapter (see `adapters/`), set Drafts status `Sent` with `sent_at` and `final_text`, add a Touchpoints row, and update `last_contacted`.
7. If an adapter cannot send, set status `Approved`, give the owner the text and profile link to send by hand, and log it.
8. Record replies you see in Touchpoints (`direction: in`).
9. Write one Run log row with how long the call took in `note` (`review_minutes=<n>`).

---

## Claude (checker)

You do not write or rewrite messages, contact members, place calls, or edit `rules.yaml`. You check and you count.

### Step 2: Check (between Fo's two steps)

1. Read `rules.yaml`, the outreach doc, and the Drafts, Members, Touchpoints, Status history and Conversions tabs.
2. If there are no Drafts rows for today, write a Run log row `nothing_to_do` and stop.
3. Run the deterministic checks: `python scripts/checks.py` with the exported tabs. It flags `cap`, `opted_out`, `holdout`, `skip`, `not_in_sheet` and `no_reason`.
4. Then read each draft yourself and add judgment flags:
   - `assumption_unlabeled`: the draft or "Seen" line states a guess as fact.
   - `unknown_data`: the pick relies on a blank or missing column.
   - `tone`: breaks `tone` or Editor's Notes.
   - `pressure`: guilt, fake urgency, or an offer not in `rules.yaml`.
   If a draft is fine, write `ok`.
5. Write every flag to the Checks tab, and copy it into the draft's "Claude flags" line in the doc. Set Drafts status to `Checked`.
6. Run `python scripts/scorecard.py` and write its row to the Scorecard tab and its sentence to the Scorecard section of the doc.
7. Write one Run log row.

If you cannot write into the Google Doc cleanly, write only to the Checks and Scorecard tabs. Fo reads those.

---

## Measurement

Configured under `measure` in `rules.yaml`. Each owner defines their stages, lowest first, and what each is worth.

- **Time:** `review_minutes` (from the call) against `baseline_minutes` (the owner's timed manual routine).
- **Moved up:** of members contacted in the last `moved_up_window_days`, how many are now at a higher stage than on the day they were contacted. The same for the hold-back group, measured from the day they would have been contacted.
- **Revenue:** add up Conversions rows for contacted members dated within `attribution_days` after their first contact. Work out the conversion rate in the hold-back group over the same window, and subtract what that rate would have produced among the contacted members anyway. Report the running total against `revenue_target`.

Claude computes these with `scripts/scorecard.py`. Fo reports them on the call but does not compute them, because Fo wrote the messages.
