# Setup Guide - `/slack-crawler`

Two files. No code to compile, no dependencies beyond Claude Code and the Slack MCP plugin.

| File | Purpose | Install Location |
|---|---|---|
| `SKILL.md` | The skill definition - Claude reads this to run `/slack-crawler` | `~/.claude/skills/slack-crawler/SKILL.md` |
| `slack_sections.md` | Your personal channel registry - maps section names to channel IDs | `~/.claude/skills/slack-crawler/slack_sections.md` |

---

## Prerequisites

| Requirement | How to Check |
|---|---|
| Claude Code CLI | Run `claude --version` - should return a version number |
| Slack MCP plugin | In Claude Code, run `/slack-crawler` - if it says "Slack tools not available", the plugin is not configured |
| Channel membership | You must be a member of any private 🔒 channels you want the skill to read |

---

## Step 1: Install the Skill

```bash
mkdir -p ~/.claude/skills/slack-crawler
cp SKILL.md ~/.claude/skills/slack-crawler/SKILL.md
```

Claude Code picks up skills from `~/.claude/skills/` automatically. No restart, no config change. The skill appears as `/slack-crawler` in your next session.

---

## Step 2: Build Your Channel Registry

You cannot use someone else's `slack_sections.md` directly. It reflects their Slack sidebar - their sections, their channels, their private channel memberships. Your sidebar is different.

This isn't a limitation - it's the nature of Slack sections. They are a purely client-side UI feature. There is no Slack API endpoint that exposes them. The registry must be bootstrapped manually from screenshots of your own sidebar, then maintained as your sections change.

### How to Bootstrap

For each Slack sidebar section you want to cover:

1. Open Slack and navigate to the section. Make sure all channels are visible - scroll if the section is long.

2. Take a screenshot that shows the complete channel list for that section.

3. In Claude Code, share the screenshot and say:
   ```
   Add the `_SectionName` section to slack_sections.md
   ```

   Claude will read the channel names, call `slack_search_channels` for each one, flag anything it can't resolve, skip DMs and group DMs, and append the completed section table to `~/.claude/skills/slack-crawler/slack_sections.md` - creating the file if it doesn't already exist.

4. Repeat for each section you want to cover.

### What to Expect During ID Resolution

| Situation | What Claude Does | What You See in the Registry |
|---|---|---|
| Shared/external channel | Marks as unresolvable - search API cannot index cross-workspace channels | `⚠️ UNKNOWN` in ID column, 🔗 in Type column |
| Private channel with unusual name | May not resolve if search cannot find it | Claude flags it - provide the ID manually |
| DMs / group DMs | Skipped entirely | Noted in the section footer |

### Handling Shared/External Channels

Channels with an "External" badge are cross-workspace shared channels. The Slack search API cannot find them by name. The skill skips them automatically and notes them in Coverage Notes.

To include one: open the channel in Slack → click the channel name → "Copy link" → the ID is the `CXXXXXXXXX` part of the URL → edit `slack_sections.md` and replace `⚠️ UNKNOWN` with the real ID.

### A Complete Example

```markdown
# Slack Sections — Channel Registry

**Author:** Your Name (you@yourcompany.com)
**Last updated:** 2026-05-24
**Sections documented:** `_Engineering`, `STPM`

---

## Section: `_Engineering`

Core engineering program channels.

| Channel | ID | Type | Notes |
|---|---|---|---|
| #eng-standup       | C0123456789 | 🌐 Public  | Daily standup coordination  |
| #eng-incidents     | C0234567890 | 🔒 Private | P0/P1 incident response     |
| #eng-vendor-collab | ⚠️ UNKNOWN  | 🔗 Shared/External | External badge - not API-readable |

**Total channels:** 3 (2 resolved, 1 unresolved)

---

## Section: `STPM`

Security TPM team coordination.

| Channel | ID | Type | Notes |
|---|---|---|---|
| #sec-tpm-team  | C0345678901 | 🔒 Private | Team collaboration  |
| #tpm-community | C0456789012 | 🌐 Public  | Best practices and learning |

**Total channels:** 2 (2 resolved)
```

---

## Step 3: Run the Skill

```
/slack-crawler <section-name> [--canvas <canvas-id|new>]
```

```
/slack-crawler _Domain                        ← brief in conversation only
/slack-crawler STPM --canvas new              ← brief + new canvas, returns canvas ID
/slack-crawler Engineering --canvas F0ABC123  ← brief + replaces that canvas
/slack-crawler                                ← lists your available sections
```

**Matching rules:**
- Case-insensitive: `stpm`, `STPM`, `Stpm` all work
- Leading underscores ignored: `_Domain` and `Domain` match the same section

---

## Registry File Lookup

The skill searches these paths in order and uses the first file it finds:

1. `~/.claude/skills/slack-crawler/slack_sections.md` - default and recommended
2. `./slack_sections.md` - current working directory when Claude Code launched
3. `~/slack_sections.md` - home directory

---

## Maintaining Your Registry

| Situation | What to Do |
|---|---|
| Joined a new channel and added it to a section | Add a row to the section table |
| Created a new Slack sidebar section | Screenshot it → "Add the `_NewSection` section to `slack_sections.md`" |
| A channel was renamed | Update the name (the ID stays the same) |
| A channel was archived | Remove the row or add "Archived" to Notes |
| A private channel became inaccessible | Skill flags it - remove from registry or rejoin |
| A new cron script now covers some channels | Add them to the Cross-Section Overlap table |

The registry does not auto-update. In practice, sections change infrequently, so this is a low-overhead file.

---

## Sharing With a Colleague

**What to share:**
- `SKILL.md` - identical install, works for any user, no edits needed

**What they must build themselves:**
- `slack_sections.md` - must reflect their own Slack sidebar, their own sections, their own channel memberships

Send them this repo link and point them to Step 2.

---

## Quick Reference Card

```
/slack-crawler — Setup Checklist

□ 1. Install skill:
      mkdir -p ~/.claude/skills/slack-crawler
      cp SKILL.md ~/.claude/skills/slack-crawler/SKILL.md

□ 2. Build registry (one-time, 5-10 minutes):
      - Screenshot each Slack sidebar section
      - Tell Claude: "Add the _SectionName section to slack_sections.md"
      - Claude resolves all channel IDs from your screenshots
      - File saved to ~/.claude/skills/slack-crawler/slack_sections.md

□ 3. Run:
      /slack-crawler <section-name>
        → brief in conversation (last 14 days)

      /slack-crawler <section-name> --canvas new
        → brief + creates a new Slack canvas, returns canvas ID

      /slack-crawler <section-name> --canvas F0XXXXXXX
        → brief + replaces content of that canvas

WHY you need your own slack_sections.md:
  Slack sections = client-side only. No API exposes them.
  Your layout is not anyone else's layout.
  Private channel access is per-user.
```
