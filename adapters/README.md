# Adapters

An adapter tells Fo two things for one platform: **where member data comes from** and **how an approved message is sent**. The skill and the owner's rules don't change between platforms; only the adapter does.

| Adapter | Role | Status |
| --- | --- | --- |
| [email](email.md) | **Channel**: send now or save to drafts, from the owner's account; optional voice note | Default |
| [skool](skool.md) | **Source only**: the member export. Nothing is sent inside Skool | In use with our first tester |
| [hand-send](hand-send.md) | Channel: the owner sends it themselves | Always available |
| none | Draft and review only, never sent | For demo rows and dry runs |
| slack, discord, circle | Source (export) or channel (with an app the admin installs) | Not built yet |

Sources say where members are read from; channels say how they're reached. Keep them separate: a platform whose rules forbid automation can still be a source.

To add one, copy `email.md` (for a channel) or `skool.md` (for a source), keep the same headings, and open a pull request. An adapter must never post publicly and must fall back to hand-send when it can't send.
