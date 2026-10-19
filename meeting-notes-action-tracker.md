# Meeting Notes + Action Item Tracker

A meeting that produces no written record is a meeting that happened in parallel in everyone's head - which means the decisions made, the actions assigned, and the context discussed will diverge the moment the call ends. This template fixes that.

The table below captures the three things that matter - decisions made, actions assigned, and open questions - plus any risks to log. Everything else is optional. When you want the full page of notes, with attendees, discussion points and the next meeting, use the [alternate style](#alternate-style-the-full-notes-on-one-page) at the bottom of this page.

---

## Meeting Outcomes - [Meeting Name], [Date]

| # | What | Owner | Date | Status | Notes |
|:---|:---|:---|:---|:---|:---|
| **Decisions** | | | | | |
| D1 | | | | | |
| **Action items** | | | | | |
| A1 | | | | Open | |
| **Open questions** | | | | | |
| Q1 | | | | | |
| **Risks and issues to log** | | | | | |
| R1 | | | | | |

### What goes in each column

- **#:** D for a decision, A for an action, Q for an open question, R for a risk or issue. Keep the numbers, so the next meeting can say "A3 is done".
- **What:** the decision as decided, the task as it will be done, the question as asked, or the risk as described.
- **Owner:** one named person, not a team. For a decision, the person who made it.
- **Date:** when a decision takes effect, when an action is due, or when a question should be answered. An estimate is fine; say it is one.
- **Status:** for actions, Open / In Progress / Complete / Blocked / Cancelled. For questions, the resolution once there is one.
- **Notes:** for a decision, the reasoning. For a risk, whether it is in the RAID log. For anything else, what the next reader needs.

---

## How to Fill It In

Fill this in during the meeting, not after. Circulate it within 24 hours. Put the action items in your tracker before you close the document.

**Decisions first.** The most important section. Every decision should have a clear statement of what was decided, who decided it, and what evidence or reasoning drove the decision. Ambiguous decisions are the ones that get relitigated. If no decisions were made, say so: "No decisions made in this meeting - discussion only" is useful information. It tells anyone reading the notes that this was an input session, not a decision session.

**Actions next.** Every action item needs three things: a specific task, a named owner (one person, not a team), and a due date. An action item without any of these three isn't an action item - it's a suggestion.

**Read the actions back before everyone leaves.** At the close of every meeting, read the action items back out loud. Confirm the owner, the due date, and that the task is specific enough to be completable. If someone isn't sure what "own" means for their action item, it's not specific enough.

**Then the open questions.** Questions that came up in the meeting but were not resolved. Every open question needs an owner responsible for getting it answered and a target date.

**Then the risks.** Any risks or issues that came up in the discussion that need to be logged in the RAID log.

**For a recurring meeting, keep a running list.** Maintain a running list of all open action items. Update status at each meeting. Close items when complete - do not delete them. At the start of every meeting, run through open action items from the last session before covering new business. Items that are consistently Open and overdue need a conversation about whether they're real commitments or aspirations. The table is in [Reference](#running-action-item-tracker).

---

## What to Learn From

### Unknown vs Actionable

The same action item, written two ways:

| | # | What | Owner | Date | Status | Notes |
|:---|:---|:---|:---|:---|:---|:---|
| **Unknown** | A3 | Look into the certificate renewal issue | Security team | ASAP | Open | |
| **Actionable** | A3 | List the services still using the expiring intermediate certificate, from the certificate inventory scan, and send the list to the platform team so they can rotate before it expires on Nov 15 | Priya (Security) | Thu, Oct 22 | Open | Date is her estimate; she will say by Tuesday if it moves |

A good action item answers the same questions as any report: **who** (one named person), **what** (a task that can be finished), **when** (a date, even an estimate), **where** (which systems), **why** (what it unblocks or prevents), and **how** (the source or method). In the unknown one, nobody can tell who will do what or by when, so nobody acts on it. The actionable one can be checked done or not done at the next meeting.

### Where This Breaks

- **Actions that roll from meeting to meeting.** An item open for three meetings is stuck. Escalate it, or close it on purpose and say why.
- **Notes nobody reads past the first paragraph.** If the decisions and actions sit below the discussion, most people never reach them.
- **Waiting for the full picture before writing it down.** An action with a gap ("owner to be confirmed by Friday") is still worth listing, so nobody forgets it and everyone can see it.

### Tips for Good Meeting Notes

**Capture during, not after.** Notes written from memory an hour later are reconstructions, not records. Whoever is taking notes should be typing in real time - even rough notes taken live are more accurate than polished notes written later.

**One notes owner per meeting.** Rotating note-taking responsibility is fine. Shared note-taking in a shared doc is fine. No assigned owner is not fine.

**Lead with decisions, not discussion.** The people reading the notes after the meeting care most about what was decided and what they need to do. Put that first.

**Do not record everything.** A verbatim transcript is not meeting notes. Capture the signal - decisions, actions, open questions, key context. Leave out the back-and-forth that led there.

**Circulate within 24 hours.** Notes that circulate a week later aren't useful. Same-day is ideal. Next day is acceptable. After that, the value degrades fast.

**Follow up on action items.** The notes are only as useful as the follow-through. If action items aren't tracked and reviewed at the next meeting, the meeting notes become a historical record rather than an operational tool.

---

## Reference

### Running Action Item Tracker

For recurring meetings. Update status at each meeting. Close items when complete - do not delete them.

| # | Action Item | Owner | Due Date | Status | Date Closed | Notes |
|:---|:---|:---|:---|:---|:---|:---|
| | | | | | | |

---

## Alternate Style: The Full Notes on One Page

Use this when the meeting needs a full record: who was there, what was discussed, and what comes next. Copy the block into the meeting's notes file.

```markdown
# [Meeting Name] - [Date]

| Field | Detail |
|:---|:---|
| Meeting | [Name / purpose] |
| Date | |
| Time | |
| Facilitator | |
| Notes Owner | |
| Attendees | |
| Absent (expected) | |

## Purpose
[One sentence: what was this meeting trying to accomplish?]

## Decisions Made
| # | Decision | Decision Maker | Rationale | Effective Date |
|:---|:---|:---|:---|:---|
| D1 | | | | |
| D2 | | | | |

## Action Items
| # | Action Item | Owner | Due Date | Status | Notes |
|:---|:---|:---|:---|:---|:---|
| A1 | | | | Open | |
| A2 | | | | Open | |

## Key Discussion Points
[Enough context for someone who wasn't in the meeting to understand what was covered. Not a transcript. Three to eight bullet points for most meetings.]
- [Discussion point 1]
- [Discussion point 2]
- [Discussion point 3]

## Open Questions
| # | Question | Owner | Target Date | Resolution |
|:---|:---|:---|:---|:---|
| Q1 | | | | |

## Risks and Issues Surfaced
| Item | Type | Description | Owner | RAID Log Entry? |
|:---|:---|:---|:---|:---|
| | Risk / Issue | | | Yes / No |

## Next Meeting
| Field | Detail |
|:---|:---|
| Date / Time | |
| Purpose | |
| Prep required | |
| Pre-read to distribute | |

## Distribution
Circulate these notes to: [attendees + relevant stakeholders who weren't present]
```

---

*Template version 1.1. Propose changes via pull request.*
