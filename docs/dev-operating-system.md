# Corbyn Development Operating System

This is the working model for using Hermes, Linear, GitHub, Cursor, and Codex together.

## Goal

Keep Corbyn focused on product judgement, client relationship, and approval while Hermes handles intake, planning, orchestration, review, and reporting.

## Source of truth

Linear is the source of truth for active work.

GitHub is the source of truth for code and reviewable change.

`project-update-reports` is the source of truth for client/stakeholder progress reports.

## Default workflow

1. Intake
   - Input can come from Telegram, Discord, Freddie/Mike comments, screenshots, repo TODOs, or Corbyn's ideas.
   - Hermes converts messy input into a short interpretation and identifies ambiguities.

2. Planning
   - Hermes creates either:
     - a small Linear issue, or
     - a brief/plan if the task is bigger than one agent-sized issue.
   - Bigger work is split into small implementation issues with acceptance criteria.

3. Assignment
   - Use labels to route work:
     - `agent:cursor` — scoped UI/feature work for Cursor Cloud/local Cursor
     - `agent:codex` — deeper bug investigation, architecture, backend, review
     - `agent:hermes` — orchestration, reviews, docs, tests, small direct changes
     - `needs-review` — ready for review
     - `client-facing` — should appear in updates
     - `blocked` — needs decision/access/input
     - `scope-risk` — may exceed agreed scope
     - `compliance` — finance/legal wording sensitive
     - `design-polish` — UI/copy/visual judgement

4. Execution
   - Cursor handles small scoped build tasks.
   - Codex handles isolated investigation/review/backend tasks.
   - Hermes handles glue, repo checks, Linear hygiene, docs, reports, and direct small edits.

5. Review
   - Hermes reviews diffs/commits against acceptance criteria.
   - Hermes runs available tests/builds where possible.
   - Corbyn makes final merge/deploy/client judgement.

6. Reporting
   - Hermes generates draft stakeholder reports every two days.
   - Reports are draft-only until Corbyn approves them.
   - Client-sent wording should be plain-language and avoid implementation noise unless relevant.

## Linear issue size rule

An issue assigned to Cursor Cloud should be small enough that:

- it has one clear outcome;
- acceptance criteria fit in a short list;
- it can be reviewed in under 10 minutes;
- it does not require major product judgement mid-task.

If it is bigger, Hermes should split it first.

## Linear issue template

```markdown
## Outcome
[What should be true when this is done]

## Context
[Why this matters, links/screenshots if relevant]

## Acceptance criteria
- [ ] ...
- [ ] ...
- [ ] ...

## Not in scope
- ...

## Suggested agent
Cursor / Codex / Hermes

## Test/review notes
- Run/check ...
```

## Review checklist

Before merge/deploy:

- Does the change satisfy the Linear acceptance criteria?
- Did it avoid scope creep?
- Does it preserve client/compliance-sensitive wording?
- Is the UI acceptable visually, not just functionally?
- Were tests/build/lint run where available?
- Is there anything client-facing worth mentioning in the next update?

## Reporting cadence

Start with draft-only reports every 2 days to Telegram.

Each report should include:

- what changed;
- why it matters;
- currently in progress;
- blockers or decisions needed;
- links/source activity for Corbyn, not necessarily for clients.

Do not auto-send to Freddie or Mike until the report format has been trusted over several cycles.
