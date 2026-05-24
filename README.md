# tpm-toolbox

Practical tools for Technical Program Managers - templates, trackers, and scripts built from real program work. The goal is to spend less time building infrastructure and more time running programs.

Everything here is ready to use or adapt. Nothing requires a specific toolchain or corporate system. If it needs a dependency, it is documented.

---

## What Is Here

### Trackers and Templates

| Tool | What It Is |
|------|-----------|
| [RAID Log Template](raid-log-template.xlsx) | A clean, ready-to-use Excel RAID log with tabs for Risks, Assumptions, Issues, and Dependencies. Color-coded, auto-calculating, zero setup required. See the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) in tpm-templates for how to use it effectively. |
| [Program Kickoff Checklist](program-kickoff-checklist.md) | Pre-kickoff checklist, recommended agenda with timing, section-by-section facilitation guide, and post-kickoff follow-up checklist. |
| [Meeting Notes + Action Item Tracker](meeting-notes-action-tracker.md) | Template for capturing decisions, actions, open questions, and risks in a meeting. Includes a running tracker for recurring meetings. |

### Scripts and Automation

| Tool | What It Is |
|------|-----------|
| [Slack Canvas Status Synthesis](slack-canvas-status-synthesis/) | Two-script workflow that reads a Slack canvas to extract a reusable status template, then uses that template to generate a draft status report from your Slack channels and canvases. Claude does the reading and drafting; the wrapper handles local files. Draft output only - review before posting. |

---

## What Is Coming

- Program status report template
- Program health dashboard

---

## How This Fits Together

The tools here are designed to work alongside the templates in [tpm-templates](https://github.com/ChefPlex/tpm-templates). The RAID log here is the working file - the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) explains how to run it. The status report template here feeds the communications cadence defined in the [Communications Plan template](https://github.com/ChefPlex/tpm-templates/blob/main/communications-plan-template.md). The canvas synthesis tool produces drafts in whatever format your existing status canvas already uses.

They are separate repos because templates and tools serve different purposes - but they are designed to be used together.

---

## Contributing

If you have a tool, script, or template that saves TPMs real time - open a PR or file an issue describing it. The bar: it has to work, it has to be generic enough to apply outside one company or team, and it has to be documented well enough that someone can pick it up without asking you questions.

---

## Final Note

The goal here is boring tools that get used. A messy tracker reviewed every week beats a perfect one nobody opens.

---

*Built from experience running platform security, infrastructure, and compliance programs at enterprise scale. Maintained by [Eric White](https://www.linkedin.com/in/edwhite) | [ChefPlex](https://github.com/ChefPlex)*
