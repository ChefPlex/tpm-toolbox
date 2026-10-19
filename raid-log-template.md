# RAID Log Template (Markdown)

The same log as [`raid-log-template.xlsx`](raid-log-template.xlsx), in a format you can read before you download anything, paste into Confluence or Notion, diff in a pull request, or open on a phone. The spreadsheet is still the better place to actually run a busy program - it sorts, filters and calculates. This is for everywhere the spreadsheet does not go.

The table below is the whole log: risks, assumptions, issues and dependencies in one place, each row with its owner, rating, date and plan. When an entry needs every field written out, use the [alternate style](#alternate-style-the-full-entry-for-each-item) at the bottom of this page. For how to run the log rather than what fields it has, read the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) in `tpm-templates`.

---

## RAID Log - [Program Name]

| ID | Description and impact | Owner | Rating | Target date | Status | Plan |
|:---|:---|:---|:---|:---|:---|:---|
| **Risks** - what could go wrong, and what are we doing about it | | | | | | |
| R1 | | | | | | |
| **Assumptions** - what we are treating as true without having verified it | | | | | | |
| A1 | | | | | | |
| **Issues** - what has already gone wrong and needs resolution | | | | | | |
| I1 | | | | | | |
| **Dependencies** - what this program is waiting on from somewhere else | | | | | | |
| D1 | | | | | | |

For a larger program, add the columns you need: category, date raised, proximity, strategy, who raised it, and whether it is shared with the customer.

### What goes in each column

- **ID:** R for a risk, A for an assumption, I for an issue, D for a dependency. Never reuse an ID; when a risk becomes an issue, the issue links back to it.
- **Description and impact:** what it is, and what happens to the program if it lands or stays unresolved.
- **Owner:** one named person. For a dependency, the owner on your side, with the contact on the other side in the plan.
- **Rating:** for a risk, probability x impact (1 to 9). For an issue, its priority. For a dependency, likelihood and impact. For an assumption, the impact if it is wrong.
- **Target date:** when the risk should be closed, the issue resolved, the assumption validated, or the dependency delivered.
- **Status:** see [the field values](#field-values).
- **Plan:** the mitigation for a risk, the resolution for an issue, the validation for an assumption, or what you need and from whom for a dependency.

---

## How to Fill It In

**Start with a brainstorm.** Set up a session with the program team, and the customer where there is one, to pull together the first list of risks, assumptions, issues and dependencies. Start it from the charter review, before the kickoff.

**Then review it on a cadence.** Weekly for high-velocity programs, bi-weekly for steadier ones. Go through the log with the team so it is updated and everyone shares the same picture.

**Check three counts at every review.** Open risks · risks with no owner · risks with no plan. Do the same for issues. The second and third numbers should be zero; anything else is the first thing to fix.

**Log an assumption any time you are treating something as true without confirmation.** The test is simple: if it turned out to be false, would it change the plan? If yes, it belongs here.

**Every dependency needs an owner on your side and a named contact on the other side.** "I haven't heard back" is not a status.

**Rate risks the same way every time.** Probability and impact are each High, Medium or Low, scored 3, 2, 1. A rating of 6 or above gets active mitigation and regular review.

---

## What to Learn From

### Unknown vs Actionable

The same risk, written two ways:

| | ID | Description and impact | Owner | Rating | Target date | Status | Plan |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **Unknown** | R1 | Migration dates | Service teams | High | | Open | Follow up |
| **Actionable** | R1 | Fourteen of forty service teams have not committed a migration date. Without dates there is no schedule, and the regulatory deadline does not move | A. Okafor | 6 (Medium x High) | 2026-04-15 | In Progress | Weekly named-owner follow-up. Escalate any team with no date by the 15th to their director, with the deadline attached |

The actionable row answers who owns it, what the risk is, when it should close, where it hits (the schedule and the regulatory date), why it matters, and how it is being worked. The unknown row names a topic, not a risk.

### More Worked Rows

| ID | Description and impact | Owner | Rating | Target date | Status | Plan |
|:---|:---|:---|:---|:---|:---|:---|
| A1 | The service inventory in the CMDB covers every service in scope. It is the only inventory that exists, and it is what the audit will be measured against. If wrong, scope is understated and every date derived from it moves, including the one committed to the regulator | R. Nasser | High if wrong | | Open | Reconcile the CMDB against the load balancer config and the cloud account inventory |
| I1 | The final validation environment has no allocated hardware. Nothing can be certified as done until it exists, so completed migrations are stacking up unverified. This was R4 until it materialized | M. Delgado | High | 2026-03-29 | In Progress | Infrastructure has the request. Escalated to the platform director on 3/18 with the count of blocked migrations attached |
| D1 | Additional HSM capacity is needed before the second wave of services can cut over. If late, wave two slips by the length of the delay, and wave three slips with it | S. Whitfield | Medium x High | 2026-04-30 | At Risk | Need provisioned capacity in both regions, plus the key ceremony scheduled, from J. Aubert, Platform Infrastructure. Their roadmap review is on the 22nd; confirm the ask is on the agenda before then |

The example entries are illustrative and the names are invented. The shape of them is not: every one is written the way the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) argues an entry should be written, with a named owner, a specific impact, and a plan somebody is actually working.

### Where This Breaks

- **Opened only when something goes wrong.** A log nobody reviews between incidents is a record, not a tool. Review it on the cadence.
- **Risks with no owner or no plan.** They are the easiest thing to see in the counts and the most common thing left alone.
- **Silence logged as progress.** Two teams that never replied are not a green status. Say so in the row.

---

## Reference

### Field Values

| Field | Values |
|:---|:---|
| Risk category | Technical / Schedule / Budget / Operational / External |
| Probability and impact | High / Medium / Low |
| Risk rating | Probability x impact, scoring Low 1, Medium 2, High 3 (so 1 to 9). 6 or above gets active mitigation and regular review |
| Proximity | How soon it could land: This Sprint / This Quarter / Later |
| Strategy | Avoid / Mitigate / Transfer / Accept |
| Risk status | Open / In Progress / Mitigated / Closed |
| Assumption status | Open / Validated / Invalidated / Closed |
| Issue priority | High / Medium / Low |
| Issue status | Open / In Progress / Resolved / Closed |
| Dependency type | Internal (another team) / External (vendor, regulator, customer) |
| Dependency status | On Track / At Risk / Blocked / Complete |

### Where Risks Come From

A prompt list for the brainstorm, by category:

| Category | Look at |
|:---|:---|
| Technical | Requirements, technology, interfaces, performance, quality, complexity |
| Schedule | Inaccurate estimates, resource allocation, time tracking |
| Budget | Wrong budget estimate, scope creep, budget tracking, cost overruns |
| Operational | Resource planning, roles and responsibilities, communication and cooperation, not enough people, dependencies, skills, training |
| External | Customer, suppliers and subcontractors, partners, legal, events outside anyone's control |

### Other Logs Worth Keeping

When the program needs them, keep these beside the RAID log, one row each:

| Log | Columns |
|:---|:---|
| Actions | Action, owner, date raised, source, status, target or completed date |
| Decisions | Decision, category, status, agreed date or target date, agreed by, evidence or approval, related risk / issue / action |
| Changes | Change, impact, raised by, date raised, owner, status, decision |
| Deliverables | Deliverable, link, author, status, target date, approver, sign-off date and version |

### About the Spreadsheet

The spreadsheet's Days Open column on risks and issues is calculated, so it is left out here, where it would go stale.

---

## Alternate Style: The Full Entry for Each Item

Use this when an entry needs every field written out, for a high-rated risk or a dependency on another organization. Copy the block for the type you need, and keep the summary row in the log.

```markdown
## Program

| Field | Detail |
|:---|:---|
| Program Name | |
| TPM | |
| Last Reviewed | |
| Review Cadence | Weekly for high-velocity programs, bi-weekly for steadier ones |

### R[n] - [Risk title]

| Field | Entry |
|:---|:---|
| Description and Impact | |
| Owner | |
| Category | |
| Probability | |
| Impact | |
| Risk Rating | |
| Proximity | |
| Strategy | |
| Mitigation Plan | |
| Status | |
| Date Raised | |
| Target Close | |
| Date Closed | |
| Notes | |

### A[n] - [Assumption]

| Field | Entry |
|:---|:---|
| Assumption Description | |
| Status | |
| Reason / Basis | |
| Validation Action | |
| Impact if Wrong | |
| Owner | |
| Date Raised | |
| Date Closed | |
| Notes | |

### I[n] - [Issue]

| Field | Entry |
|:---|:---|
| Description and Impact | |
| Owner | |
| Category | |
| Priority | |
| Resolution Plan | |
| Status | |
| Date Raised | |
| Target Resolution | |
| Date Closed | |
| Linked Risk ID | |
| Notes | |

### D[n] - [Dependency]

| Field | Entry |
|:---|:---|
| Description | |
| Type | |
| What We Need | |
| Owner (Our Side) | |
| External Contact | |
| Due Date | |
| Impact if Late | |
| Likelihood | |
| Impact | |
| Status | |
| Notes | |
```

---

*Template version 1.1. Propose changes via pull request.*
