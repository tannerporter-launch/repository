# 01 · Product Plan — how it works when it's done

This is the "finished product" walkthrough: what users do, screen by screen. Wireframes are
ASCII sketches; each references the matching **real demo screenshot** in `assets/` so the
builder can match the intended look.

- Calendar + side panel → `assets/demo-jun22-calendar-sidepanel.png`, `assets/slide-layer1-one-calendar.png`
- New Appointment modal → `assets/demo-jun22-new-appointment-modal.png`
- Pipeline dashboard → `assets/demo-jun22-pipeline-full.png`, `assets/demo-jun22-pipeline-dashboard.png`
- Metrics funnel → `assets/slide-layer4-daily-metrics.png`
- "Never miss another one" (future) → `assets/slide-layer3-never-miss.png`

---

## Screen inventory

| # | Screen | Primary users | Status |
|---|--------|---------------|--------|
| S1 | Login / Auth | All internal | Core |
| S2 | Team Calendar (day/week) | All internal | Core |
| S3 | Appointment Side-Panel (view/edit) | All internal | Core |
| S4 | New Appointment modal | All internal | Core |
| S5 | Pipeline Dashboard | Owner, Staff | Core |
| S6 | Metrics / Weekly Scorecard | Owner (email) | Core |
| S7 | My Settings (profile, calendar sync, time-off) | All internal | Core |
| S8 | Admin Setup (staff, types, sources, tiers, field config) | Owner only | Core |
| S9 | Unified Inbox | Owner, Staff | Future |
| S10 | AI Receptionist / Voice Triage config | Owner | Future |
| S11 | Public Self-Booking page | External leads | Future |

Global chrome (top nav, seen in every demo screenshot): **CALENDAR · PIPELINE · DISCUSS ·
SETUP** tabs, a "DEMO ON" toggle (dev only), and **Sign out**. Brand: "TAKOY DESIGNS · OPS",
olive/green palette.

---

## Primary user journeys

### J1 — Inbound lead → booked consult (the money path) [C1][C3]
1. A lead calls (or DMs). **Nissa** (or any rep) opens the app on her phone/desktop → **S2 Calendar**.
2. She taps **+ New Appointment** (or taps an open slot to pre-fill the time) → **S4 modal**.
3. Searches the client by name/phone/email; if new, **"+ Or create a new client"**.
4. Fills **Type** (e.g., Initial Consult), **Assigned to** (any staff), **Start/End**,
   **Budget tier**, **Property type**, **Address**, **Notes**.
5. Taps **Book appointment** → event is written to the shared calendar, **double-booking the
   same staff member is blocked**, an auto **text + email confirmation** goes to the client,
   and a **ClickUp project is auto-created** for the job [C2].
6. The lead now shows as a booked consult in **S5 Pipeline** (no longer "falling through").

### J2 — A rep's day [C3]
1. Carolyn opens the mobile web calendar, sets **Who = Carolyn**, **What = All types**.
2. Sees her color-coded appointments for the day/week. Taps one → **S3 side-panel** with the
   customer's phone, email, address, status, and notes; taps to call/text or get directions.

### J3 — Owner oversight [C2][C3]
1. Tanya sets **Who = Everyone** to see the whole team on one calendar.
2. Switches to **S5 Pipeline**: Set Rate, Avg Quote, Won Value, Falling-Through count, funnel
   bars (Inquiries → Consults booked → Quotes sent → Won), and Top Sources.
3. Every Monday she gets an **automated weekly scorecard email** (S6) summarizing last week —
   "this is also how you'll know a new salesperson's numbers without hovering" [C2].

### J4 — Nothing falls through the cracks [C3]
1. On **S5 Pipeline**, the **"Falling through the cracks"** list shows inquiries with no booked
   consult and their **days-since-contact** (e.g., "8 days no contact").
2. Tanya/Nissa clicks a person → sends an **email or text** right from the row, or books them.

### J5 — Time off / vacation [C3]
1. Nissa goes to **S7 My Settings → Time off**, adds a range ("Jun 30–Jul 4, Vacation").
2. On the team calendar those slots show as **"Unavailable — Vacation"** to everyone, so no one
   books her — **without** exposing her personal calendar events.

### J6 — (Future) After-hours miss → AI receptionist [C2][C3]
A call comes in when all reps are in homes/after hours → AI receptionist answers, gathers the
same intake fields, offers a self-booking link, and drops the lead into the pipeline so it never
"falls through." (See `assets/slide-layer3-never-miss.png`.)

---

## Page-by-page layouts

