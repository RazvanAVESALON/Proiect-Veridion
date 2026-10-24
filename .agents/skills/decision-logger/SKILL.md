---
name: decision-logger
description: >-
  Use this skill to systematically document and log every methodological, technical,
  architectural, and sampling decision made during the project into DECISIONS.md.
  Ensures defensibility, auditability, and feeds directly into the final Deliverable
  README and Cut List.
---

# Decision Logger Skill (Economic & Technical ADR System)

This skill enforces a rigorous audit trail of all choices, trade-offs, discarded alternatives, and rationale throughout the Veridion Economic Data Science project.

## Core Purpose
The client's auditors and analysts do not accept "we googled it" or unrecorded intuition.
Every decision must be recorded so that:
1. Every figure and proxy has a clear derivation history.
2. Discarded approaches and dead ends are captured directly for the **Cut List**.
3. Decisions are structured like Architecture Decision Records (ADR).

---

## The Decision Log File: `DECISIONS.md`

All decisions must be appended to [DECISIONS.md](file:///d:/Proiect%20Veridion/DECISIONS.md) in the project root.

### Entry Format Schema

Each decision entry must follow this standardized template:

```markdown
### [DEC-XXX] <Concise Title of the Decision>
- **Date & Phase:** YYYY-MM-DD | Phase (e.g., Part 1: Sample Selection, Part 2: Proxy Estimation)
- **Status:** [PROPOSED | ACCEPTED | SUPERSEDED | REJECTED]
- **Context & Problem Statement:** What problem or dilemma prompted this decision?
- **Decision Taken:** What exact path, method, formula, or subset did we choose?
- **Alternatives Considered & Discarded:**
  - *Option B:* Why was it rejected? (Feasibility, noise, unreliability at scale)
  - *Option C:* Why was it rejected?
- **Rationale & Evidence:** Why does this decision stand scrutiny across the table?
- **Assumptions & Downstream Impact:**
  - What assumptions are we relying on?
  - How wrong could this be? (Uncertainty bounds)
  - Does this feed the "Cut List" or "Dead Ends" section?
```

---

## Workflow Instructions for the Agent

1. **Trigger Condition:** Whenever a strategic, methodological, or data-filtering decision is agreed upon with the user (e.g., selecting the sample, choosing Detective Route over Quant, selecting specific proxies, defining entity resolution rules):
   - Update or append the decision into [DECISIONS.md](file:///d:/Proiect%20Veridion/DECISIONS.md).
   - If an earlier decision is modified, update its status to `SUPERSEDED` and link the new decision ID.
2. **Sync with Cut List:** Any discarded methodology, unused data source, or de-prioritized step must explicitly note whether it enters the final deliverable's *Cut List*.
3. **Notify User:** In the response, confirm that the decision has been permanently logged with its ID.
