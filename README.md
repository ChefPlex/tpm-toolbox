# tpm-toolbox

Working tools with code for Technical Program Managers, built from real program work.

The goal is to spend less time on the mechanical parts of program management and more time on the judgment parts.

**This repo is the things that run.** The documents a program produces - charters, the kickoff
checklist, the RAID log template and guide, meeting notes, RACI matrices, close-out reports - are in
[tpm-templates](https://github.com/ChefPlex/tpm-templates).

**Both Slack tools need setup**: they require Claude Code and a working Slack MCP connection, which
most people will not have. Better to say that here than three clicks in.

---

## What Is Here

### Scripts and Automation

| Tool | What It Is |
|---|---|
| [Slack Crawler](slack-crawler/) | Claude Code skill I built and open-sourced here. Reads all channels in a named Slack sidebar section and produces a structured two-week intelligence brief, with hot callouts for the last 24 hours and three days at the top. Runs on demand. Optionally writes the brief to a Slack canvas. |
| [Slack Canvas Status Synthesis](slack-canvas-status-synthesis/) | Two-script workflow that reads a Slack canvas to extract a reusable status template, then uses that template to generate a draft status report from your Slack channels and canvases. Draft output only. Review before posting. |

---

## Maturity

| Tool | Status | Notes |
|---|---|---|
| Slack Crawler | Working | Strong signal-gathering workflow. Requires Claude Code and Slack MCP setup. A skill, so its paging and coverage line are instructions to Claude, not checks in code, and there is no automated test. |
| Slack Canvas Status Synthesis | Working | Draft output only, reviewed before publishing. Tested: `test_slack_status.py` runs both scripts end to end against recorded tool-call transcripts (template schema, smuggled instructions, sensitive data, tool boundary, observed coverage). A real setup is checked with `--doctor`. |

---

## The Two-Step Status Workflow

The two Slack tools are designed to work together. Run them in sequence to go from raw channel noise to a polished draft status report.

### Step 1: Run Slack Crawler once or twice a week

```text
/slack-crawler <section-name> --canvas new        # first run, creates the canvas
/slack-crawler <section-name> --canvas F0XXXXXXX  # subsequent runs, updates in place
```

The crawler reads all channels in a named sidebar section and produces a structured brief covering the last 14 days. It writes the brief to a canvas and keeps updating that same canvas each time you run it.

By the time you need to write a status report, you have a current, organized picture of what happened across all your channels, not your memory of it.

### Step 2: Run Slack Canvas Status Synthesis to draft the report

```text
./canvas_generator_from_template.py <template_name> <channel_ids|none> <crawler_canvas_id>
```

Pass the crawler's canvas ID as the third argument (comma-separate it with any other canvases). The synthesis tool then reads your program channels and the canvas the crawler just updated, applies a template extracted from one of your existing status canvases, and produces a draft in your usual format.

⚠️ **Pass the program channels too, not only the crawler canvas.** The crawler's brief is a summary a model wrote, so a blocker the crawler missed is missing from the brief as well, and a draft built only on the brief cannot see it. With the channels included, the synthesis tool reads the original messages, and its coverage check records, from the reads it observed, which channels were read in full, which were cut short, and which it could not confirm. Treat a fact that appears only in the brief as secondary, as the [Status Contract](STATUS-CONTRACT.md) says.

It will not be perfect. It will get you most of the way there: the structure, the populated sections, the signal pulled from Slack, and the first draft of the report. You still own the final call.

### Why this works

The crawler does the ongoing intelligence work throughout the week. The synthesis tool does the assembly work when you need to report. Keeping them separate means you can run the crawler on whatever cadence makes sense for your program without tying it to your reporting schedule.

---

## Where This Breaks

These tools break when they're treated as the source of truth.

A crawler can collect signal. It can't know whether a Slack message is confirmed, political, stale, or already superseded.

A status synthesis tool can draft. It cannot decide whether the program is Green, Yellow, or Red. It cannot own the risk call. It cannot make the escalation decision.

Use the tools to reduce mechanical work. Do not use them to avoid judgment.

---

## Safety and Data Handling

Before using any automation with real program data:

- Confirm the tool is approved for the data you're using.
- Don't paste secrets, credentials, private keys, customer-sensitive data, restricted incident details, unreleased roadmap commitments, or regulated personal data into unapproved tools.
- Sanitize inputs when possible.
- Review all generated drafts before sharing.
- Keep the system of record updated after the draft is finalized.

A polished draft is not the system of record.

---

## How This Fits Together

These tools are designed to work alongside the templates in [tpm-templates](https://github.com/ChefPlex/tpm-templates).

The RAID log, the kickoff checklist and the meeting notes tracker that used to live here are now in tpm-templates, beside the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) and the rest of the program documents.

The status synthesis tool produces drafts in whatever format your existing status canvas already uses, which means it works with the reporting structure in [program-reporting-frameworks](https://github.com/ChefPlex/program-reporting-frameworks).

They're separate repos because templates and tools serve different purposes, but they're designed to be used together.

---

## Contributing

If you have a tool, script, or template that saves TPMs real time, open a PR or file an issue describing it.

The bar:

- It has to work.
- It has to be generic enough to apply outside one company or team.
- It has to be documented well enough that someone can pick it up without asking you questions.
- It has to make the work clearer, safer, faster, or less fragile.

---

These tools exist because the mechanical parts of program management - gathering signal, drafting reports, tracking status - are solvable. The judgment parts are not. The goal is to spend less time on the former so you have more for the latter.


Maintained by [Eric White](https://www.linkedin.com/in/edwhite) | [ChefPlex](https://github.com/ChefPlex)

## License

Two licenses, one rule: **code is MIT, documents are CC BY 4.0.**

| What | License |
|:---|:---|
| The code: everything in [`slack-canvas-status-synthesis/`](slack-canvas-status-synthesis/) except its Markdown | [MIT](slack-canvas-status-synthesis/LICENSE). Use it in your own tooling, commercial or not, with the notice kept |
| Everything else: the Slack Crawler skill, the status contract, and all Markdown | [CC BY 4.0](LICENSE). Use it, adapt it, put it to work in your own program. Credit is the only condition |

Copyright (c) 2024-2026 Eric White.

---

**Part of the ChefPlex TPM portfolio** | Status: Active | [I need to… find the right document across all the repositories](https://github.com/ChefPlex/tpm-templates/blob/main/PORTFOLIO-GUIDE.md) | [All repositories](https://github.com/ChefPlex)
