# Adapter: email (default channel)

## Access needed

- The owner's email account (for example Gmail) connected to Fo at wajo.ai.
- Read-only test at setup: list the last few messages in the inbox. Send nothing.

## Read

- Members with `channel` = `email` and an `email` address in the sheet.

## Send

The owner chooses a default at setup (`send.default`), and can override it per message on the call:

- **"Send it now"**: Fo sends the approved email straight away, but only if it can send from the owner's account, or the owner opted in to Fo's own address (`send.from: fo`). Otherwise Fo saves it to the owner's drafts and says it's ready to send.
- **"Save it to my drafts"**: Fo creates it as a draft in the owner's email, ready to review or send later. Nothing goes out.

Every email:
- one person per email, from the owner's own address, signed as the owner;
- a short subject that is specific to the person and true to the content;
- plain text, no tracking pixels, no mailing-list tools;
- with a voice note attached when the owner said yes to one and approved the audio (see `SKILL.md`, "Voice notes over email").

**From whom.** By default Fo saves to the owner's drafts and the owner sends, so every email comes from the owner. Fo's own address is used only with `send.from: fo`, chosen at setup. Those emails say they're from Fo, the owner's assistant, and are signed for the owner.

After sending, check that the email is in the owner's Sent folder before calling it sent. The recipient can take a minute or two to see it. Never send again without checking the Sent folder first. Then Fo records `sent_at` in Drafts, adds a Touchpoints row (`direction: out`), and updates `last_contacted`.

## Replies

- Replies in the owner's inbox from a member's address are logged to Touchpoints (`direction: in`) and mentioned on the next call.