### S1 · Login / Auth
```
┌─────────────────────────────────────┐
│            TAKOY DESIGNS · OPS       │
│                                      │
│   Email    [__________________]      │
│   Password [__________________]      │
│            [   Sign in   ]           │
│            Forgot password?          │
└─────────────────────────────────────┘
```
- Email + password (accounts provisioned by owner — see doc 06 / open question in doc 07).
- On success → lands on **S2 Team Calendar** (default view). Mobile + desktop responsive.

### S2 · Team Calendar  → `assets/demo-jun22-calendar-sidepanel.png`, `assets/slide-layer1-one-calendar.png`
```
 TAKOY DESIGNS · OPS         [CALENDAR] PIPELINE DISCUSS SETUP        Sign out
 ────────────────────────────────────────────────────────────────────────────
 TAKOY DESIGNS · TEAM CALENDAR · WEEK OF JUN 22
 VIEW BY [Today] ‹  Jun 22–2026 (day 26)  › [Week ▾] Who[Everyone ▾] What[All types ▾]   23 appts  [+ New appointment]
 ────────────────────────────────────────────────────────────────────────────
        MON 22        TUE 23        WED 24        THU 25        FRI 26
  8a  ┌Consult·Sasha┐              ┌Event·Owen ┐              ┌Event·Marin ┐
  9a  │Consult·Hail.│ Event·Brody                             Event·Knox
 10a  │Event·Marcus │              ...color-coded blocks by appointment type...
 11a  │Event·Nora   │
  1p  │Event·Erin   │
 ────────────────────────────────────────────────────────────────────────────
 Open white space = bookable. Tap a slot to book; tap an appointment to edit.
```
- **VIEW BY**: `Today` reset · `‹ ›` date nav · `Day / Week` toggle.
- **Who** dropdown: `Everyone` (default checked) + one checkbox per team member
  (Tanya, Carolyn, Tracy, Nissa …) each with a color dot, + **"+ Add team member"** (owner).
- **What** dropdown: `All types` + one entry per appointment type (filters the grid).
- **Appointments**: color-coded by **type**; label shows `Type · Customer` and a sub-line
  `City · detail`. Tap → **S3 side-panel**. Tap empty slot → **S4 modal** pre-filled with that time.
- **+ New appointment** (top-right) opens **S4**.
- Time-off blocks render as muted **"Unavailable — <reason>"** bars (J5).

### S3 · Appointment Side-Panel  → `assets/demo-jun22-calendar-sidepanel.png`
```
                                        ┌──────────────────────────────┐
                                        │ INSTALL WALKTHROUGH · VASQUEZ │
                                        │ Erin Vasquez · Draper       ✕ │
                                        │ TITLE   [Install Walkthrough…]│
                                        │ START [06/22 01:00P] END [02:30P]
                                        │ ADDRESS [Draper, UT]          │
                                        │ NOTES  [___________________]  │
                                        │ ─────────────────────────────│
                                        │ PHONE   (801) 555-0119        │
                                        │ EMAIL   erin.v@example.com    │
                                        │ STATUS  rescheduled           │
                                        │ [Cancel appointment] [Save changes]
                                        └──────────────────────────────┘
```
- Slides in from the right over the calendar. Editable: Title, Start, End, Address, Notes.
- Read-back block shows the **customer's** Phone / Email / Status (explicitly the *customer's*
  info, not the assigned rep's — confirmed [C3]). Phone/email are tap-to-call / tap-to-text.
- **Status** values: e.g., `scheduled`, `confirmed`, `completed`, `rescheduled`, `cancelled`.
- Buttons: **Save changes**, **Cancel appointment** (removes/voids the event).

### S4 · New Appointment modal  → `assets/demo-jun22-new-appointment-modal.png`
```
        ┌─────────────────────────────────────────────┐
        │ NEW APPOINTMENT                           ✕ │
        │ Books in the CRM and blocks double-booking  │
        │ the same staff member.                      │
        │ CLIENT [ Search name, phone, or email…    ] │
        │        ▸ Or create a new client             │
        │ TYPE [Pick a type ▾]   ASSIGNED TO [Staff ▾]│
        │ START [mm/dd/yyyy --:--] END [mm/dd/yyyy --]│
        │ TITLE [e.g. Consult · Hendricks]            │
        │ ADDRESS [______________________]            │
        │ (Budget tier ▾)  (Property type ▾)          │
        │ NOTES [______________________________]      │
        │                    [Cancel] [Book appointment]
        └─────────────────────────────────────────────┘
```
- **Client**: typeahead search over existing clients; **"+ Or create a new client"** reveals
  name/phone/email fields inline.
- **Type** (appointment type, drives color), **Assigned to** (any staff — no restriction [C3]).
- **Budget tier**: `Under $2k / $2–5k / $5–10k / $10k+` [C3].
- **Property type**: e.g., Residential / New build / Commercial (list TBD — see doc 07).
- **Start/End**, **Title**, **Address**, **Notes**.
- **Book appointment**: validates → **blocks double-booking the assigned staff** → writes event,
  fires confirmation text+email, creates ClickUp project. Disabled until required fields set.

