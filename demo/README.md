# Demo data

`coaching-skool/` is a fictional paid coaching community, **Northstar Coaching Circle**, built so anyone can watch the whole loop work before using real data. Names are placeholders, emails are `@example.com`, and every member has `channel` = `none`, so nothing can ever be sent to them.

## What's in it

| Tab | What it holds |
| --- | --- |
| Members | 157 fictional members: join and last-active dates, goals, total posts and posts in the last 30 days, calls attended, intro posted, recent wins, cancellations, and one **Tester** row |
| Segments & strategies | The nine default segments with their signal, strategy, example subject and voice-note idea. Editable |
| Touchpoints, Weekly pulse | The owner's own tracking tabs, kept as they were |
| Status history, Drafts, Conversions, Checks, Scorecard, Run log | Written by the loop |
| How to use | What each column and tab means |

On 18 Oct 2026, members sort into segments roughly like this (each member counted once, in its highest-priority segment):

| Segment | Members |
| --- | --- |
| renewal_at_risk | 4 |
| never_started | 28 |
| went_quiet | 50 |
| fading | 6 |
| recent_win | 5 |
| goal_stalled | 10 |
| lurker | 6 |
| skipping_calls | 10 |
| win_back | 4 |

Counts move as the dates age, which is the point: the community changes every day.

## Using it

Tell Claude: *"Install the re-engagement loop for me using Fo, with the demo data."* Fo builds this sheet in your own Drive from `demo-member-sheet.xlsx` (or the CSVs, one per tab).

Then say yes to the **demo call**. Claude asks whose email should get the real test message. Fo turns `demo-call.md` into your call doc: three numbers, then four ready-made drafts, with your tester's first. Claude gives you the link to open, and Fo calls you to walk through it. On the call you can add a voice note and send the test email.

For a full run, where Fo sorts all 157 members and writes fresh drafts, say *"Run the loop now."*

## Switching to your own data

1. Export your members from your platform (for example the members CSV from your community's admin settings).
2. Paste it into the Members tab, or point Fo at your own sheet instead.
3. Fo matches your column names to the skill's and shows you the mapping. Columns you don't have are fine: segments that need them are skipped, never guessed.
4. Keep the Segments & strategies tab, edit it, or brainstorm new rows with Fo.
