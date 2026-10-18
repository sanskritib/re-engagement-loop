# Re-engagement loop

A packaged skill for anyone who runs a paid community or audience (coaches, community managers, creators, course and membership owners) and loses track of the people who drift away or never get started.

Every night, **Fo** reads your member export and finds who needs a nudge: people who went quiet, people who joined but never posted, people whose renewal is coming up. It drafts a personal email for each. Before morning, **Claude** checks every draft against your rules and updates the scorecard. Then Fo **calls you**: it gives you the whole picture first ("of 157 members, 23 went quiet, 11 never started…"), walks through each draft and why, and changes it while you talk. For each one you say **"send it now"** or **"save it to my drafts"**. Optionally, Fo adds a short **voice note** that quotes you word for word.

No dashboard to check. The loop comes to you: a phone call, a doc you can edit, and an email or text if you miss the call.

**Your members are read from your platform's export, and reached through your own email.** Many community platforms (Skool among them) don't allow bots or automated messages, so the skill never acts inside the platform.

Built for the Wajo × Anthropic hackathon, October 2026, and inspired by a coach running a paid Skool community. Version 0.2.

## How it works

Three steps, each on its own schedule, passing work through two shared files: your **member sheet** (Google Sheet) and your **outreach doc** (Google Doc). Nothing runs on your laptop, and the two agents never call each other directly.

| Default time | Who | What happens |
| --- | --- | --- |
| 02:00 | Fo | Reads your member export, sorts everyone by your rules, picks who to reach out to and why, writes an email draft for each into the outreach doc |
| 05:00 | Claude | Checks every draft against your rules and flags problems (without rewriting), then updates the scorecard |
| 08:00 | Fo | Calls you, opens with the full picture and the scorecard, reviews each draft with you, sends or saves to your drafts as you say, logs everything |

If a step doesn't run, the next one notices and tells you. Every run is logged.

## What you get each morning

- **Time:** how long the review took, against your own timed manual routine.
- **Movement:** how many contacted members moved up a stage, against a small group deliberately held back for comparison.
- **Revenue:** renewals and upgrades that followed outreach, minus what the held-back group did anyway, as a running total against your target.

Claude computes these, not Fo, because Fo wrote the messages.

## Install

You need a Wajo account on the OG Fo plan with Google (Drive and Gmail) connected, and your member export in a Google Sheet. Or nothing but the Wajo account, to try the demo.

**Easiest: ask Claude.** Add this repo's `SKILL.md` as a skill in Claude (or just share the repo link), make sure Fo's MCP is connected (`https://mcp.api.wajo.ai/fo`), and say: *"Install the re-engagement loop for me using Fo. My member sheet is <link>."* To try it first, say *"…using Fo, with the demo data"* instead: Fo builds a fictional coaching community in your own Drive, and asks whose email should receive the real test message. Claude sends the install to Fo, relays Fo's setup questions to you, and sets up the checker.

To see it work immediately instead of waiting for the night, say *"run the loop now"*: Fo drafts, Claude checks, and Fo calls you straight away.

**Or do it by hand:**

1. **Send Fo the install message** in [`prompts/install-fo.md`](prompts/install-fo.md), with your sheet's link. Fo adds the loop's tabs to your sheet (without touching what's there), creates the outreach doc, asks you the [setup questions](setup/questions.md), saves your `rules.yaml`, and schedules the nightly draft and morning call.
2. **Set up the Claude checker** as a scheduled task, using the prompt Fo sends you at the end of setup (the template is [`prompts/claude-checker.md`](prompts/claude-checker.md)).
3. **Check your platform adapter** in [`adapters/`](adapters/). Skool, email and hand-send are available; hand-send always works.

## Try it without real data

```sh
pip install -r requirements.txt
python demo/make_demo.py --date 2026-10-18
python scripts/checks.py --rules demo/rules.yaml --data demo/data --date 2026-10-18
python scripts/scorecard.py --rules demo/rules.yaml --data demo/data --date 2026-10-18
```

The demo is a fictional coaching community with three simulated weeks of the loop. Today's drafts include one contacted too recently and one in the hold-back group, so you can see the checks catch them. All demo numbers are simulated.

## Safety rules

These are in [`SKILL.md`](SKILL.md) and can't be switched off:

- Nothing is sent without your approval of that specific message.
- Only people in your sheet are contacted, and no more often than your limit.
- Opted-out, skipped and held-back members are never contacted.
- Guesses are labeled as guesses; missing data counts as unknown, not inactive.
- No guilt, pressure or invented offers.
- Nothing happens inside your community platform: no posts, no DMs, no logging in as you.
- Voice notes are always in Fo's own voice, introduced as your assistant, and played to you before they go out. Your voice is never cloned.
- The agents never change your rules; they propose changes on the call.

We recommend telling your members that you use an assistant to manage outreach.

## Files

| Path | What it is |
| --- | --- |
| `SKILL.md` | The playbook both agents follow, with a section for each role |
| `rules.example.yaml` | Example owner settings |
| `setup/questions.md` | The eight setup questions |
| `prompts/` | Install messages for Fo and the Claude checker |
| `adapters/` | Per-platform read and send instructions |
| `scripts/` | Deterministic checks and the scorecard |
| `templates/` | Sheet tabs and an example outreach doc |
| `demo/` | The demo coaching community Fo can build in your Drive (`coaching-skool/`), and a generator for scripted test data |

## Authors

Sanskriti Bhatnagar and Majid Mohammed. MIT licensed.
