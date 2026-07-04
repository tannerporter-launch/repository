# Client Software Planning Package — Takoy Designs Operations CRM

**Client:** Takoy Designs (Tanya Koyle) · **Builder:** Web Launch Pros (Tanner Porter)
**Prepared from:** three client calls — May discovery (phone), June 11 proposal/close (Zoom),
June 22 build check-in (Zoom) — plus the demo/mockup screenshots in `assets/`.

**Evidence labels used throughout:** `Confirmed by transcript` · `Strongly implied by transcript`
· `Internal recommendation` · `Needs client confirmation` · `Future phase candidate`.
Call tags: **[C1]** May · **[C2]** June 11 · **[C3]** June 22.

> This is the consolidated, SOP-structured package. The numbered docs (`00`–`07`) in this folder
> remain as supporting detail; this file is the single source of truth and follows the planning SOP's
> 28-section format.

---

## 1. Executive Summary

Takoy Designs is a 10-year custom window-treatment business doing ~$2.8M/year through **in-home
sales**, run by owner Tanya Koyle with a small team (one admin, two sales reps, a remote assistant,
and external install subcontractors). The business is healthy but **leaks revenue at the front door**:
there is no shared calendar, so whoever answers a call usually can't see the reps' availability and
has to say "let me have someone call you back" — and those callbacks are where leads die. Tanya
estimates **~1 lead/week (4–5/month)** lost this way, at an **average project value around $6,000**,
plus roughly **an hour a day per person** wasted on scheduling ping-pong. She also has **no
conversion tracking** at all. `Confirmed by transcript` [C1][C2].

**What she needs:** one mobile-friendly web app that gives the whole team **a single shared calendar**
and a **live pipeline view**, so anyone can book a customer while they're still on the phone and
nothing slips through the cracks. It must sit *in front of* the tools she keeps — ClickUp (project
management) and personal Google/Apple calendars — not replace them. `Confirmed by transcript` [C1][C2][C3].

**First version focus (MVP):** the unified team calendar + live appointment booking (with
double-booking protection) — the piece that directly stops the "call-you-back" losses. Conversion
tracking, text/email reminders, calendar sync, ClickUp auto-project, and the weekly scorecard follow
immediately after within the same ~30-day build. `Confirmed by transcript` [C2].

**Explicitly deferred:** custom quoting (supplier pricing is too fluid/inconsistent to automate
reliably), plus optional add-ons — AI receptionist, voice triage, and a unified social/email/text
inbox. `Confirmed by transcript` [C1][C2][C3].

**Success looks like:** the office can book any lead live on the first call; Tanya can see every
team member's schedule and the inquiry→consult→quote→won funnel in one place; and the ~1 lost
lead/week trends toward zero. `Strongly implied by transcript` [C1][C2].

**Commercial status:** the "Operating System" package is **sold and paid** ($9,800 list; negotiated
bank-transfer total ~$9,506; 50% upfront; ongoing support moved to on-demand). `Confirmed by transcript` [C2].

---

## 2. Client Context

### 2.1 Company Overview

| | |
|---|---|
| **Company** | Takoy Designs |
| **Owner** | Tanya Koyle |
| **Industry** | Home services — custom window treatments (blinds, cellular/Roman shades, shutters, motorized) |
| **Business model** | Fully **custom, in-home** sales (no storefront); orders from all major suppliers with own margins/markups |
| **Market** | Boise / Eagle / Meridian, Idaho; Mountain Time; residential-primary, some builder work |
| **Scale** | ~$2.8M last year → **$3M goal**; avg project ~$6,000; social-lead close rate ~30–50% |
| **Lead sources** | Instagram ads (primary focus), Facebook, Google/website, referrals, builders, Houzz, repeat clients |
| **Current tools** | ClickUp (PM), a separate quoting tool (~$250/mo), Google Calendar, Apple/iCal (Tanya personal), QuickBooks + spreadsheet (commissions) |
| **Background** | 10 years independent; strong supplier relationships; cautious about scaling and about over-automating |

`Confirmed by transcript` [C1][C2][C3].

### 2.2 Business Goals

- Stop losing leads to the "call-you-back" gap (reduce missed/lost leads). `Confirmed` [C1]
- Give the whole team live visibility into everyone's schedule. `Confirmed` [C1][C3]
- Let the office book appointments live, on the first call. `Confirmed` [C1]
- Get real conversion metrics (inquiry → consult → quote → won). `Confirmed` [C1][C2]
- Increase owner visibility, including a new salesperson's numbers "without hovering." `Confirmed` [C2]
- Reduce the ~1 hour/day/person scheduling waste. `Confirmed` [C1]
- Reach $3M without proportionally adding chaos; smooth process before hiring a 2nd salesperson. `Confirmed` [C1][C2]
- Keep run-cost modest and avoid another cumbersome tool. `Confirmed` [C1][C2]

### 2.3 Current Pain Points (by category)

**Scheduling / Lead handling — the core pain.**
- *Now:* No shared calendar; admin can't see reps' availability, so live booking is impossible —
  "let me have someone call you back." *Why it matters:* callbacks are where leads die; ~1/week lost.
  *Who:* Nissa (admin), reps, and ultimately Tanya (revenue). *System should:* one calendar all can see
  + live booking. `Confirmed` [C1][C3]

**Revenue leakage / Reporting.**
- *Now:* No conversion tracking; Tanya "doesn't even know how to start." *Why:* can't see lost
  opportunity or ROI on ad spend. *Who:* Tanya. *System should:* pipeline funnel + falling-through list. `Confirmed` [C1][C2]

**Manual work / Owner visibility.**
- *Now:* ~1 hr/day/person on scheduling shuffle; Tanya wears every hat and wants to delegate without
  losing oversight. *Why:* wasted time; owner can't safely hand off. *System should:* shared views +
  weekly scorecard. `Confirmed` [C1][C2]

**Software fragmentation.**
- *Now:* ClickUp + separate quoting tool + Google Calendar + QuickBooks/spreadsheet, none integrated.
  *Why:* info gaps, duplicate entry, manual follow-ups. *System should:* sit in front of ClickUp +
  calendars, one place to work. `Confirmed` [C1]

**Communication.**
- *Now:* Reminders/follow-ups are ad hoc; email gets ignored. *Why:* no-shows, missed follow-ups.
  *System should:* automated **text** + email confirmations/reminders. `Confirmed` [C2][C3]

**Quoting (noted, deferred).**
- *Now:* Quoting tool is cumbersome; supplier prices change 2–3×/yr in inconsistent formats; Tanya
  doesn't trust automating it. *System should:* **not** automate quoting now. `Confirmed` [C1][C2]

---

## 3. Current-State Workflow (as-is)

1. **Lead comes in** — Instagram/Facebook ad, Google/website, referral, or builder. *Tool:* phone /
   DM / ClickUp intake. *Manual:* Tanya manually logs Instagram leads into ClickUp, which flags
   Carolyn to call. *Failure points:* social leads are "cold," unqualified; some never get logged.
   *People:* Tanya, whoever answers. `Confirmed` [C1]
2. **Call answered** — "they all get answered." *Tool:* phone. *Manual:* intake depth depends on who
   answers (a rep gets full detail; the admin gets a few questions). *Info gap:* budget/timeline not
   consistently captured; often not written down. *People:* Nissa or a rep. `Confirmed` [C1]
3. **Try to book a consult** — *Failure point (the big one):* if the **admin** answers, she can't see
   rep availability, so she says "she'll call you back to schedule." *Tool:* Google Calendar (siloed
   per person). *Result:* callback delay or never happens → **~1 lead/week lost**. *People:* Nissa. `Confirmed` [C1][C3]
4. **In-home consult** — rep measures windows, discusses design, builds a quote. *Tool:* the separate
   quoting software. *Manual/failure:* prices sometimes look wrong, so the rep can't finalize in-home
   and must re-check the catalog later. *People:* Carolyn/Tracy/Tanya. `Confirmed` [C1]
5. **Quote sent** — room-by-room pricing emailed to the customer. *Tool:* quoting tool → email.
   *Manual:* markup/margin applied; formatting fiddly. `Confirmed` [C1]
