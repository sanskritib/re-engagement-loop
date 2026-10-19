---
name: re-engagement-loop
description: Run a daily re-engagement loop for a paid community or audience. Fo reads the member export, sorts members into re-engagement segments, drafts a personal email for each, reviews them with the owner on a call while the owner follows along in a call doc, and sends (or saves to drafts) only what the owner approves, with a voice note. Claude checks every draft and keeps the scorecard. Right after install it offers a five-minute demo call on fictional data. Use when an owner wants members followed up on without doing it by hand.
version: 0.4.0
---

# Re-engagement loop

Three steps run on their own schedules and pass work to each other through two shared files: the **member sheet** (a Google Sheet) and the **outreach doc** (a Google Doc). The agents never call each other directly. If a step does not run, the next step notices and says so.

| Step | Default time | Who | Reads | Writes |
| --- | --- | --- | --- | --- |
| 1. Draft | 02:00 | Fo | Members, Touchpoints, rules, Editor's Notes | Outreach doc, Drafts tab, Status history tab, Run log |
| 2. Check | 05:00 | Claude | Outreach doc, Drafts, Members, Touchpoints, Status history, rules | Checks tab, Scorecard tab, flags in the doc, Run log |
| 3. Review and send | 08:00 (owner's time) | Fo | Outreach doc, Checks, Scorecard | Outreach doc, Drafts, Touchpoints, Run log |

Times are in the owner's time zone and come from `rules.yaml`.

**Where members are read and where they are reached are kept separate**, and every platform is set up in one of two modes:

| Mode | When | Reading members | Reaching members |
| --- | --- | --- | --- |
| `read_only` | The platform's terms forbid bots or automation (Skool's community rules do), or Fo has no approved way in | From an export the owner downloads (CSV) into the member sheet | Only through the owner's own channels, by default the owner's email |
| `connected` | The platform allows automation and offers an official integration or app the owner has connected (for example a Slack or Discord app an admin installed, or a CRM with an API) | Fo retrieves the member list itself on each run | Through the platform's official integration if the owner turns that on, otherwise email |

Fo decides the mode at setup (see Step 0) and records it as `community.mode` in `rules.yaml`. When unsure, it's `read_only`. A `read_only` platform is never acted inside: no posts, comments or direct messages there, and no logging in as the owner.

## Installing (for Claude, when an owner asks you to set this up)

Fo is reached through Fo's MCP server. Check your tools before anything else.

**If Fo's tools are available** (`ask_fo`, `get_fo_reply`, `start_fo_call`, `list_fo_conversations`, `get_fo_conversation`), you do the install for the owner:
1. Ask the owner for their member sheet link, or whether to use the demo data, if they haven't said.
2. Send Fo the install message from `prompts/install-fo.md` with `ask_fo`, with the sheet link or "use the demo data" filled in.
3. While Fo works, keep calling `get_fo_reply`, but only tell the owner when Fo's progress actually changes, in one line. When Fo asks setup questions, put them to the owner all together, word for word, and send all their answers back in one `ask_fo`. Never answer for the owner. When Fo asks the owner to connect their email, relay the instructions and wait for the owner to confirm before telling Fo it's done.
4. **Show each file as soon as Fo makes it**, with a link and one line on what it's for. For example: "Fo made your member sheet: <link>. This is your community." Then "Fo made your call doc: <link>. Keep this open when Fo calls; it's what Fo walks you through."
5. When Fo sends the checker prompt, set up Step 2 as a scheduled task if you can create one; otherwise give the owner the prompt and say where it goes.
6. **Offer the demo call** (see "Demo call"): "Want to try a five-minute demo call with Fo now, on the fictional community?" Offer it after every first install, whether the owner used the demo data or their own sheet.
7. Afterwards you can use `start_fo_call` to give the owner a link to a review call on demand, and `list_fo_conversations` / `get_fo_conversation` to read call transcripts if they ask what was approved.

