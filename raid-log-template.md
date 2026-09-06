# RAID Log Template (Markdown)

The same log as [`raid-log-template.xlsx`](raid-log-template.xlsx), in a format you can read
before you download anything, paste into Confluence or Notion, diff in a pull request, or open on
a phone. The spreadsheet is still the better place to actually run a busy program - it sorts,
filters and calculates. This is for everywhere the spreadsheet does not go.

For how to run the log rather than what fields it has, read the
[RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md) in
`tpm-templates`.

**One structural difference, on purpose.** The spreadsheet uses one wide row per entry, which is
right for a spreadsheet and unreadable as a 16-column markdown table. Here each entry is a small
block, and each section opens with a narrow at-a-glance table so you can still scan the whole log
in one screen. Same fields, shape that suits the medium.

---

## Program

| Field | Detail |
|---|---|
| Program Name | |
| TPM | |
| Last Reviewed | |
| Review Cadence | Weekly for high-velocity programs, bi-weekly for steadier ones |

---

## Risks

*What could go wrong, and what are we doing about it.*

**Category:** Technical / Schedule / Budget / Operational / External
**Probability and Impact:** High / Medium / Low
**Risk Rating:** probability x impact. 7 or above gets active mitigation and regular review
**Proximity:** how soon it could land - This Sprint / This Quarter / Later
**Strategy:** Avoid / Mitigate / Transfer / Accept
**Status:** Open / In Progress / Mitigated / Closed

### At a glance

| ID | Risk | Owner | Rating | Status |
|---|---|---|---|---|
| R1 | Service teams have not committed migration dates | A. Okafor | 8 | In Progress |
| R2 | | | | |

### R1 - Service teams have not committed migration dates

| Field | Entry |
|---|---|
| Description and Impact | Fourteen of forty service teams have not committed a migration date. Without dates there is no schedule, and the regulatory deadline does not move. |
| Owner | A. Okafor |
| Category | Schedule |
| Probability | Medium |
| Impact | High |
| Risk Rating | 8 |
| Proximity | This Quarter |
| Strategy | Mitigate |
| Mitigation Plan | Weekly named-owner follow-up. Escalate any team with no date by the 15th to their director, with the deadline attached. |
| Status | In Progress |
| Date Raised | 2026-03-02 |
| Target Close | 2026-04-15 |
| Date Closed | |
| Notes | Two of the fourteen have never replied. Silence is not a green status. |

### R2 - [Risk title]

| Field | Entry |
|---|---|
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

---

## Assumptions

*What we are treating as true without having verified it.*

**Status:** Open / Validated / Invalidated / Closed

Log an assumption any time you are treating something as true without confirmation. The test is
simple: if it turned out to be false, would it change the plan? If yes, it belongs here.

### At a glance

| ID | Assumption | Owner | Status |
|---|---|---|---|
| A1 | The inventory in the CMDB is complete enough to scope from | R. Nasser | Open |
| A2 | | | |

### A1 - The CMDB inventory is complete enough to scope from

| Field | Entry |
|---|---|
| Assumption Description | The service inventory in the CMDB covers every service in scope. |
| Status | Open |
| Reason / Basis | It is the only inventory that exists, and it is what the audit will be measured against. |
| Validation Action | Reconcile the CMDB against the load balancer config and the cloud account inventory. |
| Impact if Wrong | Scope is understated. Every date derived from it moves, including the one committed to the regulator. |
| Owner | R. Nasser |
| Date Raised | 2026-03-02 |
| Date Closed | |
| Notes | |

### A2 - [Assumption]

| Field | Entry |
|---|---|
| Assumption Description | |
| Status | |
| Reason / Basis | |
| Validation Action | |
| Impact if Wrong | |
| Owner | |
| Date Raised | |
| Date Closed | |
| Notes | |

---

## Issues

*What has already gone wrong and needs resolution. A risk that happened is an issue.*

**Category:** Technical / Schedule / Budget / Operational / External
**Priority:** High / Medium / Low
**Status:** Open / In Progress / Resolved / Closed

### At a glance

| ID | Issue | Owner | Priority | Status |
|---|---|---|---|---|
| I1 | Validation environment is not available | M. Delgado | High | In Progress |
| I2 | | | | |

### I1 - Validation environment is not available

| Field | Entry |
|---|---|
| Description and Impact | The final validation environment has no allocated hardware. Nothing can be certified as done until it exists, so completed migrations are stacking up unverified. |
| Owner | M. Delgado |
| Category | Operational |
| Priority | High |
| Resolution Plan | Infrastructure has the request. Escalated to the platform director on 3/18 with the count of blocked migrations attached. |
| Status | In Progress |
| Date Raised | 2026-03-11 |
| Target Resolution | 2026-03-29 |
| Date Closed | |
| Linked Risk ID | R4 |
| Notes | This was R4 until it materialized. Keep the link so the history stays readable. |

### I2 - [Issue]

| Field | Entry |
|---|---|
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

---

## Dependencies

*What this program is waiting on from somewhere else.*

**Type:** Internal (another team) / External (vendor, regulator, customer)
**Status:** On Track / At Risk / Blocked / Complete

Every dependency needs an owner on your side and a named contact on the other side. "I haven't
heard back" is not a status.

### At a glance

| ID | Dependency | Owner | Due | Status |
|---|---|---|---|---|
| D1 | HSM capacity from the platform team | S. Whitfield | 2026-04-30 | At Risk |
| D2 | | | | |

### D1 - HSM capacity from the platform team

| Field | Entry |
|---|---|
| Description | Additional HSM capacity is needed before the second wave of services can cut over. |
| Type | Internal |
| What We Need | Provisioned capacity in both regions, plus the key ceremony scheduled. |
| Owner (Our Side) | S. Whitfield |
| External Contact | J. Aubert, Platform Infrastructure |
| Due Date | 2026-04-30 |
| Impact if Late | Wave two slips by the length of the delay. Wave three slips with it. |
| Likelihood | Medium |
| Impact | High |
| Status | At Risk |
| Notes | Their roadmap review is on the 22nd. Confirm the ask is on the agenda before then. |

### D2 - [Dependency]

| Field | Entry |
|---|---|
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

---

The example entries are illustrative and the names are invented. The shape of them is not: every
one is written the way the [RAID Log Guide](https://github.com/ChefPlex/tpm-templates/blob/main/raid-log-guide.md)
argues an entry should be written, with a named owner, a specific impact, and a plan somebody is
actually working.