6. **Job won → order → install** — order placed with suppliers; external subcontractors install.
   *Tool:* ClickUp moves the project through stages. *People:* Tanya + subs. `Confirmed` [C1][C2]
7. **Follow-up** — ad hoc; no systematic follow-up on un-booked or un-closed leads. *Failure:* leads
   "fall through the cracks." `Confirmed` [C1]
8. **Reporting / commissions** — run in QuickBooks + a spreadsheet with a bookkeeper. *Manual:* fully
   manual; conversions not tracked at all. *People:* Tanya + bookkeeper. `Confirmed` [C1]

**Where information gets lost / depends on memory:** intake details between call and consult;
whether a callback happened; which un-booked leads still need follow-up; conversion outcomes.

---

## 4. Future-State Workflow (to-be)

Each step: **Trigger → User action → System action → Automation → Data captured → Status change →
Notification → Result.**

1. **Lead calls or DMs.** *User:* any staff opens the app on phone/desktop → Calendar. *System:*
   shows the unified team calendar with open slots. *Result:* whoever answers can act immediately.
   `Confirmed` [C1][C3]
2. **Book live on the first call.** *User:* taps **+ New appointment** (or an open slot) → searches or
   creates the client → sets type, assigned rep, start/end, budget tier, property type, address,
   notes → **Book**. *System:* writes the appointment, **blocks double-booking the same rep**.
   *Automation:* sends **text + email confirmation**; **auto-creates a ClickUp project**. *Data:*
   client, budget tier, property type, source, type, assignee. *Status:* Inquiry → **Consult booked**.
   *Notification:* customer confirmation; rep notified of assignment. *Result:* no "call-you-back";
   lead captured while warm. `Confirmed` [C1][C2][C3]
3. **Reminders fire.** *Trigger:* appointment approaching. *Automation:* scheduled **text + email**
   reminder (respecting Mountain-Time quiet hours). *Result:* fewer no-shows. `Confirmed` [C2][C3]
4. **Consult happens.** *User:* rep views the appointment side-panel (customer phone/email/address/
   notes), completes the visit, records outcome + **quote sent + amount** (manual field). *Status:*
   Consult booked → **Quote sent**. *Result:* pipeline reflects quoting activity without a quoting engine.
   `Confirmed` [C1][C2]
5. **Won / lost.** *User:* marks the appointment **Won** (+ value) or lost. *Status:* Quote sent →
   **Won** (or Lost). *System:* funnel + Won Value update. *Result:* real close-rate visibility. `Strongly implied` [C2][C3]
6. **Nothing falls through.** *Trigger:* an inquiry has no booked/active consult and stale contact.
   *System:* surfaces it in the **Falling-through** list with days-since-contact. *User:* clicks to
   **text/email** or book. *Result:* systematic follow-up. `Confirmed` [C3]
7. **Time off.** *User:* a rep adds a vacation/personal block in settings. *System:* shows
   **"Unavailable — reason"** to the team and prevents booking, **without** exposing personal event
   detail. *Result:* accurate availability. `Confirmed` [C3]
8. **Owner oversight.** *Automation:* **weekly scorecard email** to Tanya (per-salesperson).
   *Result:* she sees numbers, including a new hire's, without hovering. `Confirmed` [C2]
9. **Calendar sync.** *System:* two-way Google sync; personal busy blocks appear as "Unavailable";
   Tanya keeps viewing personal events in Apple/iCal. *Result:* no conflicts, existing habits intact.
   `Confirmed` [C2][C3]

**What becomes easier/automated/visible:** live booking, double-booking prevention, confirmations +
reminders, ClickUp project creation, conversion metrics, follow-up, availability — all in one
mobile-friendly place.

---

## 5. User Roles and Permissions

> Two governing decisions: **no role-based differentiation on the calendar** — everyone sees
> everything and any staff can take any appointment type `Confirmed` [C3]; and **config/field editing
> is restricted to the owner** for data integrity `Confirmed` [C2].

| Role | Responsibilities | Needs to See | Needs to Do | Permissions | Notes |
|---|---|---|---|---|---|
| **Owner / Admin (Tanya)** | Runs everything; oversight | Entire calendar, full pipeline, scorecard, all client data | Everything staff can do + edit config (types/sources/tiers/fields), manage staff, integrations | Full access | Only role that edits configuration [C2] |
| **Staff — Admin/Booking (Nissa)** | Answers phones, books appts | Whole team calendar, availability, pipeline | Create/edit/cancel any appt, assign any rep, text/email leads, manage own time-off | Full day-to-day; **no** config edit | Primary booker; the "call-you-back" pain is hers [C1] |
| **Staff — Sales (Carolyn, Tracy)** | In-home consults, quotes | Whole team calendar, own + others' appts, pipeline | Same as above; record quote/won | Full day-to-day; no config edit | "Mostly sales" but wants full visibility [C3] |
| **Assistant (remote student)** | Support tasks | Calendar, pipeline | Create appts / support booking | Day-to-day view + create; **no** manage-staff/config; (destructive-edit scope TBD) | Limited tier — see Open Questions [C2] |
| **External — Subcontractor (installers)** | Installations | (Core: none in-app) | — | Stored as records; no login in MVP | Future: possible read-only install view [C2] |
| **External — Customer** | Receives service | (Future) self-book page only | (Future) self-book certain appt types | No login in MVP | Future self-booking, per-type opt-in [C1][C2] |

---

## 6. User Personas

### Persona: Tanya — Owner
**Primary goal:** Grow to $3M and delegate safely without losing visibility.
**Current frustrations:** Wears every hat; no conversion data; can't see the whole team's schedule;
burned out on scheduling shuffle. `Confirmed` [C1][C2]
**Needs from the system:** One calendar for the whole team; pipeline + weekly scorecard; owner-only
control of config; keep ClickUp + her Apple calendar.
**Important workflows:** Oversight (Who=Everyone), pipeline review, weekly scorecard, config setup.
**Success looks like:** Sees every rep's day and the funnel at a glance; a new hire's numbers are
visible automatically.

### Persona: Nissa — Admin / Booker
**Primary goal:** Book every caller on the first call.
**Current frustrations:** Can't see rep availability → forced "call-you-back" → lost leads. `Confirmed` [C1]
**Needs from the system:** Live team availability; fast New-Appointment flow; double-booking guard;
one-tap text/email.
**Important workflows:** J1 inbound→booked; falling-through follow-up.
**Success looks like:** Never says "we'll call you back to schedule" again.

### Persona: Carolyn / Tracy — Sales Rep
**Primary goal:** Run consults efficiently in the field.
**Current frustrations:** Siloed calendars; can't trust in-home pricing; details lost between call and visit. `Confirmed` [C1]
**Needs from the system:** Mobile calendar; appointment side-panel with customer contact/address/notes;
record quote/won.
**Important workflows:** J2 rep's day; consult → quote sent → won.
**Success looks like:** Opens the phone, sees the day, taps a job for everything needed.

### Persona: Remote Assistant
**Primary goal:** Help with booking/support without breaking anything.
**Needs:** View calendar + pipeline; create appointments.
**Success looks like:** Contributes to booking without access to config/staff settings. `Strongly implied` [C2]

---

## 7. User Stories (with acceptance criteria)

### Owner (Tanya)
**US-O1 — See the whole team on one calendar.** *As an owner, I want to view all staff appointments
on one calendar filtered by person and type, so that I have full visibility.*
- AC: Who filter defaults to Everyone; toggling a person shows/hides their appts; What filter narrows
  by type; changes persist on refresh; works on mobile. `Confirmed` [C3]

