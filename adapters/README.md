# Adapters

An adapter tells Fo two things for one platform: **where member data comes from** and **how an approved message is sent**. The skill and the owner's rules don't change between platforms; only the adapter does.

| Adapter | Read members from | Send through | Status |
| --- | --- | --- | --- |
| [skool](skool.md) | The member sheet, kept current by the owner's nightly sync | Fo, using the owner's existing Skool access, as a direct message | In use with our first tester |
| [email](email.md) | The member sheet (`contact` = email address) | Fo sends email from the owner's account | Fo reports it can do this; not yet tested in this loop |
| [hand-send](hand-send.md) | Any | The owner, from the text and link Fo provides | Always available; the fallback for every adapter |
| slack | Workspace member list exported to the sheet | Slack DM | Not built yet |
| discord | Server member list exported to the sheet | Discord DM | Not built yet |

To add one, copy `skool.md`, keep the same headings, and open a pull request. An adapter must never post publicly and must fall back to hand-send when it can't send.