### S5 · Pipeline Dashboard  → `assets/demo-jun22-pipeline-full.png`
```
 TAKOY DESIGNS · LIVE PIPELINE (LAST 30 DAYS)
 ┌ SET RATE ┐ ┌ AVG QUOTE ┐ ┌ WON VALUE ┐ ┌ FALLING THROUGH ┐
 │  74%     │ │  $6,850   │ │  $61,400  │ │  6              │
 │ 17 of 23 │ │ 14 quoted │ │ 9 closed  │ │ No consult yet  │
 └──────────┘ └───────────┘ └───────────┘ └─────────────────┘
 INQUIRIES        ████████████████████████████ 23
 CONSULTS BOOKED  ████████████████████ 17
 QUOTES SENT      ██████████████ 14
 WON              ██████ 9
 TOP SOURCES  (Website)(Referral)(Instagram)(Houzz)(Google)(Repeat client)
 ──────────────────────────────────────────────────────────────
 FALLING THROUGH THE CRACKS · inquiries with no consult booked yet
 Marin Donnelly   Instagram · Kaysville · $2k–5k        8 DAYS NO CONTACT
 Dustin Greer     Website · Murray · under $2k          11 DAYS NO CONTACT
 Owen Reyes       Referral · Provo · $5k–10k            6 DAYS NO CONTACT
```
- **KPI tiles**: Set Rate, Avg Quote, Won Value, Falling-Through count.
- **Funnel bars**: Inquiries → Consults Booked → Quotes Sent → Won (mirrors `slide-layer4`).
- **Top Sources** chips: Website, Referral, Instagram, Facebook, Google, Houzz, Repeat client
  — **"House" removed, "Facebook" added** per [C3]. (Editable in S8.)
- **Falling-through list**: name, source · city · budget tier, and **days-since-contact**;
  each row → click to **email/text** or book. Rows are calendar/inquiry-driven.

### S6 · Metrics / Weekly Scorecard [C2]  → `assets/slide-layer4-daily-metrics.png`
- Same funnel as S5, framed as "Daily metrics, zero gut feel."
- **Automated weekly email** to Tanya summarizing the previous week (inquiries, set rate,
  quotes, jobs won, $ sold). Per-salesperson breakdown so new hires' numbers are visible.

### S7 · My Settings [C3]
```
 MY SETTINGS
 Profile        Name / Phone / Email / color
 Calendar sync  [Connect Google Calendar]  status: ●synced
 Time off       [+ Add time off]  → { Start date, End date, Reason(Vacation/Personal) }
                • Jun 30 – Jul 4 · Vacation   [remove]
```
- **Calendar sync**: connect personal Google (two-way — appointments flow out; personal busy
  blocks flow in as "unavailable"). Owner can keep using Apple/iCal for personal viewing [C3].
- **Time off**: add/remove blocks; renders as "Unavailable" on the team calendar (J5).

### S8 · Admin Setup — owner only [C2][C3]
```
 SETUP (owner only)
 Team members     add/edit/remove staff, set color, set app role
 Appointment types add/edit/remove types + color (Initial Consult, Install Walkthrough, …)
 Referral sources  add/edit/remove (Website, Referral, Instagram, Facebook, Google, Houzz, Repeat client)
 Budget tiers      edit the 4 tiers (<2k / 2–5k / 5–10k / 10k+)
 Property types    edit list
 Field config      which custom fields appear on appointments (locked to owner)
```
- Encodes [C2]: *"administrative access to edit fields is restricted to the business owner to
  maintain data integrity."* Staff use these lists; only the owner edits them.

### S9–S11 · Future
- **S9 Unified Inbox** [C2][C3]: Facebook/Instagram DMs + email + text in one thread per client;
  "Add to ClickUp" from a message; this is the source that feeds un-booked inquiries into the pipeline.
- **S10 AI Receptionist / Voice Triage** [C3]: after-hours answer, intake capture, self-book offer.
- **S11 Self-Booking page** [C1][C2]: public link showing real openings for chosen appointment
  types (esp. networking/marketing); "self-booking is an option you switch on per appointment
  type, not a default" (`slide-layer3-never-miss.png`).

---

## Design notes
- **Palette/brand:** olive/forest green on off-white, "TAKOY DESIGNS · OPS" wordmark (match demos).
- **Mobile-first:** most usage is on phones in the field [C1][C3] — calendar and side-panel must
  be fully usable one-handed; side-panel becomes a bottom sheet on small screens.
- **Simplicity is a hard requirement** [C3]: "keep it simple," no role gymnastics, minimal clicks
  to book while a customer is on the phone.