**US-O2 — Weekly scorecard.** *As an owner, I want an automatic weekly performance email, so that I
track results (incl. a new hire's) without hovering.*
- AC: Email sent weekly; includes inquiries, set rate, quotes sent, jobs won, $ sold; broken down per
  salesperson; totals reconcile with the pipeline. `Confirmed` [C2]

**US-O3 — Owner-only configuration.** *As an owner, I want only me to edit appointment types, referral
sources, budget tiers, and fields, so that data stays clean.*
- AC: Non-owners can't see/reach Setup; API/RLS rejects non-owner writes to config tables. `Confirmed` [C2]

### Admin / Booker (Nissa)
**US-A1 — Book live on the call.** *As a booker, I want to create an appointment while the customer is
on the phone, so that I never lose them to a callback.*
- AC: New-Appointment opens from the calendar; search or create a client; set type/assignee/time/
  budget/property/address/notes; Book writes it and it appears immediately; disabled until required
  fields set; persists on refresh. `Confirmed` [C1][C3]

**US-A2 — Prevent double-booking.** *As a booker, I want the system to stop me from booking a rep who's
already busy, so that the schedule stays accurate.*
- AC: Booking an overlapping time for the same assigned rep is rejected with a clear message; a
  non-overlapping time succeeds; time-off blocks also prevent booking. `Confirmed` [C3]

**US-A3 — Follow up on leads that stalled.** *As a booker, I want a list of inquiries with no consult
booked and how long they've gone cold, so that I can follow up.*
- AC: List shows name, source·city·budget, days-since-contact; each row can email/text or book; a
  newly booked lead leaves the list. `Confirmed` [C3]

### Sales Rep (Carolyn / Tracy)
**US-S1 — See my day on my phone.** *As a rep, I want a mobile calendar filtered to me, so that I can
run my day.*
- AC: Who=self shows only my appts; tapping one opens the side-panel with customer phone/email/
  address/notes; phone/email are tap-to-contact; usable at 375px width. `Confirmed` [C3]

**US-S2 — Record consult outcome.** *As a rep, I want to mark quote sent (+amount) and won (+value), so
that the pipeline reflects reality.*
- AC: Setting Quote sent + amount moves status and feeds Avg Quote; Won + value feeds Won Value;
  changes persist. `Strongly implied` [C2][C3]

### Assistant
**US-X1 — Help book without admin power.** *As an assistant, I want to view the calendar/pipeline and
create appointments, but not change settings.*
- AC: Can create appts; cannot open Setup or manage staff; (edit/cancel-others scope per Open Questions). `Strongly implied` [C2]

---

## 8. Functional Requirements

Priority key: **MVP** (needed to solve the core pain) · **Soon** (same ~30-day build, right after MVP)
· **Future** (documented add-on). MVP/Soon items carry full acceptance criteria; Future items are
summarized in the compact table at the end.

### FR-001: Unified team calendar with Who/What filters
**Description:** One calendar showing all staff appointments, filterable by team member (Who) and
appointment type (What), with day/week views and date navigation.
**Primary role:** All internal. **Priority:** MVP.
**Acceptance criteria:**
- Who defaults to "Everyone"; per-person checkboxes with color dots filter the grid.
- What offers "All types" + each configured type; filters combine with Who.
- Day/Week toggle; Today + prev/next navigation.
- Appointments are color-coded by type and labeled `Type · Client`.
- Filter state persists on refresh; renders correctly at 375px.
**Evidence:** `Confirmed by transcript` — "one calendar that has us all on it… see what everybody's doing" [C3]; matches `assets/demo-jun22-calendar-sidepanel.png`, `assets/slide-layer1-one-calendar.png`.

### FR-002: Create appointment (New Appointment modal)
**Description:** Create an appointment capturing client (existing or new), type, assigned staff,
start/end, budget tier, property type, title, address, notes.
**Primary role:** All internal. **Priority:** MVP.
**Acceptance criteria:**
- Client typeahead by name/phone/email; "Or create a new client" adds name/phone/email inline.
- Assigned-to lists all staff (any staff, any type).
- Budget tier options: Under $2k / $2–5k / $5–10k / $10k+.
- Book is disabled until required fields (client, type, assignee, start, end) are set.
- On Book, the appointment appears on the calendar immediately and persists on refresh.
**Evidence:** `Confirmed by transcript` [C3]; matches `assets/demo-jun22-new-appointment-modal.png`.

### FR-003: Prevent double-booking the same staff member
**Description:** Block creating/editing an appointment that overlaps another for the same assigned staff.
**Primary role:** All internal. **Priority:** MVP.
**Acceptance criteria:**
- Overlapping time for the same assignee is rejected with a clear message.
- Non-overlapping succeeds; different staff at the same time is allowed.
- Active time-off for that staff also blocks booking.
**Evidence:** `Confirmed by transcript` — modal states it "blocks double-booking the same staff member" [C3].

### FR-004: Appointment side-panel (view/edit)
**Description:** Clicking an appointment opens an editable side-panel with Title/Start/End/Address/Notes
and a read-back of the **customer's** phone/email/status.
**Primary role:** All internal. **Priority:** MVP.
**Acceptance criteria:**
- Editable fields save via Save changes and persist.
- Cancel appointment voids it and frees the slot.
- Contact shown is the customer's (not the assigned rep's); phone/email are tap-to-contact.
**Evidence:** `Confirmed by transcript` — "click on the appointment… edited on the side… phone, email, status… of the actual customer" [C3]; `assets/demo-jun22-calendar-sidepanel.png`.

### FR-005: Book by tapping an open slot
**Description:** Tapping empty calendar space opens the New Appointment modal pre-filled with that
date/time (and staff column).
**Primary role:** All internal. **Priority:** MVP.
**Acceptance criteria:** Selecting a slot pre-populates start/end; user completes and books; result lands in the tapped slot.
**Evidence:** `Confirmed by transcript` — "select a spot which will then pop this up" [C3].

### FR-006: Per-person time-off / vacation blocking
**Description:** Each staff member can block a day/week as unavailable with a reason, shown to the team
without exposing personal event detail.
**Primary role:** All internal (own). **Priority:** MVP.
**Acceptance criteria:**
- Add/remove a start–end block with reason (Vacation/Personal).
- Renders as "Unavailable — reason" to everyone; blocks booking in that range.
- Personal calendar event details are not exposed.
**Evidence:** `Confirmed by transcript` — "put in vacation time so… 'Oh, Nissa's on vacation'… block out a full day or week" [C3].

### FR-007: Pipeline dashboard + conversion metrics
**Description:** A pipeline view (last 30 days) with KPI tiles (Set Rate, Avg Quote, Won Value,
Falling-Through count), a funnel (Inquiries → Consults Booked → Quotes Sent → Won), and Top Sources.
**Primary role:** Owner, Staff. **Priority:** Soon.
**Acceptance criteria:**
- KPIs compute from live data; funnel counts match underlying records.
- Top Sources reflects the configured referral-source list.
- Booking a consult moves counts from Inquiries into Consults Booked.
**Evidence:** `Confirmed by transcript` [C2][C3]; `assets/demo-jun22-pipeline-full.png`, `assets/slide-layer4-daily-metrics.png`.

### FR-008: "Falling through the cracks" follow-up list
**Description:** List inquiries with no booked/active consult, showing source·city·budget and
days-since-contact, each actionable via text/email or book.
**Primary role:** Owner, Staff. **Priority:** Soon.
**Acceptance criteria:**
- A lead with no active appointment and stale contact appears with a correct day count.
- Row actions: email, text, or open New Appointment pre-filled.
- Booking the lead removes it from the list.
**Evidence:** `Confirmed by transcript` — "who's going to be falling through the cracks… click… send them an email or a text" [C3].
**Open dependency:** how un-booked inquiries enter (manual vs. lead-form webhook vs. future inbox) — see §24/§25.

### FR-009: Text + email appointment confirmations & reminders
**Description:** On booking, send a confirmation by text and email; send scheduled reminders before the
appointment; wording configurable.
**Primary role:** System → Customer. **Priority:** Soon.
**Acceptance criteria:**
- Booking triggers a text + email confirmation.
- A reminder sends at the configured lead time; respects Mountain-Time quiet hours and STOP opt-out.
- Reminder templates editable in Setup.
**Evidence:** `Confirmed by transcript` — text prioritized for higher open rate [C2][C3].

### FR-010: ClickUp auto-project on booking
**Description:** When an appointment is booked, create a ClickUp project/task for that customer and
store the link on the appointment.
**Primary role:** System. **Priority:** Soon.
**Acceptance criteria:**
- Booking creates a ClickUp task in the configured workspace/list.
- The appointment stores the ClickUp link; failures are surfaced and retryable.
**Evidence:** `Confirmed by transcript` — decision to auto-create a ClickUp project on booking [C2].

