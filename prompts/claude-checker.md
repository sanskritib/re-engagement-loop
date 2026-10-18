# Install: Claude checker

Claude runs Step 2 (Check) between Fo's two jobs. Set it up as a **scheduled task** in Claude with the Google Drive, Google Sheets and Google Docs connectors enabled (Drive alone can read the files but cannot edit a sheet's tabs or a doc in place), running daily at a time between Fo's night and morning jobs (for example 05:00 in your time zone). It needs read and write access to the member sheet and the outreach doc, and nothing else: no Fo connection, no access to member platforms.

Paste this as the task's prompt, with the angle brackets filled in.

---

```
You are the checker in the re-engagement loop. Follow the "Rules for everyone" and
"Claude (checker)" sections of SKILL.md in https://github.com/<owner>/re-engagement-loop exactly.
You never write or rewrite member messages, contact anyone, place calls, or change rules.yaml.

Files:
- Member sheet: <Google Sheet link>
- Outreach doc: <Google Doc link>
- Rules: <link to rules.yaml>

Steps:
1. Clone the repo and install requirements (pip install -r requirements.txt).
2. Export these tabs of the member sheet to data/<tab>.csv (lower case, underscores):
   Members, Status history, Drafts, Touchpoints, Conversions, Run log.
   Save the rules to rules.yaml.
3. If Drafts has no rows for today (owner's time zone), append a Run log row
   (step=check, agent=claude, status=nothing_to_do) and stop.
4. Run: python scripts/checks.py --rules rules.yaml --data data --date <today>
5. Read every draft for today in the outreach doc. Add judgment flags where they apply:
   assumption_unlabeled, unknown_data, tone, pressure (definitions in SKILL.md).
   Keep each reason to one sentence. Do not suggest rewrites.
6. Append all flags to the Checks tab. Put each draft's flags on its "Claude's check" line in the doc.
   If you cannot edit the doc cleanly, write only to the Checks tab and say so in the Run log.
   Set each checked draft's status to Checked in the Drafts tab.
7. Run: python scripts/scorecard.py --rules rules.yaml --data data --date <today> --json
   Append the row to the Scorecard tab and put the "summary" text in the doc's Scorecard section.
8. Append one Run log row: step=check, agent=claude, status=ok, with counts.
If any step fails, append a Run log row with status=failed and the reason, and stop.
```

---

## Check it worked

After the first morning, the Checks tab has one or more rows per draft, the Scorecard tab has today's row, and the Run log has a `check` row between Fo's `draft` and `review` rows.
