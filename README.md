# tpm-toolbox

Practical tools for Technical Program Managers: templates, trackers, and scripts built from real program work.

The goal is to spend less time building infrastructure and more time running programs.

Everything here is ready to use or adapt. Nothing requires a specific corporate system. If it needs a dependency, it is documented.

## What Is Here

### Trackers and Templates

| Tool | What It Is |
|---|---|
| [RAID Log Template](raid-log-template.xlsx) | A clean, ready-to-use Excel RAID log with tabs for Risks, Assumptions, Issues, and Dependencies. Color-coded, auto-calculating, zero setup required. See the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) in `tpm-templates` for how to use it effectively. |
| [Program Kickoff Checklist](program-kickoff-checklist.md) | Pre-kickoff checklist, recommended agenda with timing, section-by-section facilitation guide, and post-kickoff follow-up checklist. |
| [Meeting Notes + Action Item Tracker](meeting-notes-action-tracker.md) | Template for capturing decisions, actions, open questions, and risks in a meeting. Includes a running tracker for recurring meetings. |

### Scripts and Automation

| Tool | What It Is |
|---|---|
| [Slack Crawler](slack-crawler/) | Claude Code skill that reads all channels in a named Slack sidebar section and produces a structured two-week intelligence brief, with hot callouts for the last 24 hours and three days at the top. Runs on demand. Optionally writes the brief to a Slack canvas. |
| [Slack Canvas Status Synthesis](slack-canvas-status-synthesis/) | Two-script workflow that reads a Slack canvas to extract a reusable status template, then uses that template to generate a draft status report from Slack channels and canvases. Draft output only. Review before posting. |

## Maturity

| Tool | Status | Notes |
|---|---|---|
| Program Kickoff Checklist | Ready | Lightweight and usable. Good for getting scope, stakeholders, risks, dependencies, and operating rhythm aligned before kickoff. |
| Meeting Notes + Action Item Tracker | Ready | Useful for recurring execution hygiene and follow-through. |
| RAID Log Template | Ready | Good base tracker. Pair it with the RAID Log Guide in `tpm-templates`. |
| Slack Crawler | Working | Strong signal-gathering workflow. Requires Claude Code and Slack MCP setup. |
| Slack Canvas Status Synthesis | Working | Strong draft-generation workflow. Requires review before publishing. |
| Program Health Dashboard | Planned | Do not describe as available until it exists. |

## The Two-Step Status Workflow

The two Slack tools are designed to work together.

Run them in sequence to go from raw channel noise to a polished draft status report.

### Step 1: Run Slack Crawler once or twice a week

```text
/slack-crawler <section-name> --canvas new        # first run, creates the canvas
/slack-crawler <section-name> --canvas F0XXXXXXX  # subsequent runs, updates in place
```

The crawler reads all channels in a named sidebar section and produces a structured brief covering the last 14 days. It writes the brief to a canvas and keeps updating that same canvas each time you run it.

By the time you need to write a status report, you have a current, organized picture of what happened across all your channels, not your memory of it.

### Step 2: Run Slack Canvas Status Synthesis to draft the report

```text
./canvas_generator_from_template.py
```

The synthesis tool reads your program channels and the canvas the crawler just updated, applies a template extracted from one of your existing status canvases, and produces a draft in your usual format.

It is not going to be perfect.

It will get you most of the way there: the structure, the populated sections, the signal pulled from Slack, and the first draft of the report. You still own the final call.

### Why this works

The crawler does the ongoing intelligence work throughout the week.

The synthesis tool does the assembly work when you need to report.

Keeping them separate means you can run the crawler on whatever cadence makes sense for your program without tying it to your reporting schedule.

## How This Fits Together

These tools are designed to work alongside the templates in [tpm-templates](https://github.com/ChefPlex/tpm-templates).

The RAID log here is the working file. The [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) explains how to run it.

The status synthesis tool produces drafts in whatever format your existing status canvas already uses, which means it works with the reporting structure in [program-reporting-frameworks](https://github.com/ChefPlex/program-reporting-frameworks).

They are separate repos because templates and tools serve different purposes, but they are designed to be used together.

## Where This Breaks

These tools break when they are treated as the source of truth.

A crawler can collect signal. It cannot know whether a Slack message is confirmed, political, stale, or already superseded.

A status synthesis tool can draft. It cannot decide whether the program is Green, Yellow, or Red. It cannot own the risk call. It cannot make the escalation decision.

Use the tools to reduce mechanical work. Do not use them to avoid judgment.

## Safety and Data Handling

Before using any automation with real program data:

- Confirm the tool is approved for the data you are using.
- Do not paste secrets, credentials, private keys, customer-sensitive data, restricted incident details, unreleased roadmap commitments, or regulated personal data into unapproved tools.
- Sanitize inputs when possible.
- Review all generated drafts before sharing.
- Keep the system of record updated after the draft is finalized.

A polished draft is not the system of record.

## What Is Coming

- Program status report template
- Program health dashboard

## Contributing

If you have a tool, script, or template that saves TPMs real time, open a PR or file an issue describing it.

The bar:

- It has to work.
- It has to be generic enough to apply outside one company or team.
- It has to be documented well enough that someone can pick it up without asking you questions.
- It has to make the work clearer, safer, faster, or less fragile.

## Final Note

The goal here is boring tools that get used.

A messy tracker reviewed every week beats a perfect one nobody opens.

Built from experience running platform security, infrastructure, and compliance programs at enterprise scale.

Maintained by [Eric White](https://github.com/ChefPlex).