### FR-011: Two-way Google Calendar sync
**Description:** Per-user Google sync — app appointments push out; external busy blocks appear as
"Unavailable"; Tanya continues viewing personal events in Apple/iCal.
**Primary role:** All internal. **Priority:** Soon.
**Acceptance criteria:**
- Connecting Google shows that user's external busy time as "Unavailable" on the team calendar.
- A booked appointment appears on the user's Google calendar.
- No personal event detail is exposed beyond "Unavailable".
**Evidence:** `Confirmed by transcript` [C2][C3].

### FR-012: Weekly scorecard email
**Description:** Automated weekly summary email to the owner with per-salesperson metrics.
**Primary role:** System → Owner. **Priority:** Soon.
**Acceptance criteria:** Sends weekly; includes inquiries, set rate, quotes sent, jobs won, $ sold; per-rep breakdown; totals match the pipeline.
**Evidence:** `Confirmed by transcript` [C2].

### FR-013: Admin Setup (owner-only configuration)
**Description:** Owner manages staff, appointment types (+colors), referral sources, budget tiers,
property types, field config, reminder wording, and integration settings.
**Primary role:** Owner. **Priority:** MVP (staff/types/sources/tiers) · Soon (integrations/templates).
**Acceptance criteria:**
- Owner can add/edit/remove types, sources (incl. **remove "House"**, **add "Facebook"**), tiers, property types, staff.
- Non-owners cannot access Setup (UI hidden + server rejects).
**Evidence:** `Confirmed by transcript` — remove House / add Facebook [C3]; owner-restricted fields [C2].

### FR-014: Authentication & session
**Description:** Email/password login; land on the calendar; sign out.
**Primary role:** All internal. **Priority:** MVP.
**Acceptance criteria:** Valid credentials sign in and route to Calendar; invalid rejected; sign-out ends the session; password reset available.
**Evidence:** `Confirmed by transcript` — demoed sign-in [C3]; `Internal recommendation` for reset/session details.

### FR-015: Budget-range question on the Facebook lead form
**Description:** Add a budget-range question to the Facebook/Instagram lead form to pre-qualify.
**Primary role:** Marketing/Owner. **Priority:** Soon (dependent on lead-form integration — see §14/§24).
**Acceptance criteria:** Lead form captures a budget range; value flows to the lead/inquiry record.
**Evidence:** `Confirmed by transcript` — action item for Tanya to add a budget-range question [C2].

### Compact requirements table (remaining + future)

| ID | Requirement | Role | Priority | Evidence |
|---|---|---|---|---|
| FR-016 | Record quote-sent (+amount) & won (+value) on an appointment | Staff | Soon | `Strongly implied` [C2][C3] |
| FR-017 | Appointment status field (scheduled/confirmed/completed/rescheduled/cancelled) | All internal | MVP | `Confirmed` [C3] |
| FR-018 | Client records (create/search/edit; phone/email/address/source/notes) | All internal | MVP | `Confirmed` [C3] |
| FR-019 | Mobile-web responsiveness across all screens | All | MVP | `Confirmed` [C3] |
| FR-020 | Public self-booking page (per-type opt-in) | External | Future | `Future phase candidate` [C1][C2] |
| FR-021 | Unified inbox (FB/IG DM + email + text per client) | Owner, Staff | Future | `Future phase candidate` [C2][C3] |
| FR-022 | AI receptionist (after-hours answer + intake + self-book offer) | System | Future | `Future phase candidate` [C2][C3] |
| FR-023 | Voice triage | System | Future | `Future phase candidate` [C3] |
| FR-024 | Custom quoting engine | Staff | Out of scope | `Confirmed` deferred [C1][C2] |
| FR-025 | Commission tracking | Owner | Out of scope (MVP) | `Confirmed` stays in QuickBooks [C1] |

---

## 9. Non-Functional Requirements

### NFR-001: Mobile-first performance
**Description:** Calendar and booking must be fast on a phone in the field.
**Acceptance criteria:** Calendar first meaningful paint < ~1.5s on LTE; Book confirms < ~1s with async side-effects; filters update client-side without full reload.
**Priority:** MVP. `Confirmed` [C1][C3]

### NFR-002: Mobile responsiveness (no native app)
**Description:** Fully usable web app on phones and desktops; no app-store install.
**Acceptance criteria:** All flows usable at 375px; tap targets ≥44px; side-panel becomes a bottom sheet on small screens; no horizontal scroll.
**Priority:** MVP. `Confirmed` [C3]

### NFR-003: Security & access control
**Description:** Enforce roles server-side, not just UI.
**Acceptance criteria:** Row-Level Security enforces internal-read / owner-only-config; secrets stored server-side only; PII encrypted at rest + TLS in transit.
**Priority:** MVP. `Confirmed` (owner-restricted) [C2] · `Internal recommendation` (RLS/encryption).

### NFR-004: Messaging deliverability & compliance
**Description:** Reliable, compliant text/email.
**Acceptance criteria:** SMS via A2P-registered number with STOP opt-out + quiet hours; email authenticated (SPF/DKIM); sends retry on transient failure.
**Priority:** Soon. `Confirmed` (text priority) [C2] · `Internal recommendation` (compliance).

### NFR-005: Calendar-sync reliability
**Description:** Sync must not create conflicts or leak personal detail.
**Acceptance criteria:** External busy → "Unavailable" only; sync failures logged + retried; a sync outage never blocks in-app booking.
**Priority:** Soon. `Confirmed` [C3] · `Internal recommendation` (resilience).

### NFR-006: Data integrity & no lost leads
**Description:** The falling-through logic must never silently drop an inquiry.
**Acceptance criteria:** Every inquiry is either booked, actioned, or visible in falling-through; appointment create/edit/cancel is audit-logged (who/when).
**Priority:** MVP. `Confirmed` (owner wants to "know what's happening") [C1] · `Internal recommendation` (audit).

### NFR-007: Availability & backups
**Description:** Business-critical during work hours; recoverable.
**Acceptance criteria:** Target ≥99.9% (managed platform SLAs); automated daily DB backups with point-in-time recovery.
**Priority:** Soon. `Internal recommendation`.

### NFR-008: Scalability & cost
**Description:** Grow with the team without re-architecture; keep run-cost modest.
**Acceptance criteria:** Handles added reps/second salesperson; monthly run-cost stays modest (client is cost-sensitive).
**Priority:** MVP. `Confirmed` [C1][C2].

### NFR-009: Browser compatibility & accessibility
**Description:** Works on current mobile/desktop browsers; reasonable accessibility.
**Acceptance criteria:** Latest Chrome/Safari/Edge (desktop + iOS/Android); sufficient color contrast (note: green palette needs contrast check); keyboard-navigable forms.
**Priority:** Soon. `Internal recommendation`.

### NFR-010: Logging & error handling
**Description:** Observable failures without exposing private data.
**Acceptance criteria:** Integration/automation failures logged with context; user-facing errors are friendly; logs exclude full PII.
**Priority:** Soon. `Internal recommendation`.

---

## 10. Screens, Views, and Interface Requirements

> Detailed wireframes live in `01-product-plan.md`; this section adds the **empty/error states** and
> per-screen specifics the SOP requires.

### Screen: Login
**Purpose:** Authenticate internal users. **Primary users:** All internal.
**Key info:** Email, password. **Primary actions:** Sign in; Forgot password.
**Empty state:** N/A. **Error state:** "Email or password incorrect" without revealing which.
**Mobile:** Single-column, large fields. `Confirmed` [C3] + `Internal recommendation`.

### Screen: Team Calendar
**Purpose:** See/manage everyone's schedule; book. **Primary users:** All internal.
**Key info:** Color-coded appointments by type; Who/What filters; date range; time-off blocks.
**Primary actions:** Filter Who/What; Day/Week; date nav; + New appointment; tap slot to book; tap appt to edit.
**Filters/search:** Who (per-person), What (per-type). **Empty state:** "No appointments this week —
tap a slot or + New appointment to book." **Error state:** "Couldn't load the calendar — retry" (cached
view if possible). **Mobile:** Single-day column with horizontal day-swipe; side-panel → bottom sheet.
`Confirmed` [C3]; `assets/slide-layer1-one-calendar.png`.

