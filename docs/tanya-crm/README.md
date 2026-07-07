# Takoy Designs CRM — Planning Documentation

Build-ready planning spec for the custom CRM / operations web app being built by
**Web Launch Pros** for **Takoy Designs** (Tanya Koyle — custom window treatments,
in-home sales, Boise / Eagle, ID).

This doc set converts three client calls (May discovery, June 11 proposal/close,
June 22 build check-in) plus the demo/mockup screenshots into a single source of
truth a builder (AI or human) can execute against.

## Start here

**[Client-Software-Planning-Package.md](./Client-Software-Planning-Package.md)** is the primary,
consolidated deliverable — the full 28-section software planning package (executive summary →
current/future workflows → personas → user stories → FR/NFR with acceptance criteria → screens →
data model → statuses → automations → integrations → reporting → notifications → testing → MVP →
phased roadmap → risks → assumptions → next steps → conflicts), built to the client planning SOP.

The numbered docs below are **supporting detail** referenced by the master package.

## Supporting docs

| # | Doc | What it covers |
|---|-----|----------------|
| 00 | [Overview](./00-overview.md) | Business context, goals, team, scope (bought vs. deferred), glossary |
| 01 | [Product Plan](./01-product-plan.md) | How it works when done — user journeys + page-by-page layouts, buttons |
| 02 | [Process Plan](./02-process-plan.md) | How we build it — stack + ordered build/prompt sequence |
| 03 | [Functional Requirements](./03-functional-requirements.md) | Every button/control, ID'd (FR-###) |
| 04 | [Non-Functional Requirements](./04-non-functional-requirements.md) | Hosting, speed, security, SMS compliance, reliability |
| 05 | [Data Model](./05-data-model.md) | Objects, relationships, ER diagram, People/Events hierarchy |
| 06 | [Roles & Permissions](./06-roles-and-permissions.md) | Who can do what → RLS policy map |
| 07 | [Open Questions](./07-open-questions.md) | Missing variables / decisions still needed before build completes |

`assets/` holds the real demo screenshots referenced throughout (extracted from the call PDFs).

## Scope at a glance

- **In scope now (purchased "Operating System" package):** one unified team calendar,
  lead pipeline / conversion tracking, text + email appointment reminders, metrics
  dashboard + weekly scorecard, ClickUp auto-project on booking, per-person time-off
  blocking, mobile-friendly web app, Google/Apple calendar sync.
- **Future phases (documented, not built yet):** AI receptionist, voice triage,
  unified social/email/SMS inbox, public self-booking links, custom quoting.

> Every requirement in these docs is tagged with its source call so you can trace it
> back: **[C1]** = May discovery, **[C2]** = June 11, **[C3]** = June 22.
