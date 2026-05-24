# Slack Canvas Status Synthesis - Examples

These examples show the intended use pattern: extract a format from a status canvas that already works, generate a draft from current Slack sources, then review before posting.

The IDs below are placeholders. Do not commit real channel IDs, canvas IDs, customer names, ticket links, or internal program details.

---

## Example 1: Weekly Program Status

### Scenario

You send a weekly status update with the same basic shape every Friday:

- Overall Red / Yellow / Green status
- What changed this week
- What is coming next
- Risks and blockers
- Decisions needed
- Owners and follow-up dates

### One-time setup

```bash
./canvas_template_extractor.py F0PASTSTATUSCANVAS weekly_program_status
```

### Weekly draft

```bash
./canvas_generator_from_template.py weekly_program_status \
  C0PROGRAMCHANNEL F0PLANNINGCANVAS \
  --output weekly_status_$(date +%Y_%m_%d).md \
  --lookback 7
```

### Human review

Before sending, verify the things that actually matter:

- Is the Green / Yellow / Red status defensible?
- Are dates and owners current?
- Are blockers written as decision points, not vague concerns?
- Did the draft miss anything that happened outside Slack?

The output should save time. It should not get a free pass.

---

## Example 2: Security Remediation Rollup

### Scenario

You are tracking a security remediation effort across multiple service teams. The useful weekly update is not a transcript of every Slack message. It is a clean rollup of:

- Services completed
- Services still in progress
- Aging exceptions
- Blocked teams
- Compliance or audit dates
- Sponsor asks

### One-time setup

```bash
./canvas_template_extractor.py F0SECURITYSTATUS security_remediation_status
```

### Weekly draft

```bash
./canvas_generator_from_template.py security_remediation_status \
  C0SECURITYPM,C0SERVICEOWNERS,C0COMPLIANCE \
  F0SECURITYDASHBOARD,F0EXCEPTIONS \
  --output security_status_$(date +%Y_%m_%d).md \
  --lookback 7
```

### What to watch

This is the kind of report where polish can be dangerous. If the source channels do not include exception approvals, risk acceptances, or current service counts, the draft may look complete while still being wrong.

That is not an AI problem. That is a source-of-truth problem. The tool just makes it easier to see.

---

## Example 3: Executive Monthly Brief

### Scenario

A monthly executive brief needs a cleaner structure than a team status update:

- Bottom line
- Health by workstream
- Material changes since last review
- Decisions needed
- Risks that require leadership attention
- Next milestone

### One-time setup

```bash
./canvas_template_extractor.py F0EXECBRIEF exec_monthly_brief
```

### Monthly draft

```bash
./canvas_generator_from_template.py exec_monthly_brief \
  C0PROGRAM1,C0PROGRAM2,C0PROGRAM3 \
  F0METRICS,F0ROADMAP,F0RISKS \
  --output exec_brief_$(date +%Y_%m).md \
  --lookback 30
```

### Review rule

For executive updates, remove anything that sounds smart but does not drive a decision. Leaders do not need a decorated activity log. They need the truth, the risk, and the ask.

---

## Example 4: Incident Follow-up

### Scenario

After an incident, you need to turn a busy incident channel into a structured follow-up:

- Timeline
- Customer or service impact
- Root cause, if known
- Corrective actions
- Owners
- Due dates
- Open questions

### One-time setup

```bash
./canvas_template_extractor.py F0PASTINCIDENTREVIEW incident_followup
```

### Per-incident draft

```bash
./canvas_generator_from_template.py incident_followup \
  C0INCIDENT123 none \
  --output incident_123_followup.md \
  --lookback 3
```

### Review rule

Do not let the tool invent certainty. If root cause is not confirmed, the draft should say that plainly. An accurate open question is better than a confident wrong answer.

---

## Example 5: Daily Program Pulse

### Scenario

You want a short morning pulse across a few active workstreams:

- New blockers
- Overnight changes
- Decisions waiting on someone
- Items at risk today
- Follow-ups for the TPM

### One-time setup

```bash
./canvas_template_extractor.py F0DAILYPULSE daily_program_pulse
```

### Daily draft

```bash
./canvas_generator_from_template.py daily_program_pulse \
  C0TEAM1,C0TEAM2,C0TEAM3 F0PROGRAMCANVAS \
  --output daily_pulse_$(date +%Y_%m_%d).md \
  --lookback 1
```

### Review rule

Daily summaries should be short. If the draft turns into a newsletter, cut it back to the decisions and risks.

---

## Wrapper Script Pattern

For repeat use, wrap the command so the inputs are not retyped every week.

### `weekly_status.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TEMPLATE="weekly_program_status"
CHANNELS="C0PROGRAMCHANNEL,C0SECURITYCHANNEL"
CANVASES="F0PLANNINGCANVAS,F0RISKCANVAS"
OUTPUT="weekly_status_$(date +%Y_%m_%d).md"

cd "$(dirname "$0")"

./canvas_generator_from_template.py "$TEMPLATE" \
  "$CHANNELS" "$CANVASES" \
  --output "$OUTPUT" \
  --lookback 7

echo "Draft generated: $OUTPUT"
echo "Review before posting. The tool writes drafts, not truth."
```

### `exec_brief.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

TEMPLATE="exec_monthly_brief"
CHANNELS="C0PROGRAM1,C0PROGRAM2,C0PROGRAM3"
CANVASES="F0METRICS,F0ROADMAP,F0RISKS"
OUTPUT="exec_brief_$(date +%Y_%m).md"

cd "$(dirname "$0")"

./canvas_generator_from_template.py "$TEMPLATE" \
  "$CHANNELS" "$CANVASES" \
  --output "$OUTPUT" \
  --lookback 30

echo "Draft generated: $OUTPUT"
```

---

## Scheduled Drafts

Scheduling can be useful. Auto-posting is a different risk profile.

This is safe enough:

```cron
# Weekly draft every Friday at 4 PM
0 16 * * 5 cd /path/to/tpm-toolbox/slack-canvas-status-synthesis && ./weekly_status.sh
```

This repo does not include auto-posting to Slack. That is intentional. Review is part of the workflow, not a nice-to-have.

---

## Tips That Actually Matter

### Use a good source template

Use a canvas that has survived real use. A one-off draft or a rushed status update will teach the tool the wrong shape.

Good source templates usually have:

- Clear sections
- Stable status language
- Consistent owner and date patterns
- A visible place for risks and asks
- Enough structure that someone else could understand the report without you narrating it

### Pick source channels carefully

More channels do not automatically mean a better report. Five noisy channels can produce a worse draft than one useful status channel and one good planning canvas.

Use sources that contain decisions, blockers, owner changes, dates, and workstream updates.

### Keep templates current

A status template is not sacred. If the program changes, the template should change too.

Re-extract or update the template when:

- The audience changes
- The program moves from planning to execution
- Metrics become available
- Risks need a different escalation path
- The report starts feeling like paperwork

---

## What I Would Measure

I would not call this successful because the draft looks good. I would call it successful if it improves the status process without hiding risk.

Useful measures:

- Time from source review to first usable draft
- Number of corrections needed before posting
- Number of missing risks caught during review
- Number of invented or unsupported claims removed
- Whether the final report drives a decision, escalation, or dependency follow-up

A pretty report that avoids the hard question is still a bad report.