### Screen: Appointment Side-Panel
**Purpose:** View/edit an appointment; contact the customer. **Primary users:** All internal.
**Key info:** Title, start/end, address, notes; customer phone/email/status.
**Primary actions:** Save changes; Cancel appointment; tap-to-call/text/email; close.
**Empty state:** N/A. **Error state:** "Couldn't save — retry"; **confirm before Cancel appointment**
(destructive). **Mobile:** Bottom sheet. `Confirmed` [C3].

### Screen: New Appointment modal
**Purpose:** Create a booking live. **Primary users:** All internal.
**Key info:** Client search/create; type; assignee; start/end; budget tier; property type; title; address; notes.
**Primary actions:** Search/create client; Book appointment; Cancel.
**Filters/search:** Client typeahead. **Empty state:** Client search shows "No match — create a new
client." **Error state:** Inline validation (required fields); double-booking rejection message.
**Mobile:** Full-screen sheet. `Confirmed` [C3].

### Screen: Pipeline Dashboard
**Purpose:** Conversion visibility + follow-up. **Primary users:** Owner, Staff.
**Key info:** KPI tiles; funnel bars; Top Sources; falling-through list w/ days-since-contact.
**Primary actions:** Email/text a lead; open a lead to book; (filter by period — see Open Questions).
**Filters/search:** Last-30-days default (other ranges TBD). **Empty state:** "No inquiries yet in this
period." / "Nothing falling through — you're current." **Error state:** "Couldn't load pipeline — retry."
**Mobile:** Tiles stack; bars full-width; list scrolls. `Confirmed` [C3]; `assets/demo-jun22-pipeline-full.png`.

### Screen: My Settings
**Purpose:** Profile, calendar sync, time-off. **Primary users:** All internal.
**Key info:** Name/phone/email/color; Google connection status; time-off blocks.
**Primary actions:** Edit profile; Connect Google; Add/remove time off.
**Empty state:** "No time off scheduled." **Error state:** "Google connection failed — reconnect."
**Mobile:** Single column. `Confirmed` [C3].

### Screen: Admin Setup (owner-only)
**Purpose:** Manage staff + configuration. **Primary users:** Owner.
**Key info:** Staff; appointment types (+colors); referral sources; budget tiers; property types; field config; reminder templates; integrations.
**Primary actions:** Add/edit/remove each list; edit templates; enter integration credentials.
**Empty state:** Seeded defaults present. **Error state:** Inline save errors; **confirm before removing**
a type/source in use. **Mobile:** Usable but desktop-optimized. `Confirmed` [C2][C3].

### (Future) Screens
Unified Inbox, AI Receptionist/Voice Triage config, Public Self-Booking page — `Future phase candidate`.

---

## 11. Data Model

> Full field-level tables and the ER (Mermaid) diagram are in `05-data-model.md`. Summary below.

| Entity | Purpose | Key Fields | Relationships | Notes |
|---|---|---|---|---|
| StaffMember | Internal user | id, name, email, phone, color, role, google_connected | → Appointments (assignee), → TimeOff | role: owner/staff/assistant |
| Client | External customer | id, name, phone, email, address, default_source | ← Appointments, ← Leads | PII |
| Appointment | The core event | id, client_id, assigned_staff_id, type_id, start, end, budget_tier, property_type, source, status, notes, quote_sent, quote_amount, won, clickup_link, created_by | → Client, → StaffMember, → Type/Tier/PropertyType/Source | double-booking rule |
| AppointmentType | Config, colored | id, name, color, self_bookable | ← Appointments | owner-editable |
| ReferralSource | Config | id, name, active | ← Appointments/Leads | remove "House", add "Facebook" |
| BudgetTier | Config | id, label, min, max | ← Appointments/Leads | <2k/2–5k/5–10k/10k+ |
| PropertyType | Config | id, name | ← Appointments | values TBD |
| Lead/Inquiry | Pre-consult prospect | id, client_id, source, city, budget_tier, last_contact_at, status | → Client, → Source | drives falling-through |
| TimeOff | Availability block | id, staff_id, start, end, reason | → StaffMember | shows "Unavailable" |
| Reminder | Notification record | id, appointment_id, channel, kind, send_at, status, template | → Appointment | sms/email |
| PipelineStage | Funnel state | key, order | ← Appointment | inquiry→consult→quote→won |
| Subcontractor | External installer | id, name, trade, contact | (optional) ← Appointment | no login (MVP) |
| ClickUpProject | PM link | appointment_id, task_id, url | → Appointment | one per booking |
| ActivityLog | Audit | id, actor, entity, action, at | → any | who changed what (NFR-006) |
| Conversation/Message | (Future) inbox | client_id, channel, direction, body, sent_at | → Client | future |

Field-level detail: see `05-data-model.md` (Appointment, Client, StaffMember, Lead, TimeOff, Reminder all specified with type/required/notes).

---

## 12. Statuses and Workflow States

### Appointment status
| Status | Meaning | Set By | Trigger | Automation | Next Possible |
|---|---|---|---|---|---|
| Scheduled | Booked, not yet confirmed | Staff | Book appointment | Send confirmation text+email | Confirmed, Rescheduled, Cancelled, Completed |
| Confirmed | Customer confirmed | Staff/System | Reply/confirm | — | Completed, Rescheduled, Cancelled |
| Rescheduled | Moved to a new time | Staff | Edit time | New confirmation | Scheduled/Confirmed |
| Completed | Consult happened | Staff | Mark complete | Prompt for quote outcome | (feeds pipeline) |
| Cancelled | Called off | Staff | Cancel appointment | Free slot; may re-enter falling-through | — |

### Pipeline stage (funnel)
| Stage | Meaning | Set By | Trigger | Automation | Next |
|---|---|---|---|---|---|
| Inquiry | Lead captured, no consult | System/Staff | Lead created | Falling-through watch | Consult booked / Lost |
| Consult booked | Appointment scheduled | Staff | Book consult | ClickUp project created | Quote sent / Lost |
| Quote sent | Quote emailed (+amount) | Staff | Mark quote sent | Feeds Avg Quote | Won / Lost |
| Won | Sale closed (+value) | Staff | Mark won | Feeds Won Value | — |
| Lost | Did not proceed | Staff | Mark lost | — | (reactivate) |

**Required:** Scheduled, Completed, Cancelled; Inquiry, Consult booked, Quote sent, Won.
**Optional:** Confirmed, Rescheduled, Lost. **Needs client confirmation:** exact status names/whether
"Confirmed" is used; how "Lost" is defined. **Avoid:** overlapping/ambiguous statuses that duplicate
ClickUp's project stages — keep this app's statuses about the *appointment/pipeline*, not the *job/
install* (that stays in ClickUp) to prevent confusion. `Strongly implied` [C1][C2].

---

## 13. Automation Requirements

### AUTO-001: Booking confirmation
**Trigger:** Appointment booked. **Conditions:** Client has phone/email; not a time-off block.
**Action:** Send text + email confirmation. **Recipient:** Customer. **Channel:** SMS + Email.
**Data used:** Client contact, appt time/address. **Failure handling:** Retry; log; flag on the appt.
**Logging:** Yes. **Priority:** Soon. `Confirmed` [C2][C3].

### AUTO-002: Appointment reminder
**Trigger:** Scheduled lead time before appt. **Conditions:** Appt active; within quiet-hours window.
**Action:** Send text + email reminder. **Recipient:** Customer. **Channel:** SMS + Email.
**Failure handling:** Retry; log. **Priority:** Soon. `Confirmed` [C2][C3].

### AUTO-003: ClickUp project creation
**Trigger:** Appointment booked. **Conditions:** ClickUp configured. **Action:** Create project/task;
store link. **Recipient:** Internal (ClickUp). **Channel:** CRM/PM update. **Failure handling:** Surface
+ allow retry; never block booking. **Priority:** Soon. `Confirmed` [C2].

### AUTO-004: Falling-through detection
**Trigger:** Nightly (or on data change). **Conditions:** Inquiry with no active consult + stale
last_contact_at. **Action:** Add/refresh in falling-through list with day count. **Recipient:** Owner/
Staff (in-app). **Channel:** Internal. **Failure handling:** Log. **Priority:** Soon. `Confirmed` [C3].

### AUTO-005: Weekly scorecard
**Trigger:** Weekly schedule (Mon). **Action:** Compile + email per-rep metrics. **Recipient:** Owner.
**Channel:** Email. **Failure handling:** Retry; log. **Priority:** Soon. `Confirmed` [C2].

