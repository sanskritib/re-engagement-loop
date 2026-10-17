# Adapter: email

## Read

- Source: the member sheet's Members tab, with `channel` = `email` and `contact` = the member's email address.

## Send

- Fo sends the approved `final_text` from the owner's connected email account, one email per member, with a short plain subject line (for example "Checking in").
- No attachments, no tracking pixels, no mailing-list tools.
- After sending, Fo records `sent_at`, adds a Touchpoints row, and updates `last_contacted`.

## Replies

- Replies in the owner's inbox from a member's address are logged to Touchpoints (`direction: in`).

## When it can't send

- Follow [hand-send](hand-send.md).
