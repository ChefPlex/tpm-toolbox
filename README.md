# tpm-toolbox

Practical tools for Technical Program Managers - templates, trackers, and scripts built from real program work. The goal is to spend less time building infrastructure and more time running programs.

Everything here is ready to use or adapt. Nothing requires a specific tool chain or corporate system. If it needs a dependency, it is documented.

---

## What Is Here

### Trackers and Templates

| Tool | What It Is |
|------|-----------|
| [RAID Log Template](raid-log-template.xlsx) | A clean, ready-to-use Excel RAID log with tabs for Risks, Assumptions, Issues, and Dependencies. Color-coded, auto-calculating, zero setup required. See the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) in tpm-templates for how to use it effectively. |
| [Program Kickoff Checklist](program-kickoff-checklist.md) | Pre-kickoff checklist, recommended agenda with timing, section-by-section facilitation guide, and post-kickoff follow-up checklist. |
| [Meeting Notes + Action Item Tracker](meeting-notes-action-tracker.md) | Template for capturing decisions, actions, open questions, and risks in a meeting. Includes a running tracker for recurring meetings. |

---

## What Is Coming

### Trackers and Templates

| Tool | What It Will Be |
|------|----------------|
| Program Status Report Template | Structured weekly status report in Excel - Red / Yellow / Green, this week, next two weeks, decisions needed, risks flagged. Copy and fill in. |
| Stakeholder Map Template | A structured way to map stakeholders by influence, interest, and engagement level at the start of a program. |

### Scripts and Automation

| Tool | What It Will Be |
|------|----------------|
| Jira Status Puller | Python script to pull open issues, epics, and blockers from a Jira project and format them for a status report. No more copying and pasting from Jira into a doc. |
| CSV to Status Report | Takes a CSV export from any project tracker and formats it into a clean status summary. Useful when your tooling changes but your reporting cadence does not. |
| Meeting Recap Generator | Prompt template and lightweight script for turning raw meeting notes into a structured recap with decisions, action items, and owners. |
| Program Health Dashboard | A simple Python script that reads a RAID log and produces a one-page health summary - open risks by category, issues trending, dependencies at risk. |

---

## How This Fits Together

The tools here are designed to work alongside the templates in [tpm-templates](https://github.com/ChefPlex/tpm-templates). The RAID log here is the working file - the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) explains how to run it. The status report template here feeds the communications cadence defined in the [Communications Plan template](https://github.com/ChefPlex/tpm-templates/blob/main/communications-plan-template.md).

They are separate repos because templates and tools serve different purposes - but they are designed to be used together.

---

## Contributing

If you have a tool, script, or template that saves TPMs real time - open a PR or file an issue describing it. The bar is simple: it has to work, it has to be generic enough to apply outside one company or team, and it has to be documented well enough that someone can pick it up without asking you questions.

---

## A Note on Tooling Philosophy

The best TPM tool is the one your team will actually use. A perfectly formatted tracker that nobody updates is worse than a messy one that gets checked every week.

Everything here is deliberately lightweight. If it requires more than five minutes of setup, it probably does not belong here.

---

*Built from experience running platform security, infrastructure, and compliance programs at enterprise scale. Maintained by [Eric White](https://www.linkedin.com/in/edwhite) | [ChefPlex](https://github.com/ChefPlex)*