### AUTO-006: Calendar sync
**Trigger:** Appt change / external change / interval. **Action:** Push app appts out; pull external
busy → "Unavailable." **Recipient:** Internal. **Channel:** Calendar update. **Failure handling:** Log +
retry; don't block booking. **Priority:** Soon. `Confirmed` [C2][C3].

### AUTO-007 (Future): AI receptionist / missed-call follow-up
**Trigger:** After-hours/unanswered call. **Action:** Answer, capture intake, offer self-book, drop
into pipeline; or auto text "we missed you." **Priority:** Future. `Future phase candidate` [C2][C3].

---

## 14. Integration Requirements

| Integration | Purpose | Data Sent | Data Received | Sync Direction | Priority | Open Questions |
|---|---|---|---|---|---|---|
| ClickUp | Auto-create project on booking | Client/appt details | Task ID/URL | One-way (app→ClickUp) | Soon | Workspace/list IDs; stage mapping (measure/quote/install) |
| Google Calendar | Availability + push appts | App appointments | External busy blocks | Two-way | Soon | Per-user OAuth; two-way vs one-way confirm |
| Apple/iCal | Owner personal viewing | — | (view only) | N/A (owner keeps separate) | Soon | Whether any iCal sync needed beyond Google |
| SMS provider (e.g., Twilio) | Text confirmations/reminders | Message + number | Delivery/opt-out | Two-way (status) | Soon | Sending number; A2P 10DLC registration |
| Email (e.g., Resend) | Email confirmations/reminders/scorecard | Message | Delivery status | One-way | Soon | Sender domain auth |
| Facebook/Instagram Lead Forms | Capture inquiries + budget question | — | Lead data | One-way (in) | Soon/Future | Is this the inquiry source for pipeline? (see §24) |
| Website form | Capture inquiries | — | Lead data | One-way (in) | Soon | Endpoint/webhook availability |
| Quoting tool | (Deferred) | — | — | — | Out of scope | Not integrated [C1][C2] |
| QuickBooks | (Deferred) commissions | — | — | — | Out of scope (MVP) | Not integrated [C1] |

**Cross-cutting:** Auth via OAuth (Google) / API tokens (ClickUp, SMS, email) stored server-side.
Risks: Google OAuth consent per user; SMS A2P approval lead time; ClickUp format consistency. Rate
limits: unknown — handle with retry/backoff. Duplicate prevention: dedupe leads by phone/email; one
ClickUp project per appointment. Sync logs required. Test environment: sandbox keys per provider.
`Confirmed` tools named [C1][C2][C3]; specific providers/credentials `Needs client confirmation`.

---

## 15. Reporting and Dashboard Requirements

| Report/Dashboard | Audience | Metrics | Filters | Update Frequency | Priority |
|---|---|---|---|---|---|
| Live Pipeline | Owner, Staff | Set rate, Avg quote, Won value, Falling-through count; funnel (Inquiries→Consults→Quotes→Won); Top sources | Period (30d default), (person — TBD) | Real-time | Soon |
| Falling-Through list | Owner, Staff | Inquiries w/ no consult; days-since-contact; source/city/budget | — | Real-time | Soon |
| Weekly Scorecard (email) | Owner | Inquiries, set rate, quotes sent, jobs won, $ sold; **per salesperson** | Prior week | Weekly | Soon |

**Live Pipeline** — *Decision it supports:* where leads stall + where to focus follow-up/ad spend.
*Action from it:* text/email/book a stalled lead. *Data that must be accurate:* appointment status +
inquiry source. `Confirmed` [C2][C3].
**Weekly Scorecard** — *Decision:* is the team (and a new hire) performing? *Data accuracy:* per-rep
attribution of consults/quotes/won. `Confirmed` [C2].

Not requested (future candidates): revenue forecasting, ad-source ROI, crew/installer utilization.

---

## 16. Notification Requirements

| Notification | Recipient | Trigger | Channel | Message Content | Priority |
|---|---|---|---|---|---|
| Booking confirmation | Customer | Appointment booked | SMS + Email | Appt date/time, address, rep, contact | Soon |
| Appointment reminder | Customer | Lead time before appt | SMS + Email | Reminder + reschedule/contact info | Soon |
| Reschedule notice | Customer | Appt time changed | SMS + Email | New time | Soon |
| New assignment | Assigned rep | Appt assigned to them | In-app (+ optional text) | Client, time, type, address | Soon |
| Falling-through follow-up | Owner/Staff | Lead goes stale | In-app list | Who + days since contact | Soon |
| Weekly scorecard | Owner | Weekly | Email | Per-rep metrics | Soon |
| Automation failure | Owner/Admin | ClickUp/SMS/sync fails | In-app + log | What failed + retry | Soon |
| (Future) Missed-call alert | Owner/Staff | After-hours/missed call | In-app/SMS | Caller + intake | Future |

Notifications for job assignment/reschedule and failure alerts are `Internal recommendation`;
customer confirmations/reminders and scorecard are `Confirmed` [C2][C3].

---

## 17. UX and Design Requirements

- **Simplicity above all** — "keep it simple"; minimal clicks to book on a live call; no role gymnastics. `Confirmed` [C3]
- **Calendar-first + mobile-first** — most use is on phones in the field; the calendar is the home screen. `Confirmed` [C1][C3]
- **Low cognitive load / clarity** — color-coded types; open white space = bookable; clear next action. `Confirmed` [C3]
- **Minimal duplicate entry** — client search before create; sits in front of ClickUp (no re-keying jobs). `Confirmed` [C1]
- **Clear status indicators** — appointment + pipeline statuses visible at a glance. `Strongly implied` [C3]
- **Error prevention** — double-booking blocked; required-field validation; **confirmation before
  destructive actions** (cancel appt, remove a config item in use). `Confirmed` (double-book) [C3] + `Internal recommendation`.
- **Progressive disclosure** — side-panel/modal reveal detail on demand; Setup hidden from non-owners.
- **Search & filtering** — Who/What on calendar; client typeahead; falling-through actionable rows.
- **Brand** — olive/forest-green on off-white, "TAKOY DESIGNS · OPS" wordmark (match demos). `Confirmed` (demos) [C2][C3]; note green-on-green contrast for accessibility (`Internal recommendation`).

---

## 18. Technical Architecture Recommendation

`Internal recommendation` (stack not client-mandated; chosen to fit mobile-web + calendar-sync + SMS needs).

```
       Mobile / Desktop Browser (React + Tailwind + shadcn/ui)
                          |
                   Frontend App (Vite/TS)
                          |
        Supabase API  (Auth + Row-Level Security)
                          |
               Postgres (managed, backups/PITR)
                          |
   Edge Functions / scheduled jobs (reminders, falling-through, scorecard, sync)
                          |
   Integrations: Google Calendar · ClickUp · SMS (Twilio) · Email (Resend) · Lead forms
```

- **Frontend:** React + Vite + TypeScript + Tailwind + shadcn/ui (Lovable default).
- **Backend/API:** Supabase (PostgREST + Auth + RLS).
- **Database:** Postgres (managed).
- **Auth:** Supabase email/password; roles owner/staff/assistant.
- **Hosting:** Edge (Lovable/Vercel) frontend + Supabase managed backend.
- **File storage:** Supabase Storage (assets; future attachments).
- **Background jobs:** Supabase scheduled Edge Functions (reminders, nightly falling-through, weekly scorecard, sync).
- **Integrations:** Google Calendar, ClickUp, Twilio, Resend, FB/IG + website lead forms.
- **Logging/monitoring:** Supabase logs + provider webhooks; integration-failure surfacing in-app.
- **Error handling:** Retry/backoff on integrations; async side-effects never block booking.
- **Testing framework:** Vitest/RTL (frontend), Playwright (E2E), pgTAP/SQL tests for RLS.
- **Deployment:** Preview (Lovable sandbox, seeded mock data) → prod; reversible migrations.

---

## 19. Security and Permission Requirements

- **Roles:** owner / staff / assistant (internal); external subcontractor/customer are records, not
  logins in MVP. `Confirmed` [C2][C3].
