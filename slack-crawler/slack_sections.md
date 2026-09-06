# Slack Sections - Channel Registry

This file maps your Slack sidebar sections to channel IDs for use with `/slack-crawler`.
It's the authoritative source when running the skill or building canvas cron scripts.

**How to use in a cron script:**
- Copy the channel IDs from the section you want to monitor
- Use `slack_read_channel` (not `slack_search_public`) with `limit=50` and `response_format=concise`
- Batch reads to avoid rate limits (2-3 channels per batch)
- Private channels (🔒) are accessible via API if you're a member
- Shared/external channels (🔗) are NOT indexed by the Slack API - IDs unresolvable via search

DMs and group DMs are excluded from this registry. They are not channels.

**Author:** Your Name (you@yourcompany.com)
**Last updated:** YYYY-MM-DD
**Sections documented:** `_SectionA`, `SectionB`, `_SectionC`

---

## Section: `_SectionA`

What this section covers - a program, team, or workstream.
All channels in this section are already monitored by `section_a_cron.sh`.

| Channel | ID | Type | Notes |
|---|---|---|---|
| #slack-channel-1 | C0000000001 | 🔒 Private | Primary status channel. Also in `section_a_cron.sh`. |
| #slack-channel-2 | C0000000002 | 🔒 Private | Working group channel. Also in `section_a_cron.sh`. |
| #slack-channel-3 | C0000000003 | 🌐 Public | Escalation/support channel. Also in `section_a_cron.sh`. |

**Total channels:** 3 (3 resolved) - fully covered by `section_a_cron.sh` → canvas `F0000000001`

---

## Section: `SectionB`

What this section covers - tools, learning, or announcements.

| Channel | ID | Type | Notes |
|---|---|---|---|
| #slack-channel-4 | C0000000004 | 🌐 Public | Company-wide broadcast or learning channel. |
| #slack-channel-5 | C0000000005 | 🔒 Private | Team-specific private channel. |
| #slack-channel-6 | C0000000006 | 🌐 Public | Pilot or feedback channel. |
| #slack-channel-7 | C0000000007 | 🔒 Private | Reporting or analytics channel. |

**Total channels:** 4 (4 resolved)

---

## Section: `_SectionC`

What this section covers - operations, release planning, or governance.

| Channel | ID | Type | Notes |
|---|---|---|---|
| #slack-channel-8  | C0000000008 | 🔒 Private | Release planning coordination. |
| #slack-channel-9  | C0000000009 | 🌐 Public | Status updates. |
| #slack-channel-10 | C0000000010 | 🌐 Public | Help/support channel with office hours. |
| #slack-channel-11 | ⚠️ UNKNOWN | 🔗 Shared/External | External badge - shared vendor channel. Not indexed by Slack API. |

**Total channels:** 4 (3 resolved, 1 unresolved - `#slack-channel-11` is a shared/external channel)

---

## Cross-Section Overlap (Existing Cron Coverage)

Channels already covered by active cron scripts. The skill flags these in Coverage Notes
so you know the coverage exists elsewhere. Avoid duplicating unless cross-section context
is specifically what you need.

| Channel | ID | Covered By |
|---|---|---|
| #slack-channel-1 | C0000000001 | `section_a_cron.sh` |
| #slack-channel-2 | C0000000002 | `section_a_cron.sh` |
| #slack-channel-3 | C0000000003 | `section_a_cron.sh` |

---

## Adding a New Section

Take a screenshot of the section in your Slack sidebar and say:
> "Add the `_SECTIONNAME` section to `slack_sections.md`"

Claude will resolve all channel IDs via `slack_search_channels` and append the table.
DMs and group DMs are always excluded.

**Notes on unresolvable channels:**
- 🔗 **Shared/External** channels - cross-workspace shared channels. The Slack API cannot find them by name. Retrieve the ID manually: open the channel → click the channel name → "Copy link" → the ID is the `CXXXXXXXXX` portion of the URL.
- Bold channel names in the sidebar mean unread messages, not a different channel type.