**If Fo's tools are not available,** tell the owner how to connect Fo, then continue from step 1 once it's connected:
- Endpoint: `https://mcp.api.wajo.ai/fo` (Streamable HTTP), signed in with their Wajo account on the OG Fo plan.
- Claude Code: `claude mcp add --transport http fo https://mcp.api.wajo.ai/fo`, then run `/mcp` to sign in.
- Claude apps: add the endpoint as a custom connector and sign in when prompted.
- Or skip MCP: they can paste the message from `prompts/install-fo.md` into any chat with Fo.

Fo's actions are real. During install, the only things Fo should create are tabs, the outreach doc, `rules.yaml` and the two scheduled jobs. No member is contacted during setup.

## Demo call (the first run, right after install)

A five-minute guided call on the fictional community, so a new owner hears the whole loop before it touches their own members. It uses ready-made drafts from `demo/coaching-skool/demo-call.md`, so Fo has nothing to compute and can call within a minute.

**The demo's scenario:** the coach has told members that they use an assistant, Fo, for outreach, and that every message is the coach's own words (`community.members_informed: true`). So in the demo, Fo sends the test email itself, from its own address, with the voice note attached, signed as the coach's assistant (`send.from: fo`). The tester agrees to this by giving their email.

**With the demo data, the demo call comes first and setup questions come after.** During a demo install, Fo asks only for the tester's name and email. Everything else uses the defaults in `rules.example.yaml`, saved as `rules.yaml` and marked "defaults, not yet confirmed". After the demo call, Fo asks the setup questions. If the owner says "run the loop now" or "call me" before the demo call has happened, that means the demo call.

**Claude, when the owner says yes:**
1. Ask: "Who should get the real test email? Give a name and email address. It can be your own second address." This is the only message the demo can send.
2. `ask_fo`: "Prepare the demo call for the re-engagement loop. Tester: <name>, <email>. Follow 'Demo call' in SKILL.md. Reply with the call doc link, and don't call yet."
3. As soon as Fo replies, show the owner the link and say: "**Open this doc now.** It's what Fo will walk you through on the call. Fo is calling you now."
4. `ask_fo`: "Call me now for the demo call." If the owner would rather talk in this app, use `start_fo_call` and give them the link instead.
5. After the call, ask Fo what the owner decided, and report it in two lines. If Fo sent the test email, say it's coming from Fo's address and can take a minute or two to arrive (check spam too). If it was saved to drafts instead, say where. Don't ask Fo to send it again.
6. Offer the next step: "Want me to switch it to your own member sheet, or keep the demo running for a few days?"

