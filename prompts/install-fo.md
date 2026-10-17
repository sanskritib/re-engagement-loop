# Install: Fo

Send the message below to your Fo once (chat, email or any MCP client connected to your Wajo account). You need either your member sheet in Google Drive, or nothing at all if you want to try it with the demo data first. Fo prepares everything else in your own Drive: the sheet (for the demo), the extra tabs, the outreach doc, your rules file and the schedule.

If Fo already runs an earlier version of this loop for you, the message tells it to update those scheduled jobs instead of adding new ones. Fo reads its plan back to you before saving anything; say yes only if it matches.

---

```
Please install the re-engagement loop for me (or update it, if you already run a version of this).

Follow https://github.com/sanskritib/re-engagement-loop/blob/main/SKILL.md
Treat it as the source of truth: the "Rules for everyone" section and the "Fo" section, starting with Step 0 (Setup).

My member sheet: <Google Sheet link>  (or write: use the demo data)

During setup:
- Add the loop's tabs and columns to my sheet without changing anything that's already there.
- Create the outreach doc in the same folder.
- Ask me the setup questions and save my answers as rules.yaml next to the sheet.
- Schedule the nightly draft and the morning call, and read the plan back to me before saving it.
- Send me the prompt for the Claude checker with my links filled in.

Never send a member message unless I have approved that specific message.
```

---

## Check it worked

- Your sheet has the new tabs, and your original tabs and formulas are unchanged.
- There's an outreach doc and a `rules.yaml` next to the sheet.
- Ask Fo: "List my scheduled jobs for the re-engagement loop." You should see exactly two.
- After the first night, the Run log tab has a `draft` row; after the first morning, a `review` row with `review_minutes=` in the note.
