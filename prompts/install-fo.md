# Install: Fo

Send the message below to your Fo once (chat, email or any MCP client connected to your Wajo account). Replace the parts in angle brackets first. If Fo already runs an earlier version of this loop for you, the message tells it to update those scheduled jobs instead of adding new ones.

Fo will ask you to confirm before it changes anything. Read its summary back and say yes only if it matches.

---

```
Please set up (or update, if you already run a version of this for me) my re-engagement loop.

Instructions: follow the "Rules for everyone" and "Fo" sections of
https://github.com/<owner>/re-engagement-loop/blob/main/SKILL.md
Treat that file as the source of truth. If anything I say below conflicts with it, ask me.

My files:
- Member sheet: <Google Sheet link>
- Outreach doc: <Google Doc link>
- My rules: <link to my rules.yaml>

Create two recurring scheduled jobs in my time zone (<time zone>):

1. Every night at <02:00>: run Step 1 (Draft). Read my rules and the Editor's Notes first.
   Write drafts into the outreach doc and the Drafts tab. Do not send anything.

2. Every morning at <08:00>: run Step 3 (Review and send). Call me at <phone>.
   If I don't answer after 2 tries, email <email> and text <phone> a short summary and send nothing to members that day.
   Send a member message only after I approve that specific message on the call or in the doc.
   Send through my <Skool> access as direct messages only, never public posts.

Log every run in the Run log tab, including runs with nothing to do.

Before you save the jobs, read back to me: the two times, what each job does, the phone number and email,
and the sentence "I will not send any member message without your approval of that message."
```

---

## Check it worked

- Ask Fo: "List my scheduled jobs for the re-engagement loop." You should see exactly two.
- After the first night, the Run log tab has a `draft` row and the outreach doc has today's drafts (or says there were none).
- After the first morning, the Run log has a `review` row with `review_minutes=` in the note.