**Fo, when asked to prepare the demo call:**
1. If the demo sheet doesn't exist yet, build it as in Step 0 (demo data). Put the tester's name, email and `channel` = `email` in the Tester row. Use `send.from: fo` and `community.members_informed: true` for the demo, whatever the owner chose for their real community.
2. Create a Google Doc called "Your call with Fo (demo)" from `demo/coaching-skool/demo-call.md`. Fill in `{TESTER}` (the tester's first name), `{OWNER}` (the owner's first name), `{DAY}` (today's weekday) and `{DATE}`. Add the four drafts to the Drafts tab with status `Checked`, and copy the check results into the Checks tab.
3. Make the tester's voice note now, before the call: Fo's part only ("Hi <tester>, this is Fo, <owner>'s assistant…"), as an audio file. On the call you add the owner's own words, then play the finished note back.
4. Reply with the doc link. Don't call until you're asked.

**Fo, on the demo call:**
1. "Hi <owner>, it's Fo. Have you got the call doc open? I'll go through it from the top." Wait until they have.
2. Say the three numbers in "Today in three numbers" in plain words, then the agenda in one sentence: "Today: your test email first, then a renewal, a win, and one draft Claude flagged."
3. **The tester's draft first.** Read it. Ask: "Want to add a sentence in your own words for a voice note?" Make the voice note (see "Voice notes over email") and play it back.
4. Ask: "**Do you want me to send this email to <tester> now?**" If they say yes, send it from your own address with the voice note attached, signed as their assistant. Confirm it's in your Sent folder and say: "Sent. It's from me, as your assistant, and should arrive in a minute." Follow any other answer as usual: save to drafts, change, or skip.
5. Offer the rest: "There are three more drafts from fictional members. Want me to go through them, or stop here?" On the flagged draft, explain Claude's flag in one sentence and ask whether to use the suggested fix.
6. Close: read back every decision ("Your test email: sent. Niklas: saved to your drafts. Leonard and Wallace: no decision, still drafts."), then: "That's the demo. From tomorrow I'll call at <time> with real drafts."
7. Log the call to the Run log with `step=demo`.

## Run now (for testing and demos)

The owner can run the whole loop on demand instead of waiting for the schedule, by saying "run the loop now" to Claude or Fo. The scheduled jobs are not changed.

**When Claude is driving (Fo's MCP connected):**
1. `ask_fo`: "Run Step 1 (Draft) of the re-engagement loop now. Reply with the outreach doc link when the drafts are in." Poll `get_fo_reply` until it completes.
2. Run Step 2 (Check) yourself right away, without asking, as described under "Claude (checker)". If you can't edit the sheet from here, say so and continue; Fo will report that the check didn't run.
3. Show the owner the outreach doc link: "**Open this doc.** It's what Fo will walk you through. Fo is calling you now."
4. `ask_fo`: "Run Step 3 (Review and send) now: call me now instead of at the scheduled time." Fo places the call. If the owner prefers to talk in this app, use `start_fo_call` and give them the link instead.
5. During the call, Fo updates the outreach doc and Drafts tab live. After it ends, read the Run log and tell the owner what was approved, sent and logged.

**When the owner asks Fo directly:** Fo runs Step 1, waits about two minutes for Claude's check (or proceeds and says it didn't run), then runs Step 3 and calls immediately.

A run-now still follows every rule: nothing is sent without approval, and the contact limits count it like any other run.

---

Read the section for your role only. **If you are Fo, follow "Fo". If you are Claude, follow "Claude (checker)".** Both follow "Rules for everyone".

---

## Uninstall or reset

When the owner says "uninstall the re-engagement loop" or "reset the loop" (for example after a test run, before installing again for real or for a demo):

A reset erases everything the loop left behind, so the next install behaves exactly like the first one ever (for example before recording a demo).

1. **List everything the loop created or touched**, and read the list back to the owner in one message:
   - scheduled jobs;
   - Drive files: the folder, member sheet, outreach and call docs, `rules.yaml`, and any copies from earlier installs (search Drive for "Re-engagement loop" and "Northstar");
   - email: drafts the loop saved in the owner's email, and test emails it sent;
   - Fo conversations about this loop, on every channel, including calls;
   - what you remember about it.
2. **Ask once**: "I'll delete the jobs, move these files to your Drive trash, delete the loop's drafts, delete these conversations and forget all of it. Go ahead?" Wait for a yes. Never touch the owner's own member sheet or tabs.
3. **Delete the loop's scheduled jobs.** After this nothing runs, calls or sends.
4. **Move every listed Drive file to the trash.** Say the owner can empty the trash to remove them for good.
5. **Delete the loop's email drafts.** Leave sent emails alone. They can't be recalled; say how many there were.
6. **Delete your conversations about this loop**, including call transcripts, on every channel you can. Say exactly which ones you couldn't delete.
7. **Forget the loop completely.** Remove from your memory everything about it: setup answers, rules, segments, testers, Editor's Notes, drafts, calls, run history, and that it was ever installed. If something can't be removed, say exactly what you still remember.
8. **Treat the next install as the first ever.** Don't mention earlier installs, runs, testers or emails ("like this afternoon"), and don't suggest answers from them. Ask the setup questions fresh. The owner's own profile (name, phone, email, time zone) is not part of the loop and stays.
9. **Claude** removes the checker's scheduled task if it set one up. It tells the owner that Claude chats about the loop can be deleted from the chat list. If Claude has a memory of the loop, it asks before removing it.
10. Confirm in a few lines what was deleted, what was trashed, what was forgotten, and anything that couldn't be removed.

Anything already sent to members stays sent; a reset can't recall emails.

---

## Rules for everyone

These cannot be switched off in `rules.yaml`.

1. **Nothing is sent without the owner's explicit approval** of that specific message. Approval happens on the call or in writing in the outreach doc. A summary email or text is never approval. Only a clear decision counts ("send it now", "save it to my drafts", "yes"). A draft with no decision stays `Drafted`, even if the call ends early. Before the call ends, read every decision back.
2. **Only contact people in the member sheet**, through the channel listed for them, and never more often than `pick.min_days_between_contacts`. A member whose `channel` is `none` can be picked, drafted and reviewed, but is never sent anything; use it for demo rows and dry runs. Emails come from the owner. Fo saves each approved email to the owner's drafts and the owner presses send. Fo sends an email itself only if it can send from the owner's own account, or if the owner opted in at setup to sending from Fo's own address (`send.from: fo`). That opt-in is only allowed when the owner has told members they use an assistant for outreach (`community.members_informed: true`). Fo's own address always says it's from Fo, the owner's assistant. Never switch to Fo's address without that opt-in.
3. **Skip anyone who has opted out, is in the hold-back group, or is marked `skip`.**
4. **Separate what you saw from what you assume.** "Last active 21 days ago" is seen. "Probably busy with work" is an assumption and must be labeled as one. Missing data means unknown, not inactive.
5. **No guilt, pressure, fake urgency or invented offers.** The owner's tone settings apply on top of this.
6. **Respect each platform's mode.** On a `read_only` platform, never act inside it: no posts, comments or direct messages, no logging in as the owner. On a `connected` platform, act only through the official integration the owner connected, and only for direct messages to people in the sheet. Never post publicly anywhere.
7. **Never change `rules.yaml`.** Propose changes to the owner; the owner edits the file.
8. **Log every run** to the Run log tab, including runs that did nothing or failed.
9. **Do not put member data anywhere other than the owner's own sheet and doc.**
10. **Say "sent" only when it's sent.** After sending, confirm the email is in the owner's Sent folder before saying it went out, and record it. The recipient may take a minute or two to see it, so a missing email in their inbox is not a failure. Never send again without first checking the Sent folder.
11. **Talk like a person.** Call each draft by the member's first name and when it's meant to go out: "Hana's Monday-morning draft", not "D-2026-10-18-02". Draft IDs live in the sheet and are never said aloud or written in chat. Speak in plain words, and round numbers when an exact one doesn't matter.

---

## Shared files

### Member sheet tabs

Column names are configurable in `rules.yaml` under `columns`. Defaults:

**Members** (owner's data, kept current by the owner's existing sync)
`member_id, name, email, channel, profile_link, joined, last_active, posts, intro_posted, posts_30d, calls_attended_30d, goal, goal_updated, recent_win, recent_win_date, stage, renewal_date, plan_value, cancelled, last_contacted, opted_out, skip, notes`
`posts` is the member's total posts and `posts_30d` the last 30 days; `intro_posted` is yes/no. Leave a column blank if the export doesn't have it; blank means unknown, never zero, and the segments that need it are skipped.

**Status history** (one row per member per day, written by Fo in step 1)
`date, member_id, stage`

**Drafts** (one row per draft, the machine-readable ledger)
`draft_id, date, member_id, name, rule, reason, status, final_text, approved_at, sent_at`
Status moves: `Drafted → Checked → Approved → Sent` or `→ Saved to drafts`, or `→ Skipped`. A member in the hold-back group who matched a rule gets a row with status `Held back` and no draft; that row is the comparison group's start date.

**Touchpoints** (one row per message sent or received)
`date, member_id, channel, direction, draft_id, summary, replied, reply_date`
If the owner already keeps a Touchpoints tab with their own columns (for example `Date, Member, Type, What was said`), keep those and add the missing ones; fill both. Headers are matched case-insensitively.

**Segments & strategies** (the playbook; owner-editable)
`segment, priority, enabled, signal, strategy, example_subject, voice_note_idea, added_by, added_on`
`added_by` is `default`, `owner` or `brainstorm`. Fo adds rows only after the owner approves them.

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

The outreach doc is the **call doc**: the owner keeps it open while Fo calls, the way you'd follow someone's slides while they present. It reads top to bottom in the order the call goes. Everyone who mentions it says so: "Open this doc. It's what Fo will walk you through."

```
# Your call with Fo · <weekday>, <date>

Keep this doc open during the call. Fo walks through it from top to bottom.

## Today in three numbers
<three bullets in plain words: the three numbers that shape today's call, e.g.
 the money at risk, the biggest group, the best news. Each says why it matters.>

## On today's call
<numbered list of the drafts in the order Fo will go through them, one line each>

## Drafts
### <First name>'s <weekday>-morning draft
- Why them: <one line, with the segment in brackets>
- Seen: <facts from the sheet, with dates>
- Assumed: <labeled assumptions, or "none">
- Draft:
  > <subject and message>
- Claude's check: <filled in by Claude in step 2>
- Your decision: <filled in on the call>
- Ref: <draft_id, for the sheet only>

## Scorecard
<one paragraph from the Scorecard tab, written by Claude>

## Since yesterday
<what changed: replies, stage moves, anything sent>

## All segments
<one line per segment: count, how many drafted, how many held back>

## Editor's Notes
<standing feedback from the owner; Fo reads this before every draft run>
```

"Weekday-morning" is when the email goes out if approved on that morning's call.

**Choosing the three numbers.** Pick the three that should shape the call: usually the renewal or revenue risk, the biggest segment, and one piece of good news (a recent win, a reply, a member who moved up). If a draft for a tester is in the run, put it first in "On today's call".

### Hold-back group

To measure honestly, some quiet members are deliberately not contacted. A member is in the hold-back group when the last digit of the number in their `member_id` is in `measure.holdout_digits` (default `0` and `5`, about 20%). This rule is fixed so Fo can apply it without code and Claude can check it.

---

## Re-engagement segments

Fo doesn't just find "inactive" members. It sorts every member into segments, each with its own strategy, kept in the **Segments & strategies** tab of the member sheet so the owner can read, edit, switch off or add to them. A member can match several segments; Fo uses the highest-priority one that is switched on.

| Segment | Signal (from the sheet) | Strategy | Example subject |
| --- | --- | --- | --- |
| `renewal_at_risk` | Renewal within 30 days, not active for 7+ days | Remind them what they came for and what's coming up before the renewal; ask one easy question | "Before your renewal: what you said you wanted from this" |
| `never_started` | Joined 7+ days ago, no intro, no posts | Lower the bar: invite a one-line intro or to just listen in on the next call | "No intro needed. Just come say hi" |
| `went_quiet` | Not active for 14+ days | Reference their goal or last contribution; ask how it's going, no guilt | "How's the book coming along?" |
| `fading` | Was active (5+ posts) but no posts and no calls in 30 days | Notice the change kindly; offer a small way back in | "We've missed your updates" |
| `recent_win` | A win logged in the last 14 days | Celebrate it and invite them to share it with the group (re-engages them and others) | "Saw your win. Would you share how you did it?" |
| `goal_stalled` | Goal set, not updated for 30+ days | Check in on the goal itself; offer to reset or shrink it | "Is the goal still the goal?" |
| `lurker` | Active in the last 7 days but no posts or calls in 30 days | Turn reading into one small action: a question to answer, a thread to join | "A quick question I think you'd answer well" |
| `skipping_calls` | Active but no calls attended in 30 days | Share what they missed and one reason to join the next one | "What you missed on Thursday's call" |
| `win_back` | Cancelled or churned (only if the export includes it) | A warm, no-pressure note; ask what would have helped | "No pitch. Just a question" |

Rules for segments:
- A segment only runs if its columns exist in the sheet. Missing data means the segment is skipped, never guessed.
- A member who cancelled is only ever in `win_back`, never in the other segments, even though they look inactive.
- Each run, Fo picks at most `pick.max_per_segment` members per segment and `pick.max_per_run` in total, highest priority first.
- The call always opens with the count for every segment, so the owner sees the whole community, not just the drafts.

### Brainstorm mode

The owner can say "let's brainstorm strategies" any time, on the call or in chat. Fo also offers it when a segment is large, gets few replies, or the owner sounds unsure.

In brainstorm mode Fo:
1. Looks at the segment counts, recent replies and what's worked (from Touchpoints and Scorecard).
2. Proposes two or three new segments or strategies, each with its signal (which columns), its angle, and an example subject. It says when a signal needs a column the sheet doesn't have.
3. Talks them through with the owner and adapts them.
4. Adds only the ones the owner explicitly approves to the Segments & strategies tab, with `added_by` = `brainstorm` and the date, switched on from the next run.

---

## Fo

### Step 0: Setup (once, when the owner installs the skill)

The owner gives you either their own member sheet or the words "use the demo data". You prepare everything else, in the owner's own Google Drive. Nothing is needed from anyone else's Drive.

**Demo data (when the owner asks for it, or has no member sheet yet):**
The demo is a fictional paid coaching community, "Northstar Coaching Circle", with 157 members, every segment represented, and a filled Segments & strategies tab. It's there so a new owner can watch the whole loop work before touching real data, and it can be swapped for their own export at any time (see `demo/README.md`).
- Create a new folder "Re-engagement loop (demo)" in the owner's Drive. If you can't create folders, put the files in the Drive root with names starting "Re-engagement loop (demo) – " so they sort together. Tell the owner once; don't ask them to move anything.
- Create a Google Sheet there from `demo/coaching-skool/demo-member-sheet.xlsx` in the repo. If you can't import the file directly, create the sheet and fill one tab per CSV in `demo/coaching-skool/`, entering cells as user-entered so the formulas calculate.
- The demo is a fictional coaching community. Every member has `channel` = `none`, so nothing can be sent to them.
- Ask the owner who should receive real emails during the test (for example a teammate, or the owner's second address). For each tester, fill the "Tester" row (add more rows if needed) with their name and email, and `channel` = `email`. Only these rows can ever be sent to. Set their last-active date 20 days back so they are picked on the first run. Tester drafts always come first on the call.
- Then continue from step 2 below with this sheet.

**Own sheet:**

1. Read the member sheet. Match its columns to the skill's names (see `columns` in `rules.example.yaml`) and show the owner the mapping before using it.
2. Add any missing tabs the loop needs (Segments & strategies, Status history, Drafts, Touchpoints, Conversions, Checks, Scorecard, Run log). Fill Segments & strategies with the default segments from "Re-engagement segments", all switched on except those whose columns are missing, with the headers listed under "Shared files". Add missing columns to Members (`member_id`, `channel`, `profile_link`, `plan_value`, `opted_out`, `skip`) at the right-hand end. Fill `member_id` as `M-0001`, `M-0002`, … in row order.
   - Never delete, rename, reorder or overwrite the owner's existing tabs, columns, formulas or data.
   - If a Touchpoints tab already exists with other columns, keep them and add the missing ones.
3. Create the outreach doc in the same folder as the sheet, using the layout under "Outreach doc layout", with an empty Editor's Notes section.
4. **Contact details for the call.** Check what you already know about the owner from their Wajo account: phone number, email, time zone. If you have them, confirm them in one line ("I'll call you on +1 … — still right?") instead of asking again. If you don't have a phone number, ask for it once and save it to their Fo profile so other tasks can use it too. If they'd rather not give one, the morning review uses a call link instead (`start_fo_call`), sent by email or text at the scheduled time.
5. **Platform mode and channel access.**
   - Find out what the community platform allows. Read its adapter in `adapters/` if there is one (its `mode` line), and check the platform's current terms for rules on bots, automation or scraping. If they forbid it, or you can't confirm an official integration the owner has connected, the mode is `read_only`. Tell the owner which mode you chose and why in one sentence.
   - `read_only`: ask how they get the member export (for example a members CSV from the admin settings) and how often they'll refresh it. `connected`: run a read-only test that lists a few members through the integration.
   - Then check the sending channel: read `adapters/email.md` ("Access needed") and run its read-only test on the owner's email account. Send nothing.
   - If you can, tell the owner in one line how you reach the platform.
   - If you can't, ask the owner to connect their email at wajo.ai now. Never ask for a password in chat and never type one in yourself. Wait for them to say it's done, then run the read-only test again.
   - If they'd rather not connect it, set the adapter to hand-send and say what that means: you prepare each approved message and they paste it.
**Keep setup about the loop.** Don't bring up anything else from the owner's calendar, email or other tasks in setup questions or on calls (for example "your 8:30 prep text"). The owner may be sharing their screen.

6. Walk the owner through `setup/questions.md` (skip anything you already know from step 4) and write their answers to `rules.yaml` next to the sheet. Always ask these two, because they set defaults the owner can change by voice later:
   - **How approved emails go out:** first check whether you can send from the owner's own email account. If you can, ask: "When you approve an email, should I send it straight away, or save it to your drafts?" Save it as `send.default`. If you can't (the usual case), say so plainly and ask: "I'll save approved emails to your drafts and you press send. That's the default. Or, if you've told your members you use an assistant for outreach, I can send them myself from my own address, signed as your assistant. Have you told them, and which do you prefer?" Save `community.members_informed`, `send.from` (`owner` or `fo`) and `send.default` (`save_to_drafts`, or `send_now` only with `send.from: fo`).
   - **Segments:** read out the segments in the "Segments & strategies" tab (see "Re-engagement segments") in one sentence each, ask which to turn on, and ask: "Want to brainstorm any of your own now?"
   Read the file back to them for confirmation.
7. Create the two scheduled jobs (Step 1 and Step 3), and read back the times, what each does, and the phone number and email.
8. Send the owner the links to the sheet, the outreach doc and `rules.yaml`, plus the prompt from `prompts/claude-checker.md` with the links filled in, so they can set up the Claude checker.
9. Write a Run log row: `step=setup`.

### Step 1: Draft (night)

1. Read `rules.yaml`, the Members, Touchpoints and Drafts tabs, and the Editor's Notes section of the outreach doc.
2. Append today's stage for every member to Status history.
3. Sort every member into the segments that are switched on in the Segments & strategies tab, and record the count per segment in the doc's "All segments" section. Pick members not excluded by "Rules for everyone" 2 and 3: at most `pick.max_per_segment` per segment and `pick.max_per_run` in total, highest priority first. Use the segment's strategy for the draft, and put the segment id in the Drafts `rule` column. For each member who matched a rule but is in the hold-back group, add a Drafts row with status `Held back`, the rule, and no draft, unless they already have one in the last `measure.attribution_days`.
4. For each pick, write a block in the outreach doc (layout above), headed with the member's first name and the morning it would go out, and a Drafts row with status `Drafted`. Then fill in "Today in three numbers" and "On today's call" at the top of the doc. The draft:
   - is written for this person from what the sheet says about them;
   - follows `tone` and everything in Editor's Notes;
   - is signed as the owner;
   - stays under `tone.max_words`.
5. Update "Since yesterday".
6. Write one Run log row. If nothing matched, log `nothing_to_do` and leave the doc saying so.

### Step 3: Review and send (morning)

1. Read the outreach doc, Drafts, Checks and Scorecard.
2. If no Checks rows exist for today's drafts, tell the owner at the start of the call: "Claude's check didn't run today." Continue.
3. Call the owner at `owner.call_time` on `owner.phone`. In the call notification (text or email), include the outreach doc link: "Open this before you pick up."
4. On the call:
   - Start by checking the owner has the outreach doc open: "Have you got today's call doc open? I'll go through it from the top." Send the link again if they don't.
   - Then "Today in three numbers", in plain words, and the agenda in one sentence ("Today: four drafts. A renewal first, then two people who never started, then a win."). Then the scorecard in one sentence. Give the full segment counts only if the owner asks; they're in the doc under "All segments".
   - Go through each draft in the doc's order, by name ("Hana's Monday-morning draft"): why them, what you wrote, and Claude's check.
   - Apply the owner's changes to the doc while you talk, and say what you changed.
   - Ask for a clear decision on each draft, in the owner's words: **send it now**, **save it to my drafts**, **change it**, or **skip**. If you can't send from the owner's account and they haven't opted in to your own address, "send it now" means: save it to their drafts and tell them it's ready to send ("It's in your drafts, at the top. Just press send."). If they just say "approve" or "yes", use `send.default` and say which you're doing ("Sending it now" / "Saved to your drafts").
   - For each approved draft, offer the voice note: "Should I add a voice note to this email?" If yes, follow "Voice notes over email".
   - If a segment has many members, few replies, or the owner sounds unsure about an angle, offer once per call: "Would you like to brainstorm another strategy for this group?" (see "Brainstorm mode").
   - If the owner gives standing feedback ("never mention price"), add it to Editor's Notes.
   - If the owner asks for a rule change, note it under "Your decision". Do not edit `rules.yaml`.
   - Before hanging up, read back every decision, including drafts with none ("Hana: sent. Sam: saved to your drafts. Priya: no decision, still a draft."). Fix anything the owner corrects.
5. If the owner does not answer after `owner.call_retries` attempts, email and text a short summary to `owner.email` and `owner.phone`. Send nothing to members that day.
6. For each draft the owner said to **send now**: send it through the member's channel adapter (see `adapters/`), from the owner's account or, if the owner opted in, from your own address. Confirm it's in the Sent folder (rule 10). Then set Drafts status `Sent` with `sent_at` and `final_text`, add a Touchpoints row, and update `last_contacted`.
   For each draft the owner said to **save to drafts**: create it as a draft in the owner's email (subject, body, any voice note attached) without sending, set Drafts status `Saved to drafts`, and don't count it as a contact until the owner sends it. Next morning, mention any saved drafts still unsent.
7. If an adapter cannot send, set status `Approved`, give the owner the text and profile link to send by hand, and log it.
8. Record replies you see in Touchpoints (`direction: in`).
9. Write one Run log row with how long the call took in `note` (`review_minutes=<n>`).

---

## Voice notes over email

Voice notes are a core part of the loop and are on by default (`voice_notes.enabled: true`; the owner can turn them off). Any approved email can carry a short voice note as an audio attachment. The note has two parts, always in this order:

1. **The owner's words, verbatim.** On the call, after the owner approves a draft, ask: "Want to add something in your own words for the voice note?" Take exactly what they said from the call transcript. Remove filler words only, change nothing else, and read the quote back to confirm.
2. **Your part, in your own voice, openly as the owner's assistant.** One or two sentences: who you are, why you're writing, one easy next step. For example: "Hi Sam, this is Fo, Majid's assistant. Majid asked me to pass this on in his words: '…'. He'd love to see you on Thursday's call. Just reply to this email if you'd like a spot."

Rules:
- Always your own voice. Never imitate, clone or synthesize the owner's voice.
- Your part uses only facts that are in the approved email. If the email says "you joined in July", don't say "most of a year".
- The note says it comes from Fo, the owner's assistant.
- Actually make the audio file, and play it to the owner on the call before it goes out. Text approval isn't enough for audio. If you can't play audio on the call, send the file to the owner by text or email and wait for a "yes" before attaching it. Never say a voice note is attached unless the file is attached.
- Write a subject line that makes the member want to open it and is true to the content (for example "A quick voice note from Majid's team about your book goal"). No clickbait, no fake urgency.
- Email only, as an attachment under `voice_notes.max_seconds`, saved in the owner's draft or sent as `send.from` allows. The email body still contains the full text, so it works without audio.
- Log the transcript of the full note in Drafts `final_text`, and `channel` = `email+voice` in Touchpoints.

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
5. Write every flag to the Checks tab, and copy it into the draft's "Claude's check" line in the doc, in plain words (for example "pressure: 'don't miss out' adds urgency that isn't true"). Set Drafts status to `Checked`.
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
