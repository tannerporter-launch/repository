# 02 · Process Plan — how we build it

## Recommended stack (Lovable)

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | **React + Vite + TypeScript + Tailwind + shadcn/ui** | Lovable's default; fast to build the calendar/dashboard UI shown in the demos |
| Backend | **Supabase** — Postgres + Auth + Row-Level Security + Storage + Edge Functions | One managed backend covers DB, login, per-role security, and serverless jobs |
| SMS | **Twilio** (or Supabase-compatible SMS provider) via Edge Function | Text reminders/confirmations — the higher-open-rate channel Tanya wants [C2] |
| Email | **Resend** via Edge Function | Confirmations + weekly scorecard |
| Calendar sync | **Google Calendar API** (OAuth per user) | Two-way sync; personal busy → "unavailable" [C2][C3] |
| PM integration | **ClickUp API** | Auto-create a project when an appointment is booked [C2] |
| Scheduling jobs | **Supabase scheduled Edge Functions (cron)** | Reminder sends, falling-through recompute, weekly scorecard |
| Hosting | **Lovable/Vercel edge (frontend) + Supabase managed Postgres** | Serverless, auto-scaling, low ops (see doc 04) |

> Why not custom quoting: supplier pricing changes 2–3×/year in inconsistent formats and can't be
> automated reliably — **explicitly out of scope** [C1][C2]. The pipeline's "Quote sent / Avg quote"
> is fed by a **manual "quote sent + amount" field** on the appointment/job, not a quoting engine.

## Environments
- **dev** (Lovable sandbox / preview) with seeded mock data (the demo already uses "Demo mode — mock data").
- **prod** Supabase project + production frontend deploy. Separate API keys/secrets per env.
- Secrets (Twilio, Resend, Google OAuth, ClickUp) live in Supabase env/secrets, never in the client.

## Seed / mock data
Reuse the demo's realistic mock set: ~23 inquiries, 17 consults, 14 quotes, 9 won; staff Tanya/
Carolyn/Tracy/Nissa; sample appointment types + the falling-through examples (Marin/Dustin/Owen).

---

## Build order (the "order of prompts")

Each step is a self-contained Lovable prompt with an **acceptance check**. Build and verify in
order; steps 1–13 are the purchased core, 14+ are future phases.

### 1 — Scaffold + auth + roles
> "Create a mobile-friendly ops web app called 'Takoy Designs · OPS' with email/password auth via
> Supabase. Top nav tabs: Calendar, Pipeline, Discuss, Setup, plus Sign out. Add a `role` on each
> user: `owner`, `staff`, `assistant`. After login, land on the Calendar tab. Olive/forest-green
> brand on off-white."
- ✅ Can sign in; role stored; non-owners can't reach Setup.

### 2 — Data model + RLS
> "Create Supabase tables per docs/tanya-crm/05-data-model.md: users/staff, clients, appointments,
> appointment_types, referral_sources, budget_tiers, property_types, leads, time_off, reminders,
> pipeline stages, clickup_links. Add Row-Level Security: all internal users can read all
> appointments/clients; only `owner` can write to config tables (types/sources/tiers/property_types
> /staff). Seed the demo mock data."
- ✅ Tables exist; RLS blocks a staff user from editing appointment_types; seed data loads.

### 3 — Team Calendar read view
> "Build the Team Calendar (Calendar tab): day/week toggle, Today + prev/next date nav, a **Who**
> filter (Everyone + per-staff checkboxes with color dots) and a **What** filter (All types + per
> type). Render appointments in a week grid, color-coded by appointment type, labelled
> `Type · Client` with a `City · detail` sub-line. Match assets/demo-jun22-calendar-sidepanel.png."
- ✅ Filtering by Who and What updates the grid; colors match types; works on mobile width.

