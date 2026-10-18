# Status Contract

The rules every AI-assisted status report in these repositories follows. Two tools draft status reports: the [Slack Canvas Status Synthesis](slack-canvas-status-synthesis/) scripts here, and the [status report generator](https://github.com/ChefPlex/ai-automations/tree/main/status-report-generator) in `ai-automations`. They present a draft differently. They do not differ on what a draft is allowed to decide.

---

## What the model may do

- **Summarize what the sources say**, using only facts found in them: dates, owners, ticket IDs, metrics and links exactly as written.
- **Lay out the evidence for a status**, with the source of each point.
- **Suggest a status color**, only if the tool's mode allows it, and only labeled as a suggestion with a one-line rationale drawn from the sources.

## What must stay unresolved in the draft

The model does not settle these. It names them in a `Needs Review` section:

- A required fact that is missing (no owner, no date, no metric).
- Sources that conflict with each other.
- Anything that reads like an instruction addressed to the model rather than information about the program.
- Any source that was not read, or not read in full.

## What only a person decides

- **The status color.** Red, Yellow or Green is a judgment about risk and confidence, and it belongs to the TPM.
- **The risk call and any escalation.**
- **Whether the report is published**, and to whom. Neither tool posts anything.

## What every draft must carry

- **Its coverage.** Which sources were read, which were not, and which were cut short. A source left out of the coverage record is a source the reader will assume was covered.
- **The difference between evidence and summary.** A summary written by a model, such as a crawler brief, can be an input, but it is not primary evidence. A fact found only in a summary is marked that way.

---

## How each tool applies it

| | Status color | Coverage |
|:---|:---|:---|
| Slack Canvas Status Synthesis | Suggests one, labeled `Suggested status (TPM decides)` | Checked in code from the reads the run actually made, written as `<draft>.coverage.json`. An incomplete draft is marked INCOMPLETE at the top |
| Status report generator (`ai-automations`) | Suggests none. Lays out the evidence for each color and marks the field `TPM CALL` | The inputs are what you paste in, so coverage is what you chose to include |

The stricter tool and the more helpful tool both follow this contract. Choose by how much help you want with the color, not by which one is "safer".

---

*Part of the [tpm-toolbox](README.md). Maintained by [Eric White](https://www.linkedin.com/in/edwhite) | [ChefPlex](https://github.com/ChefPlex)*
