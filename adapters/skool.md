# Adapter: Skool

Skool has no public API, so this adapter relies on two things the owner already has: a sheet that is synced from Skool, and a Fo account that can act in Skool as the owner.

## Read

- Source: the member sheet's Members tab, kept current by the owner's existing nightly sync from Skool.
- Required columns: `member_id`, `name`, `profile_link` (the member's Skool profile URL), `last_active`, `stage`.
- `channel` = `skool` for every member reached this way.

## Send

- Fo opens the member's `profile_link` and sends the approved `final_text` as a **direct message** from the owner's account.
- Never post in the community feed, comment on posts, or message anyone not in the sheet.
- After sending, Fo records `sent_at` in Drafts, adds a Touchpoints row (`direction: out`), and updates `last_contacted`.

## Replies

- When Fo sees a reply in the owner's Skool inbox from a member in the sheet, it adds a Touchpoints row (`direction: in`) and sets `replied` on the original message's row.

## When it can't send

- If the profile link is missing, the DM fails, or Skool access isn't available, Fo sets the draft to `Approved` (not `Sent`) and follows [hand-send](hand-send.md).

## Before using it

- Check Skool's terms for your community on automated messaging.
- Make sure the people you message know you use an assistant to manage outreach.
