# Adapter: email (default channel)

## Access needed

- The owner's email account (for example Gmail) connected to Fo at wajo.ai.
- Read-only test at setup: list the last few messages in the inbox. Send nothing.

## Read

- Members with `channel` = `email` and an `email` address in the sheet.

## Send

The owner chooses a default at setup (`send.default`), and can override it per message on the call:

- **"Send it now"**: Fo sends the approved email from the owner's account straight away.
- **"Save it to my drafts"**: Fo creates it as a draft in the owner's email, ready to review or send later. Nothing goes out.

Every email:
- one person per email, from the owner's own address, signed as the owner;
- a short subject that is specific to the person and true to the content;
- plain text, no tracking pixels, no mailing-list tools;
- with a voice note attached when the owner said yes to one and approved the audio (see `SKILL.md`, "Voice notes over email").

After sending, Fo records `sent_at` in Drafts, adds a Touchpoints row (`direction: out`), and updates `last_contacted`.

## Replies

- Replies in the owner's inbox from a member's address are logged to Touchpoints (`direction: in`) and mentioned on the next call.
