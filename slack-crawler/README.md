# slack-crawler

A Claude Code skill that reads your Slack sidebar sections on demand and produces a dense, scannable intelligence brief covering the last two weeks - with hot callouts for the last 24 hours and 3 days at the top.

Give it a section name. Get a structured brief. Optionally write it to a Slack canvas.

---

## What It Does

Slack lets you group channels into named sidebar sections. This skill reads all the channels in a named section and produces a structured brief:

- **HOT - Last 24 Hours**: Time-sensitive items across all channels, with severity indicators
- **HOT - Last 3 Days**: Notable items from the 24h to 3-day window
- **2-Week Summary by Channel**: 3-7 bullets per channel - dominant themes, decisions, open risks
- **Cross-Channel Themes**: The synthesis layer - what does the combined signal tell you about program health?
- **Coverage Notes**: What was skipped and why (shared channels, inaccessible private channels, channels already covered by cron jobs)

Output goes directly into your Claude Code conversation. You can optionally ask it to write the brief to a Slack canvas.

---

## Why This Exists: The Slack Sections Problem

**Slack sections are invisible to the Slack API.** There's no endpoint that lists your sidebar sections or the channels in them. Sections are a purely client-side UI feature - they exist only inside your Slack app. This means you can't query "what channels are in my _Domain section?" without first building a registry.

The solution is a one-time bootstrap: take screenshots of your Slack sidebar sections, share them with Claude, and Claude resolves all the channel IDs via the Slack API. The result is saved to `slack_sections.md` - a registry file the skill reads at runtime. Once it exists, the skill works entirely via API. The registry only needs updating when your sidebar changes.

Two weeks is the default window because it's long enough to catch decisions and threads that moved slowly, short enough that the output stays actionable rather than encyclopedic.

---

## Repo Contents

```
slack-crawler/
├── README.md              ← You are here
├── SKILL.md               ← The Claude Code skill definition (install this - same for everyone)
├── slack_sections.md      ← Sanitized template registry (reference only - build your own)
└── SETUP.md               ← Step-by-step setup and sharing guide
```

---

## What You Need to Personalize

**`SKILL.md` is the same for everyone.** Install it as-is. No edits required.

**`slack_sections.md` must be built fresh for every person.** The file in this repo is a sanitized template with placeholder channel names and IDs. It won't work as-is because your Slack sidebar sections have different names, different channels, and your private channel memberships are your own.

---

## Quick Start

### Step 1 - Install the Skill

```bash
mkdir -p ~/.claude/skills/slack-crawler && \
cp SKILL.md ~/.claude/skills/slack-crawler/SKILL.md
```

Claude Code picks up skills from `~/.claude/skills/` automatically. No restart needed.

---

### Step 2 - Build Your Registry

This is the setup step unique to you. It takes 5-10 minutes and only needs to be done once.

For each Slack sidebar section you want to cover:

1. Open Slack and find the section. Make sure all channels in the section are visible.
2. Take a screenshot of the full channel list. If the section is long, scroll to capture everything.
3. In Claude Code, share the screenshot and say:
   ```
   Add the `_SectionName` section to slack_sections.md
   ```
4. Claude reads the channel names, resolves each ID via `slack_search_channels`, flags anything it can't resolve, skips DMs, and appends the completed table to `~/.claude/skills/slack-crawler/slack_sections.md`.
5. Repeat for each section you want to cover.

**On shared/external channels:** Channels with an "External" badge are cross-workspace shared channels. The Slack API cannot find them by name. If you need to include one, get the ID manually: open the channel, click the channel name, "Copy link" - the ID is the `CXXXXXXXXX` part of the URL.

---

### Step 3 - Run It

```
/slack-crawler <section-name> [--canvas <canvas-id|new>]
```

```
/slack-crawler _Domain                        ← brief in conversation
/slack-crawler STPM --canvas new              ← brief + creates a new canvas, returns ID
/slack-crawler Engineering --canvas F0ABC123  ← brief + replaces that canvas
/slack-crawler                                ← lists your available sections
```

Section names are case-insensitive. Leading underscores are ignored: `_Domain` and `Domain` match the same section.

---

## Registry File Lookup

The skill searches these paths in order and uses the first file it finds:

1. `~/.claude/skills/slack-crawler/slack_sections.md` - recommended, right next to the skill
2. `./slack_sections.md` - current working directory when Claude Code launched
3. `~/slack_sections.md` - home directory

---

## Output Format

```
# [Section Name] - Slack Crawler Brief
> Period: Last 14 days | As of: [date/time]
> Channels: [N readable] of [N total]
> Overall: GREEN / YELLOW / RED - one-sentence rationale

## HOT - Last 24 Hours
- [CRITICAL] specific event - person, #channel, timestamp
- [RISK] specific event
- [NOTABLE] specific event

## HOT - Last 3 Days
- [same format, 24h-3d window only, no repeats from above]

## 2-Week Summary by Channel

### #channel-name
**[N messages in 14 days]**
- Dominant theme or decision
- Recurring issue or open risk

## Cross-Channel Themes
- Pattern or risk that spans multiple channels

## Coverage Notes
- #channel-name - Shared/external channel, skipped
- #channel-name - Not accessible
- #channel-name - Already covered by my_cron.sh
```

---

## Maintenance

| Situation | Action |
|-----------|--------|
| Joined a new channel and added it to a section | Add a row to that section's table in `slack_sections.md` |
| Created a new sidebar section | Screenshot it and say "Add the `_NewSection` section to `slack_sections.md`" |
| A channel was renamed | Update the name in the table (the ID does not change) |
| A channel was archived | Remove the row or add "Archived" to the Notes column |
| A private channel became inaccessible | The skill flags it - remove from registry or rejoin |

---

## Extending This Pattern

**Keep a standing canvas for a section** - Run with `--canvas new` once to create it, note the canvas ID, then use `--canvas F0XXXXXXX` on every subsequent run to refresh it in place.

**Build a cron script for a section** - After running a brief, say "build a cron for [section-name]". Claude generates a bash cron script and canvas update prompt.

**Deep dive one channel** - Say "deep dive on #channel-name". Claude re-reads with a higher message limit and produces a thread-by-thread breakdown.

**Generate a status report from the canvas** - Use the [Slack Canvas Status Synthesis](../slack-canvas-status-synthesis/) tool in this repo. The crawler does the weekly intelligence work; the synthesis tool does the assembly when you need to report.

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Claude Code CLI | Installed and authenticated - run `claude --version` to verify |
| Slack MCP plugin | Configured in Claude Code - the skill calls `slack_read_channel` internally |
| Channel membership | You must be a member of any private channels you want the skill to read |
| `slack_sections.md` | Must exist at one of the 3 lookup paths - see Step 2 |

---

## Origin

This tool grew out of earlier work in [SlackSummarization](https://github.com/ChefPlex/SlackSummarization), which was built for a specific internal program environment. The crawler is the generalized version - same core idea, configurable registry, no hardcoded organizational context.

---

*Part of the [tpm-toolbox](https://github.com/ChefPlex/tpm-toolbox). Built by [Eric White](https://github.com/ChefPlex) | Version 2.0.0*
