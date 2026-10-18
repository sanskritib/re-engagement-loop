# Adapter: Skool (read only)

Skool is a **source**, not a channel. Its community rules ask members not to use bots or automation to post, comment or message others, so this skill never acts inside Skool: no posts, no DMs, no logging in as the owner.

## Access needed

- None inside Skool. The owner exports the member list (Skool admins can download it as a CSV) and keeps it in the member sheet, by hand or with their existing sync.

## Read

- Source: the member sheet's Members tab, filled from the export.
- Useful columns: `name`, `email`, `joined`, `last_active`, `posts`, `intro_posted`, `plan_value`, `renewal_date`.
- Missing columns are unknown, not zero. A member with no `posts` value is never treated as "never posted".

## Reach

- Through [email](email.md) from the owner's own account, using the email address in the export. Set `channel` = `email` for those members.