- **Authentication:** email/password; session expiry; password reset. `Confirmed` (login) [C3] + `Internal recommendation`.
- **Authorization:** RLS — internal users read all appointments/clients; **only owner writes config**
  (types/sources/tiers/property types/staff/fields). `Confirmed` [C2].
- **Data access restrictions:** personal calendar detail never exposed (only "Unavailable"). `Confirmed` [C3].
- **Admin-only actions:** config edits, staff management, integration credentials, field config. `Confirmed` [C2].
- **Audit log:** who created/edited/cancelled an appointment + config changes (owner wants to "know
  what's happening"). `Confirmed` intent [C1] + `Internal recommendation`.
- **Sensitive data:** customer name/phone/email/address = PII; encrypt at rest + TLS; exclude full PII from logs.
- **API credential storage:** server-side secrets only; never shipped to client.

### Permissions table
| Feature/Action | Owner/Admin | Staff (Nissa/Carolyn/Tracy) | Assistant | Customer/External |
|---|---|---|---|---|
| View team calendar | Yes | Yes | Yes | No |
| Create appointment | Yes | Yes | Yes | No (future self-book) |
| Edit/cancel any appointment | Yes | Yes | Limited (TBD) | No |
| View pipeline & metrics | Yes | Yes | Yes | No |
| Text/email a lead | Yes | Yes | Yes | No |
| Manage own time-off | Yes | Yes | Yes | No |
| Edit config (types/sources/tiers/fields) | Yes | No | No | No |
| Manage staff / integrations | Yes | No | No | No |
| Receive weekly scorecard | Yes | Optional | No | No |

`*` Assistant's edit/cancel scope for *others'* appointments is an Open Question (§24).

---

## 20. Testing Plan

**Test types:** unit (metrics calc, double-booking rule), integration (ClickUp/Google/SMS/email),
E2E (booking flow), role-based (RLS/permissions), mobile (375px), browser, automation (reminders/
scorecard), error-handling (integration failures), data-persistence (refresh), API-failure.

### Test Case: Book live on the phone (happy path)
**Role:** Staff/Admin. **Preconditions:** Signed in; a client exists or will be created.
**Steps:** 1) Open Calendar. 2) + New appointment. 3) Search/create client. 4) Set type, assignee,
time, budget tier, property type, address. 5) Book.
**Expected:** Appointment appears immediately in the assignee's column; confirmation text+email queued;
ClickUp project link stored; pipeline Inquiry→Consult increments; persists on refresh.
**Failure cases:** Missing required field → Book disabled; SMS provider down → appt still books, notice logged.

### Test Case: Double-booking prevention
**Role:** Staff. **Preconditions:** Rep A has 1–2pm booked.
**Steps:** Attempt to book Rep A 1:30–2:30pm.
**Expected:** Rejected with a clear message. **Failure cases:** Booking Rep B 1:30–2:30 succeeds; booking Rep A 2–3pm succeeds; time-off overlap also rejected.

### Test Case: Owner-only config (permission)
**Role:** Staff, then Owner. **Preconditions:** Both accounts exist.
**Steps:** As Staff, try to open Setup / edit a referral source (via UI and direct API).
**Expected:** UI hidden; API write rejected by RLS. As Owner, edit succeeds (remove "House", add "Facebook").
**Failure cases:** Assistant cannot reach Setup; token tampering still rejected server-side.

### Test Case: Time-off blocks booking
**Role:** Staff. **Preconditions:** Rep C added vacation Mon–Fri.
**Steps:** Try to book Rep C on Wednesday.
**Expected:** Slot shows "Unavailable — Vacation"; booking blocked; personal event detail not shown.

### Test Case: Falling-through follow-up
**Role:** Owner/Staff. **Preconditions:** An inquiry with no consult, last contact 8 days ago.
**Steps:** Open Pipeline → Falling-through.
**Expected:** Lead listed with "8 days no contact"; text/email actions work; booking removes it from the list.

### Test Case: Reminder automation
**Role:** System. **Preconditions:** Appointment tomorrow; reminder lead time set.
**Steps:** Run the scheduled reminder job.
**Expected:** Text + email sent at the right time; respects quiet hours; STOP opt-out honored; logged.
**Failure cases:** Provider error → retry + log, no crash.

### Test Case: Mobile booking (E2E)
**Role:** Staff. **Preconditions:** 375px viewport.
**Steps:** Complete the full booking flow on mobile.
**Expected:** No horizontal scroll; side-panel/modal as sheets; tap targets ≥44px; booking succeeds.

---

## 21. MVP Scope

### 21.1 MVP Must Include
- Unified team calendar with Who/What filters, day/week, date nav (FR-001). `Confirmed` [C3]
- Create/edit appointment + client create/search (FR-002, FR-004, FR-018). `Confirmed` [C3]
- Double-booking prevention (FR-003). `Confirmed` [C3]
- Tap-slot-to-book (FR-005), appointment status (FR-017). `Confirmed` [C3]
- Per-person time-off blocking (FR-006). `Confirmed` [C3]
- Auth + roles + owner-only Setup for staff/types/sources/tiers (FR-013, FR-014). `Confirmed` [C2][C3]
- Mobile responsiveness (FR-019 / NFR-002). `Confirmed` [C3]

### 21.2 MVP Should Exclude (do soon after, not in the first cut)
- Pipeline dashboard + falling-through (FR-007/008) — *build immediately after the calendar works.*
- Text/email confirmations + reminders (FR-009).
- ClickUp auto-project (FR-010), Google sync (FR-011), weekly scorecard (FR-012).
- Everything Future: self-booking, unified inbox, AI receptionist, voice triage, quoting, commissions.

### 21.3 MVP Success Criteria
- The office can book any caller **live on the first call** — zero "call-you-back to schedule." `Confirmed` [C1]
- Every staff member sees the whole team's schedule on their phone. `Confirmed` [C3]
- Double-booking is impossible; time-off is respected.
- Tanya can view everyone's calendar in one place.

### 21.4 MVP Risks
- **Lead-source gap:** without an inquiry feed, falling-through is limited to calendar data (mitigate in §26).
- **Adoption:** team must switch from Google-only habits (mitigate: sync + simplicity).
- **SMS lead time:** A2P registration can delay texting (start early; email-first fallback).

---

## 22. Phased Roadmap

### Phase 1: Foundation / MVP — the calendar that stops the bleeding
**Goal:** Live team calendar + live booking. **Includes:** FR-001–006, 013 (core), 014, 017–019.
**Excludes:** pipeline, automations, integrations. **Exit criteria:** book live on mobile with
double-booking + time-off enforced; whole team visible; owner can configure types/sources/tiers.
Target: **calendar live by end of month** [C2].

### Phase 2: Visibility & Communication
**Goal:** Conversion tracking + client comms. **Includes:** FR-007/008 (pipeline + falling-through),
FR-009 (text+email), FR-016/017 (quote/won status), FR-012 (scorecard). **Exit criteria:** funnel +
falling-through accurate; confirmations/reminders sending; weekly scorecard delivered. Target:
**conversion tracking by first half of July** [C2].

### Phase 3: Integrations & Automation
**Goal:** Connect the ecosystem. **Includes:** FR-010 (ClickUp auto-project), FR-011 (Google sync),
FR-015 (lead-form budget question / inquiry intake). **Exit criteria:** booking creates a ClickUp
project; external busy blocks show as Unavailable; inquiries flow into the pipeline.

