# Program Kickoff Checklist

A program kickoff is the moment a team officially starts working together toward a shared objective. The whole value is settling scope, roles and working norms before anyone writes a line of code or opens a remediation ticket, because each of those gets harder to renegotiate the longer the program runs. The failed version is a deck nobody remembers.

The table below is the whole checklist, in the order the work happens: getting ready, the kickoff itself, and setting the program up to run. Each row says what happens, what it produces, who owns it and how much it matters. The kickoff agenda and what to cover in each part of the meeting are in [Reference](#reference).

---

## Kickoff Checklist - [Program Name]

| What happens | Artifact / outcome | Owner | Level | Status | Notes |
|:---|:---|:---|:---|:---|:---|
| **Get ready** | | | | | |
| Sponsor reviews and approves the charter | Approved charter | Product / program owner | Must | | |
| Name the executive sponsor, product / program owner and engineering lead | Names in the charter | TPM | Must | | |
| Write objectives that can be measured | Objectives in the charter | Product / program owner | Must | | Not "improve security posture" but "achieve X% coverage by Y date" |
| List what is in scope and what is out | Scope in the charter | Product / program owner + TPM | Must | | |
| Propose the Definition of Done and agree it with the TPM and engineering lead | Definition of Done | Product / program owner | Must | | If the goal is to move a metric, record the baseline, or a to-do to get one |
| Draft the RACI | RACI | TPM | Should | | It doesn't need to be final, but it needs to exist |
| Start the stakeholder list with the sponsor and known owners | Stakeholder list | TPM | Should | | It fills in through discovery |
| Draft the high-level milestone plan | Milestone plan | TPM | Must | | Enter any known compliance deadlines |
| Start the RAID log from the charter review | RAID log | TPM | Must | | |
| Draft the high-level design | HLD | Engineering lead + architect | Should | | For engineering programs |
| Set up the document repository | Repository link | TPM | Must | | |
| Set up the program tracking system | Tracker (Jira, Linear, Asana, or equivalent) | TPM | Should | | |
| Draft the communications plan | Communications plan | TPM | Should | | At minimum: cadence, channel, owner |
| Name the roster with roles and allocations | Team roster | TPM + engineering lead | As needed | | |
| Agree the business case | Business case | Product / program owner | As needed | | Each problem paired with the objective that fixes it, and why now |
| Get the budget approved | Approved budget | Product / program owner | As needed | | Or the date it will be approved, and by whom |
| Decide build or buy | Record of the decision | Product / program owner + engineering lead | As needed | | When buying is on the table |
| Sign vendor or contractor SOWs | Signed SOW | Product / program owner + procurement | As needed | | Or the date they will be |
| Triage compliance: which frameworks apply? | Triage outcome | TPM | As needed | | Initiate early; late discoveries are the expensive kind |
| Start the security / architecture review | Review request | TPM + engineering lead | As needed | | |
| Start the legal / privacy review | Review request | TPM | As needed | | |
| Draft and review the kickoff deck | Kickoff deck | TPM | Should | | |
| **Kick off** | | | | | |
| Run the kickoff | Kickoff held | TPM | Must | | 90 minutes for most programs, two hours for complex multi-team ones. See the [agenda](#kickoff-agenda) |
| Record the session | Recording | TPM | Should | | For async team members and future joiners |
| Agree how the team will work | Team agreement | TPM | Should | | Five agreed principles beat a ten-page team charter |
| Brainstorm risks and put owners on the top three | RAID log entries | All | Must | | Five to ten minutes, everyone contributes |
| Name the open questions, each with an owner | Open questions list | TPM | Must | | |
| **Set up to run (within 48 hours)** | | | | | |
| Send the kickoff notes to attendees and stakeholders | Kickoff notes | TPM | Must | | |
| Enter the action items with owners and due dates | Action items in the tracker | TPM | Must | | |
| Log the risks and open questions from the kickoff | RAID log, open questions log | TPM | Should | | |
| Start the weekly program team meeting | Recurring invite | TPM | Must | | |
| Start the steering committee | Monthly invite | TPM | As needed | | When the program needs one |
| Create the program channel and share the repository link in it | Program channel | TPM | Should | | Slack, Teams, or equivalent |
| Update the charter with changes from the kickoff | Updated charter | Product / program owner + TPM | Should | | |
| Schedule the first status report | First report on the calendar | TPM | Must | | |

### What goes in each column

- **What happens:** the activity, in the order the work usually happens. Bold rows mark the three stretches: getting ready, the kickoff, and setting up to run.
- **Artifact / outcome:** what exists when the activity is done.
- **Owner:** the person who gets it done. Write a name, not a role, once you know it.
- **Level:** **Must** - nearly every program needs it. **Should** - the right practice for most programs. **As needed** - add it when the program calls for it.
- **Status:** done, in progress, not started, or skipped.
- **Notes:** a link, what is still open, when it will be done, or why it was skipped.

---

## How to Fill It In

Go through it every time. Not every row fits every program: skip the ones that do not, and go deeper on the ones that matter more than usual. The point is to think about each one before the kickoff, so nothing catches you off guard later.

**Get as much ready as you can.** A kickoff that happens before the foundation is ready creates false starts, not momentum. If something genuinely cannot be done yet, write down when it will be and who owns it, and say so at the kickoff.

**Move a row up when it applies.** A program that buys from a vendor needs the SOW before the kickoff. A program with regulatory exposure needs the compliance triage. When an "As needed" row applies, treat it as a Must.

**Add rows.** The list is a starting point. Add what your program needs, in the place it happens.

---

## What to Learn From

### Unknown vs Actionable

The same row, written two ways:

| | What happens | Artifact / outcome | Owner | Level | Status | Notes |
|:---|:---|:---|:---|:---|:---|:---|
| **Unknown** | RACI | | TPM | Should | Not done | |
| **Actionable** | Draft the RACI and review it with the sponsor and engineering lead | RACI v0.2 in the program repository [link] | [TPM name] | Should | In progress: draft sent Oct 14 | Reviewed in the kickoff on Oct 21. The scope-change row still has no A; it goes on the kickoff's open questions |

The actionable row answers who owns it, what exists, when it will be done, where it lives, why it is not finished and how the gap will be handled. The unknown row only says something is missing.

### Where This Breaks

- **A deck nobody remembers.** The kickoff is where scope, roles and working norms get settled. If it is only a presentation, nothing gets settled.
- **Kicking off before the foundation is ready.** A kickoff that happens before the foundation is ready creates false starts, not momentum.
- **No risks surfaced.** A kickoff that ends without surfacing any risks is a kickoff that didn't create enough psychological safety for people to be honest.
- **Open scope questions left implicit.** If there are open scope questions, name them. Do not leave them implicit.
- **The plan presented as fixed.** Present it as the current best understanding, which will be refined as the team learns more.
- **A ten-page team charter.** Five agreed principles are better than a ten-page team charter nobody reads.

---

## Reference

### Kickoff Agenda

A kickoff does not need to be long. 90 minutes is usually enough for most programs. Two hours for complex multi-team programs. More than two hours and you're probably covering things that belong in working sessions, not kickoffs.

**Recommended agenda (two-hour version, for complex multi-team programs):**

For the usual 90-minute kickoff, keep the same order and shorten each block by about a quarter. For a remote kickoff that runs past 90 minutes, split it into two sessions (see [remote kickoffs](#remote-kickoffs)).

| Time | Topic | Owner | Notes |
|:---|:---|:---|:---|
| 0:00 - 0:10 | Introductions and context | TPM | Who is in the room and why |
| 0:10 - 0:25 | Problem statement and strategic alignment | PO | Why are we doing this |
| 0:25 - 0:45 | Scope, objectives, and Definition of Done | TPM + PO | What are we building and what does done look like |
| 0:45 - 1:00 | Roles and RACI | TPM | Who owns what |
| 1:00 - 1:20 | Plan, milestones, and dependencies | TPM | How we are going to get there |
| 1:20 - 1:30 | Working norms | TPM | How the team will operate |
| 1:30 - 1:45 | Risks and open questions | All | What are we worried about |
| 1:45 - 2:00 | Q&A and next steps | TPM | Close with clarity |

**Record the kickoff.** Async team members, future joiners, and anyone who needs to ramp up later will thank you.

### What to Cover in Each Section

#### Problem Statement and Strategic Alignment

This is the most important part of the kickoff and the one most often glossed over. The team needs to understand not just what they're building but why it matters. Engineers who understand the business problem make better technical decisions than engineers who are handed a spec.

Cover:
- The specific problem or risk being addressed
- Why it matters to the business now
- What happens if the program does not succeed
- How it connects to the organization's current priorities

#### Scope, Objectives, and Definition of Done

Be specific and leave no room for ambiguity. This is the contract.

Cover:
- Objectives with measurable targets
- Explicit in-scope and out-of-scope items
- Definition of Done at the program level and, if possible, at the milestone level
- Any known scope constraints or boundaries

If there are open scope questions, name them. Do not leave them implicit.

#### Roles and RACI

Every person in the room should leave knowing what they're responsible for and who to go to for decisions. Don't read the RACI table out loud - review it at a high level, call out the decision-making structure, and confirm that everyone understands their role.

Specifically cover:
- Who is the single accountable owner for program success (usually the PO or exec sponsor)
- Who makes technical decisions (engineering lead)
- Who manages the program (TPM)
- Who escalation goes to when the team is stuck
- Which external teams the program depends on and who owns those relationships

#### Plan, Milestones, and Dependencies

Walk through the milestone plan at a high level. Don't present it as fixed - present it as the current best understanding, which will be refined as the team learns more.

Specifically cover:
- The major milestones and target dates
- Known dependencies on other teams and the current status of those dependencies
- Any hard external deadlines (compliance dates, product launches, contractual obligations)
- The planning process going forward - how the team will refine the plan, who contributes, how often it gets updated

#### Working Norms

This section prevents a lot of friction later. The team should agree on:

- Meeting cadence (team sync, steering committee, how decisions get made between meetings)
- Status reporting (format, frequency, channel, who reads it)
- How decisions get documented (RAID log, decision log, meeting notes)
- Communication channel and expectations (response time, what goes in Slack vs. email vs. the tracker)
- How scope changes are handled (change control process)
- How the team gives each other feedback when something isn't working

These do not need to be elaborate. Five agreed principles are better than a ten-page team charter nobody reads.

#### Risks and Open Questions

Do not skip this. A kickoff that ends without surfacing any risks is a kickoff that didn't create enough psychological safety for people to be honest.

Run a quick risk brainstorm - five to ten minutes, everyone contributes. Log everything in the RAID log. Assign owners to the top three. The rest get monitored.

Close with explicit open questions that need to be resolved before the team can proceed, and name who is responsible for resolving each one.

### Remote Kickoffs

Most of the same principles apply, with a few additions:

**Camera on.** The kickoff is the first time many team members are meeting each other. Face-to-face - even virtual face-to-face - matters for relationship building.

**Breakout rooms for working norms.** Small group discussion is more productive than plenary for working norms. Put people in groups of 4-5 for 10 minutes, then bring back the top three agreements from each group.

**Interactive elements.** A kickoff where everyone stares at a deck for 90 minutes doesn't build alignment. Use polls, shared docs, or a virtual whiteboard for the risk brainstorm.

**Shorter sessions.** Remote attention spans are shorter. If the kickoff needs to be more than 90 minutes, split it into two sessions with a break in between.

---

## Alternate Style: A Plain Checklist

Use this when you would rather tick boxes than fill in a table. Copy the block into the program folder.

```markdown
# Kickoff Checklist: [Program Name]

## Get Ready
- [ ] (Must) Sponsor reviews and approves the charter
- [ ] (Must) Executive sponsor, product / program owner and engineering lead named
- [ ] (Must) Objectives can be measured
- [ ] (Must) In scope and out of scope listed
- [ ] (Must) Definition of Done proposed and agreed
- [ ] (Should) RACI drafted
- [ ] (Should) Stakeholder list started
- [ ] (Must) High-level milestone plan drafted
- [ ] (Must) RAID log started from the charter review
- [ ] (Should) High-level design drafted
- [ ] (Must) Document repository set up
- [ ] (Should) Program tracking system set up
- [ ] (Should) Communications plan drafted
- [ ] (As needed) Roster with roles and allocations
- [ ] (As needed) Business case agreed
- [ ] (As needed) Budget approved, or the date it will be
- [ ] (As needed) Build or buy decided and recorded
- [ ] (As needed) Vendor or contractor SOWs signed, or the date they will be
- [ ] (As needed) Compliance triage done
- [ ] (As needed) Security / architecture review started
- [ ] (As needed) Legal / privacy review started
- [ ] (Should) Kickoff deck drafted and reviewed

## Kick Off
- [ ] (Must) Kickoff held
- [ ] (Should) Session recorded
- [ ] (Should) Team agreement on how the team will work
- [ ] (Must) Risks brainstormed; top three have owners
- [ ] (Must) Open questions named, each with an owner

## Set Up to Run (Within 48 Hours)
- [ ] (Must) Kickoff notes sent
- [ ] (Must) Action items in the tracker with owners and due dates
- [ ] (Should) Risks and open questions logged
- [ ] (Must) Weekly program team meeting started
- [ ] (As needed) Steering committee started
- [ ] (Should) Program channel created, repository link shared in it
- [ ] (Should) Charter updated with changes from the kickoff
- [ ] (Must) First status report scheduled
```

---

*Template version 1.1. Propose changes via pull request.*
