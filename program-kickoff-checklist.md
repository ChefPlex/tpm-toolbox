# Program Kickoff Checklist

A program kickoff is the moment a team officially starts working together toward a shared objective. Done well, it aligns everyone on scope, roles, plan, and working norms before anyone has written a line of code or sent a remediation ticket. Done poorly, it is a deck nobody remembers and a calendar invite that produces no shared understanding.

This checklist covers what needs to be in place before the kickoff, what needs to happen in the kickoff, and what needs to happen right after. Use it every time. The programs where you skip steps are the ones that teach you why the steps exist.

---

## Part 1: Pre-Kickoff - What Must Exist Before the Meeting

Do not schedule the kickoff until these are done. A kickoff that happens before the foundation is ready creates false starts, not momentum.

### Charter and Scope

- [ ] Program charter drafted and reviewed by executive sponsor
- [ ] Objectives are specific and measurable - not "improve security posture" but "achieve X% coverage by Y date"
- [ ] Definition of Done agreed by TPM, PO, and engineering lead
- [ ] In-scope items explicitly listed
- [ ] Out-of-scope items explicitly listed
- [ ] Build vs. buy decision made and documented (if applicable)

### Resources and Roles

- [ ] Executive sponsor named and confirmed
- [ ] Product / program owner named and confirmed
- [ ] Engineering lead named and confirmed
- [ ] Core team roster complete with roles and allocations
- [ ] RACI drafted (does not need to be final, but needs to exist)
- [ ] Any vendor or contractor engagements initiated

### Plan and Infrastructure

- [ ] High-level milestone plan drafted
- [ ] Program tracking system set up (Jira, Linear, Asana, or equivalent)
- [ ] Document repository established and location communicated
- [ ] RAID log created with initial entries from charter review
- [ ] Kickoff deck drafted and reviewed

### Compliance and Reviews

- [ ] Compliance triage completed - which regulatory frameworks apply?
- [ ] Security / architecture review initiated if required
- [ ] Legal / privacy review initiated if required
- [ ] Known compliance deadlines entered into the milestone plan

### Communications

- [ ] Stakeholder list finalized
- [ ] Communications plan drafted (at minimum: cadence, channel, owner)
- [ ] Dedicated program channel created (Slack, Teams, or equivalent)
- [ ] Calendar invites sent for recurring syncs (team, steering committee)

---

## Part 2: Kickoff Agenda

A kickoff does not need to be long. 90 minutes is usually enough for most programs. Two hours for complex multi-team programs. More than two hours and you are probably covering things that belong in working sessions, not kickoffs.

**Recommended agenda:**

| Time | Topic | Owner | Notes |
|------|-------|-------|-------|
| 0:00 - 0:10 | Introductions and context | TPM | Who is in the room and why |
| 0:10 - 0:25 | Problem statement and strategic alignment | PO | Why are we doing this |
| 0:25 - 0:45 | Scope, objectives, and Definition of Done | TPM + PO | What are we building and what does done look like |
| 0:45 - 1:00 | Roles and RACI | TPM | Who owns what |
| 1:00 - 1:20 | Plan, milestones, and dependencies | TPM | How we are going to get there |
| 1:20 - 1:30 | Working norms | TPM | How the team will operate |
| 1:30 - 1:45 | Risks and open questions | All | What are we worried about |
| 1:45 - 2:00 | Q&A and next steps | TPM | Close with clarity |

**Record the kickoff.** Async team members, future joiners, and anyone who needs to ramp up later will thank you.

---

## Part 3: What to Cover in Each Section

### Problem Statement and Strategic Alignment

This is the most important part of the kickoff and the one most often glossed over. The team needs to understand not just what they are building but why it matters. Engineers who understand the business problem make better technical decisions than engineers who are handed a spec.

Cover:
- The specific problem or risk being addressed
- Why it matters to the business now
- What happens if the program does not succeed
- How it connects to the organization's current priorities

### Scope, Objectives, and Definition of Done

Be specific and leave no room for ambiguity. This is the contract.

Cover:
- Objectives with measurable targets
- Explicit in-scope and out-of-scope items
- Definition of Done at the program level and, if possible, at the milestone level
- Any known scope constraints or boundaries

If there are open scope questions, name them. Do not leave them implicit.

### Roles and RACI

Every person in the room should leave knowing what they are responsible for and who to go to for decisions. Do not read the RACI table out loud - review it at a high level, call out the decision-making structure, and confirm that everyone understands their role.

Specifically cover:
- Who is the single accountable owner for program success (usually the PO or exec sponsor)
- Who makes technical decisions (engineering lead)
- Who manages the program (TPM)
- Who escalation goes to when the team is stuck
- Which external teams the program depends on and who owns those relationships

### Plan, Milestones, and Dependencies

Walk through the milestone plan at a high level. Do not present it as fixed - present it as the current best understanding, which will be refined as the team learns more.

Specifically cover:
- The major milestones and target dates
- Known dependencies on other teams and the current status of those dependencies
- Any hard external deadlines (compliance dates, product launches, contractual obligations)
- The planning process going forward - how the team will refine the plan, who contributes, how often it gets updated

### Working Norms

This section prevents a lot of friction later. The team should agree on:

- Meeting cadence (team sync, steering committee, how decisions get made between meetings)
- Status reporting (format, frequency, channel, who reads it)
- How decisions get documented (RAID log, decision log, meeting notes)
- Communication channel and expectations (response time, what goes in Slack vs. email vs. the tracker)
- How scope changes are handled (change control process)
- How the team gives each other feedback when something is not working

These do not need to be elaborate. Five agreed principles are better than a ten-page team charter nobody reads.

### Risks and Open Questions

Do not skip this. A kickoff that ends without surfacing any risks is a kickoff that did not create enough psychological safety for people to be honest.

Run a quick risk brainstorm - five to ten minutes, everyone contributes. Log everything in the RAID log. Assign owners to the top three. The rest get monitored.

Close with explicit open questions that need to be resolved before the team can proceed, and name who is responsible for resolving each one.

---

## Part 4: Post-Kickoff - Within 48 Hours

- [ ] Kickoff notes distributed to all attendees and relevant stakeholders
- [ ] Action items from kickoff entered into the tracker with owners and due dates
- [ ] RAID log updated with risks surfaced during kickoff
- [ ] Open questions logged with owners and deadlines
- [ ] Document repository link shared in the program channel
- [ ] Charter updated to reflect any changes from kickoff discussion
- [ ] First status report scheduled

---

## A Note on Remote Kickoffs

Most of the same principles apply, with a few additions:

**Camera on.** The kickoff is the first time many team members are meeting each other. Face-to-face - even virtual face-to-face - matters for relationship building.

**Breakout rooms for working norms.** Small group discussion is more productive than plenary for working norms. Put people in groups of 4-5 for 10 minutes, then bring back the top three agreements from each group.

**Interactive elements.** A kickoff where everyone stares at a deck for 90 minutes does not build alignment. Use polls, shared docs, or a virtual whiteboard for the risk brainstorm.

**Shorter sessions.** Remote attention spans are shorter. If the kickoff needs to be more than 90 minutes, split it into two sessions with a break in between.

---

*Template version 1.0. Propose changes via pull request.*