### Phase 4: Advanced / Optional Add-ons
**Goal:** Reduce missed contact + consolidate comms. **Includes:** FR-020 self-booking, FR-021 unified
inbox, FR-022 AI receptionist, FR-023 voice triage. **Exit criteria:** per client sign-off (each is a
paid add-on pending Tanya's review of the options email) [C2][C3].

---

## 23. Developer Implementation Checklist

**Product Clarity:** ☑ Goal clear · ☑ Roles defined · ☑ Requirements written · ☑ Acceptance criteria (MVP/Soon) · ☑ Out-of-scope clear.
**UX:** ☑ Screens defined · ☑ Flows mapped (J1–J9) · ☑ Empty states · ☑ Error states · ☑ Mobile behavior.
**Backend:** ☑ Entities defined · ◻ API endpoints (derive from entities) · ☑ Auth defined · ☑ Permissions/RLS defined · ☑ Audit log defined.
**Integrations:** ☑ Integrations listed · ◻ Credentials collected (see §24) · ☑ Sync direction · ☑ Failure handling · ☑ Duplicate prevention.
**Testing:** ☑ Test cases (core) · ☑ Role-based tests · ☑ Integration tests · ☑ Mobile tests · ☑ Failed-automation tests.
**Release:** ☑ MVP scope confirmed · ◻ Release criteria signed off · ◻ Rollback plan (reversible migrations) · ☑ Docs updated · ◻ Client review items prepared (July 19 review) [C2].

(◻ = requires a client input or a build-time decision.)

---

## 24. Open Questions for Client

| Priority | Category | Question | Why It Matters |
|---|---|---|---|
| Critical | Lead intake | How do un-booked inquiries enter the system — manual, FB/IG + website lead-form webhook, or wait for the unified inbox? | Determines whether falling-through covers cold leads or only calendar data |
| Critical | Messaging | Confirm SMS sending number + complete A2P 10DLC registration | Texts (the priority channel) can't go live without it |
| Critical | Integrations | ClickUp workspace/list IDs + which ClickUp stages map to the pipeline | Needed for auto-project + status alignment |
| Critical | Calendar | Google sync one-way or two-way? Who grants OAuth per user? Any iCal sync beyond Google? | Affects conflict prevention + build effort |
| Important | Comms | Reminder wording/branding + cadence (e.g., 24h + 1h?) | Pending action item from Tanya [C2] |
| Important | Config | Final appointment types (+colors) and property-type values | Needed to seed dropdowns |
| Important | Config | Confirm referral sources (remove House, add Facebook — anything else, e.g., BNI/builder?) | Pipeline attribution |
| Important | Permissions | Can the remote assistant edit/cancel *others'* appointments, or only create? | Changes RLS rules |
| Important | Pipeline | Is quote-sent/won a manual flag+amount (no quoting engine)? Confirm | Determines how Avg Quote/Won Value are fed |
| Optional | Business hours | Confirm working hours + quiet-hours window (Mountain Time) | Reminder timing + future self-book windows |
| Optional | Scope | Commission tracking in or out for launch? | Confirms out-of-scope [C1] |
| Optional | Ops | App domain/URL; who provisions logins; offboarding | Deployment + access hygiene |

(Deliberately omits already-answered items — unified calendar, everyone-sees-everything, text+email, mobile-web, keep ClickUp, deferred quoting.)

---

## 25. Assumptions to Confirm

| Assumption | Why It Was Made | Risk If Wrong | How to Confirm |
|---|---|---|---|
| Pipeline "Quotes sent/Avg quote" is fed by a manual flag+amount | Quoting engine explicitly deferred [C1][C2] | Metrics undercount if no data source | Confirm the rep will mark quote-sent + amount |
| Inquiries are captured somewhere feeding falling-through | Demo showed a falling-through list [C3] | Cold leads never surface | Decide intake source (§24) |
| Google is the sync target; Apple stays personal-only | Tanya "look at my Apple calendar… but the team calendar for the team" [C3] | Rework if iCal sync required | Confirm per-user calendar setup |
| Twilio + Resend as SMS/email providers | Fit the stack; not client-named | Swap effort if different | Confirm providers/accounts |
| Property types ≈ Residential/New build/Commercial | Residential-primary + builder work [C1][C3] | Wrong dropdown values | Get Tanya's list |
| Team needing logins = Tanya, Nissa, Carolyn, Tracy, assistant | Roster from [C2] | Missing/extra accounts | Confirm from onboarding info already sent |
| ~30-day timeline with calendar first, tracking by mid-July | Stated commitments [C2] | Schedule mismatch | Confirm at July 19 review |

---

## 26. Risks and Mitigation Plan

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Lead-intake gap (cold leads not captured) | High | High | Decide intake source early; ship manual entry first, add lead-form webhook Phase 3 |
| SMS A2P registration delay | Medium | Medium | Start registration now; email-first reminders as interim |
| ClickUp data-format inconsistency | Medium | Medium | One-way app→ClickUp only; validate payload; surface failures |
| User adoption vs. Google-only habits | Medium | High | Two-way sync + radical simplicity; train at July 19 review |
| Scope creep into quoting/AI add-ons | Medium | High | Keep them Phase 4 + paid; hold MVP line |
| Permission mistakes (over-broad access) | Low | High | Enforce RLS server-side; role tests in test plan |
| Reporting accuracy (bad status data) | Medium | Medium | Simple statuses; validation; audit log |
| Bad/thin source data on quoting/commissions | Medium | Low | Explicitly out of scope; documented |
| Timeline risk (owner very busy) | Medium | Medium | Async decisions; bypass formal onboarding as agreed [C2] |
| Technical debt from rushing integrations | Low | Medium | Reversible migrations; integrations behind Setup flags |

---

## 27. Out-of-Scope Items

| Item | Reason It Is Out of Scope | Revisit When |
|---|---|---|
| Custom quoting engine | Supplier pricing too fluid/inconsistent to automate reliably [C1][C2] | If a reliable, structured supplier price feed exists |
| Commission tracking | Handled in QuickBooks + spreadsheet; not the core pain [C1] | After core adoption; if Tanya wants it centralized |
| AI receptionist | Optional paid add-on; pending Tanya's review [C2][C3] | Phase 4 / after options email reviewed |
| Voice triage | Optional paid add-on [C3] | Phase 4 |
| Unified social/email/text inbox | Optional add-on; not core booking pain [C2][C3] | Phase 4 (also unblocks richer lead intake) |
| Public self-booking | Nice-to-have; Tanya prefers phone qualification [C1][C2] | Phase 4; per-type opt-in (networking/marketing first) |
| Installer/subcontractor logins & app views | No stated need in MVP [C2] | If install coordination moves into the app |
| Native mobile app | Explicitly not wanted; mobile web suffices [C3] | Not planned |

---

## 28. Recommended Next Steps

1. **Confirm with the client (the Critical questions in §24):** lead-intake source, SMS number/A2P,
   ClickUp IDs + stage mapping, Google sync direction. Also confirm reminder wording + final config lists.
2. **Design first:** the Team Calendar + New Appointment flow (the MVP core) at mobile width, matching
   the demo screenshots.
3. **Build first (Phase 1):** auth + roles + data model/RLS → calendar read view → side-panel edit →
   New Appointment + double-booking → time-off → owner Setup (types/sources/tiers).
4. **Technical setup:** Supabase project (dev + prod), seeded mock data, secrets vault; provider
   accounts (Twilio/Resend/Google/ClickUp) with sandbox keys.
5. **Data/credentials needed:** staff list (names/emails/phones), Google OAuth consent per user,
   ClickUp workspace/list + token, SMS number + A2P brand, email sender domain.
6. **Test first:** the booking happy path, double-booking prevention, and owner-only permission
   (the three that protect the core value and data integrity).
7. **Review before development sign-off:** walk this package + Phase 1 scope with Tanya at the **July 19
   review** [C2]; lock MVP scope and the intake decision, then start Phase 2.

---

## Appendix — Conflicts or Ambiguities Found (SOP §1.5)

| Conflict | Source A | Source B | Most likely | To confirm |
|---|---|---|---|---|
| Avg project value | "~$6,000" spoken [C2] | Demo "Avg quote $6,850" [C3 mockup] | $6,000 is the client's real figure; $6,850 is mock demo data | Confirm the working average for scorecard math |
| Leads lost | "4–5 per month" [C1] | "~1 per week" [C2] | Same order of magnitude (~4–5/mo ≈ 1/wk) | Treat as ~1/week; validate once tracking is live |
| Social-lead close rate | "30% to 50%" [C2] | — | Use a conservative 30% for projections | Confirm after real data |
| Team size framing | "four primary — Tanya, Nissa, Carolyn, Tracy" [C2] | "one other salesperson" [C1, earlier] | June 11 roster is current (business grew/clarified) | Confirm active roster + who needs logins |
| Referral source "House" | Listed in demo [C3] | Tanya: "never a referral source for us" [C3] | Remove it | Done — remove House, add Facebook |

`Confirmed by transcript` for each source; resolutions are `Internal recommendation` pending client confirmation.