### 4 — Appointment side-panel (view/edit)
> "Clicking an appointment opens a right-side panel showing editable Title, Start, End, Address,
> Notes, plus a read-back of the **customer's** Phone/Email/Status. Buttons: Save changes, Cancel
> appointment. Phone/email are tap-to-call / tap-to-text. Match assets/demo-jun22-calendar-sidepanel.png."
- ✅ Edits persist; cancel voids the appointment; customer contact shown (not the rep's).

### 5 — New Appointment modal + double-booking guard
> "Add '+ New appointment' and tap-an-open-slot to open a New Appointment modal: Client typeahead
> with 'Or create a new client', Type, Assigned to (any staff), Start/End, Budget tier
> (<$2k/$2–5k/$5–10k/$10k+), Property type, Title, Address, Notes. On Book appointment, **prevent
> booking two appointments for the same assigned staff member at overlapping times**. Match
> assets/demo-jun22-new-appointment-modal.png."
- ✅ Booking a new client works; overlapping booking for the same staff is rejected with a message.

### 6 — Time-off / vacation blocking
> "In My Settings add a Time Off section (add/remove a start–end range with a reason:
> Vacation/Personal). Blocked ranges render on the team calendar as muted 'Unavailable — reason'
> bars and prevent booking that staff member, **without** exposing personal calendar events."
- ✅ Adding time off shows 'Unavailable' to everyone and blocks bookings in that range.

### 7 — Pipeline dashboard + falling-through logic
> "Build the Pipeline tab (last 30 days): KPI tiles Set Rate, Avg Quote, Won Value, Falling
> Through; funnel bars Inquiries→Consults Booked→Quotes Sent→Won; Top Sources chips (editable
> list); and a 'Falling through the cracks' list of inquiries with no booked/active consult,
> showing source·city·budget and **days since last contact**, each row clickable to email/text or
> book. Match assets/demo-jun22-pipeline-full.png."
- ✅ Metrics compute from real data; a lead with no consult appears in falling-through with correct day count.

### 8 — Text + email reminders/confirmations
> "On booking, send the client a confirmation by **text (Twilio) and email (Resend)**. Add a
> scheduled Edge Function that sends a reminder N hours before each appointment. Reminder wording
> is configurable in Setup. Respect quiet hours (Mountain Time) and STOP/opt-out."
- ✅ Booking triggers a text + email; a test appointment gets a reminder at the configured lead time.

### 9 — Google Calendar sync
> "Add per-user Google Calendar OAuth in My Settings. Two-way: app appointments push to the user's
> Google calendar; the user's Google busy blocks appear on the team calendar as 'Unavailable'.
> Owner can keep viewing personal events in Apple/iCal separately."
- ✅ Connecting Google shows external busy blocks as unavailable and pushes a booked appointment out.

### 10 — ClickUp auto-project on booking
> "When an appointment is booked, call the ClickUp API to create a project/task for that customer
> in the configured workspace/list, and store the link on the appointment. Provide a Setup field
> for the ClickUp workspace/list ID and API token."
- ✅ Booking creates a ClickUp task and the appointment stores its link.

### 11 — Weekly scorecard email
> "Add a scheduled Edge Function that emails the owner a weekly summary every Monday: inquiries,
> set rate, quotes sent, jobs won, $ sold, broken down per salesperson."
- ✅ A manual run sends a correctly-totaled scorecard email.

### 12 — Admin Setup screens
> "Build the Setup tab (owner only): manage Team members (name/phone/email/color/role),
> Appointment types (+color), Referral sources (**remove 'House', include 'Facebook'**), Budget
> tiers, Property types, and Field config. Enforce owner-only writes via RLS from step 2."
- ✅ Owner can add a type/source; a staff user cannot open Setup.

### 13 — Mobile polish
> "Ensure calendar, side-panel (as bottom sheet), modal, and pipeline are fully usable on phones;
> tap targets ≥44px; no horizontal scroll; test at 375px width."
- ✅ Full booking flow completes on a 375px viewport.

### 14+ — Future phases (documented, build when greenlit)
- **14** Public self-booking page (per-type opt-in) — `assets/slide-layer3-never-miss.png`.
- **15** Unified inbox (Facebook/Instagram/email/text per client) → feeds pipeline inquiries.
- **16** AI receptionist (after-hours answer + intake + self-book offer).
- **17** Voice triage.

---

## Delivery notes
- **Timeline target:** core (steps 1–13) in ~30 days, matching the "live in about 30 days" plan
  and the June 11 commitment (calendar by end of month, conversion tracking by first half of July)
  [C2]. `assets/slide-week1-4-live-in-30-days.png` shows the Week 1–4 rollout Tanner presented.
- **Migration/rollback:** each step is an additive Supabase migration; keep migrations reversible.
  ClickUp/Google/Twilio are integrations layered on a working core, so they can be toggled off
  behind Setup flags if a provider isn't ready.
