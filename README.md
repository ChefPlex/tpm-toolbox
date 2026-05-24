# tpm-toolbox

Practical tools for Technical Program Managers - templates, trackers, scripts, and AI-assisted workflows built from real program work.

The goal is simple: spend less time rebuilding the same operating machinery and more time running the program. These tools are deliberately lightweight. If a tool needs a dependency or has a real failure mode, it should say so up front.

---

## What Is Here

### Trackers and Templates

| Tool | What It Is |
|------|------------|
| [RAID Log Template](raid-log-template.xlsx) | A clean, ready-to-use Excel RAID log with tabs for Risks, Assumptions, Issues, and Dependencies. Color-coded, auto-calculating, zero setup required. See the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) in `tpm-templates` for how to use it effectively. |
| [Program Kickoff Checklist](program-kickoff-checklist.md) | Pre-kickoff checklist, recommended agenda with timing, section-by-section facilitation guide, and post-kickoff follow-up checklist. |
| [Meeting Notes + Action Item Tracker](meeting-notes-action-tracker.md) | Template for capturing decisions, actions, open questions, and risks in a meeting. Includes a running tracker for recurring meetings. |

### Scripts and Automation

| Tool | What It Is |
|------|------------|
| [Slack Canvas Status Synthesis](slack-canvas-status-synthesis/) | AI-assisted workflow for turning Slack channels and canvases into draft status reports using a learned template. Useful for weekly status, executive briefs, and cross-program rollups. Human review required before posting. |

---

## AI Boundary

The automation here is meant to remove the copy/paste tax, not replace judgment.

For status reporting in particular, the tool can draft the report, preserve a format, and pull signal from messy source material. The TPM still owns the truth: dates, owners, metrics, risk level, decision asks, and whether the report is useful enough to send.

A polished draft that hides the real risk is worse than a rough update that tells the truth.

---

## What Is Coming

### Trackers and Templates

| Tool | What It Will Be |
|------|-----------------|
| Program Status Report Template | Structured weekly status report in Excel or Markdown - Red / Yellow / Green, this week, next two weeks, decisions needed, risks flagged. Copy and fill in. |
| Stakeholder Map Template | A simple way to map stakeholders by influence, interest, and engagement level at the start of a program. |

### Scripts and Automation

| Tool | What It Will Be |
|------|-----------------|
| CSV to Status Report | Takes a CSV export from a project tracker and formats it into a clean status summary. Useful when the tooling changes but the reporting cadence does not. |
| Meeting Recap Generator | Expansion of the Slack Canvas Status Synthesis workflow to handle raw meeting notes, decisions, action items, and follow-up owners. |
| Program Health Dashboard | Lightweight script that reads a RAID log and produces a one-page health summary - open risks by category, issues trending, dependencies at risk. |

---

## How This Fits Together

The tools here are designed to work alongside the templates in [`tpm-templates`](https://github.com/ChefPlex/tpm-templates). The RAID log here is the working file. The [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) explains how to run it. The status reporting tools here feed the communications cadence defined in the [Communications Plan template](https://github.com/ChefPlex/tpm-templates/blob/main/communications-plan-template.md).

They are separate repos because templates and tools serve different purposes, but they are designed to be used together.

---

## Contributing

If you have a tool, script, or template that saves TPMs real time, open a PR or file an issue describing it.

The bar is simple: it has to work, it has to be generic enough to apply outside one company or team, and it has to be documented well enough that someone can pick it up without asking you questions.

---

## A Note on Tooling Philosophy

The best TPM tool is the one your team will actually use. A perfectly formatted tracker that nobody updates is worse than a messy one that gets checked every week.

Everything here is deliberately lightweight. If setup is harder than the work the tool saves, the tool is probably not done yet.

---

Built from experience running platform security, infrastructure, and compliance programs at enterprise scale. Maintained by [Eric White](https://www.linkedin.com/in/edwhite) | [ChefPlex](https://github.com/ChefPlex)
