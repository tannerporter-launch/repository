# 03 · Functional Requirements — every button / control

Each requirement has an ID (`FR-###`), the control, its action, the resulting state, and the
source call. "Source" tags: **[C1]** May · **[C2]** June 11 · **[C3]** June 22. Items marked
**(Future)** are documented for later phases.

## Global / navigation

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-001 | **Calendar** tab | Show S2 Team Calendar | [C3] |
| FR-002 | **Pipeline** tab | Show S5 Pipeline Dashboard | [C3] |
| FR-003 | **Discuss** tab | (Future) Show S9 Unified Inbox | [C2][C3] |
| FR-004 | **Setup** tab | Show S8 Admin Setup — **visible/enabled to owner only** | [C2] |
| FR-005 | **Sign out** | End session → return to S1 Login | [C3] |
| FR-006 | Responsive layout | Every screen usable on mobile web + desktop; no native app | [C3] |

## S1 · Login

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-010 | Email + Password fields | Capture credentials | [C3] |
| FR-011 | **Sign in** | Authenticate via Supabase → land on S2 Calendar | [C3] |
| FR-012 | Forgot password | Send reset email | — (standard) |

## S2 · Team Calendar

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-020 | **Today** | Reset view to current day/week | [C3] |
| FR-021 | **‹ / ›** date nav | Move to previous/next day or week | [C3] |
| FR-022 | **Day / Week** toggle | Switch grid granularity | [C3] |
| FR-023 | **Who** dropdown | `Everyone` (default) + per-staff checkboxes (color dots) filter the grid | [C3] |
| FR-024 | **+ Add team member** (in Who) | (Owner) add a staff member | [C2] |
| FR-025 | **What** dropdown | `All types` + per appointment-type filter | [C3] |
| FR-026 | **+ New appointment** | Open S4 New Appointment modal (empty) | [C3] |
| FR-027 | Tap an **open slot** | Open S4 modal pre-filled with that date/time/staff | [C3] |
| FR-028 | Tap an **appointment** | Open S3 side-panel for that appointment | [C3] |
| FR-029 | Color-coding | Appointments colored by **type**; label `Type · Client` | [C3] |
| FR-030 | Time-off rendering | Show muted "Unavailable — reason" bars; slot not bookable | [C3] |

## S3 · Appointment Side-Panel

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-040 | Edit Title / Start / End / Address / Notes | Update the appointment fields | [C3] |
| FR-041 | Customer Phone (tap) | Tap-to-call / copy — shows **customer's** number | [C3] |
| FR-042 | Customer Email (tap) | Tap-to-email — customer's address | [C3] |
| FR-043 | Status | Show/set status (scheduled/confirmed/completed/rescheduled/cancelled) | [C3] |
| FR-044 | **Save changes** | Persist edits; refresh calendar | [C3] |
| FR-045 | **Cancel appointment** | Void the appointment; remove from calendar; free the slot | [C3] |
| FR-046 | Close (✕) | Dismiss panel without saving | [C3] |

## S4 · New Appointment modal

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-050 | **Client** search | Typeahead over existing clients by name/phone/email | [C3] |
| FR-051 | **+ Or create a new client** | Reveal inline name/phone/email fields; create on book | [C3] |
| FR-052 | **Type** dropdown | Pick appointment type (sets color) | [C3] |
| FR-053 | **Assigned to** dropdown | Any staff member — **no type-to-person restriction** | [C3] |
| FR-054 | **Budget tier** | `Under $2k / $2–5k / $5–10k / $10k+` | [C3] |
| FR-055 | **Property type** | Pick from configured list | [C2][C3] |
| FR-056 | **Start / End** | Set appointment window | [C3] |
| FR-057 | **Title / Address / Notes** | Free-text details | [C3] |
| FR-058 | **Book appointment** | Validate → **block double-booking same staff** → create appointment → send text+email confirmation → auto-create ClickUp project → add to pipeline | [C2][C3] |
| FR-059 | **Cancel** | Dismiss without booking | [C3] |
| FR-060 | Book button disabled state | Disabled until required fields set | [C3] |

## S5 · Pipeline Dashboard

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-070 | KPI tiles | Show Set Rate, Avg Quote, Won Value, Falling-Through count (last 30 days) | [C3] |
| FR-071 | Funnel bars | Inquiries → Consults Booked → Quotes Sent → Won | [C2][C3] |
| FR-072 | Top Sources chips | Website, Referral, Instagram, Facebook, Google, Houzz, Repeat client | [C3] |
| FR-073 | Falling-through list | Inquiries with no booked consult; show source·city·budget + **days since contact** | [C3] |
| FR-074 | Falling-through row → **Email** | Email that lead directly | [C3] |
| FR-075 | Falling-through row → **Text** | Text that lead directly | [C3] |
| FR-076 | Row → Book | Open S4 pre-filled to book the lead | [C3] |

## S6 · Metrics / Weekly Scorecard

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-080 | Weekly scorecard email | Auto-email owner each Monday: inquiries, set rate, quotes, jobs won, $ sold | [C2] |
| FR-081 | Per-salesperson breakdown | Scorecard splits metrics by rep | [C2] |

## S7 · My Settings

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-090 | Edit profile | Name / phone / email / color | [C3] |
| FR-091 | **Connect Google Calendar** | OAuth; two-way sync on | [C2][C3] |
| FR-092 | **+ Add time off** | Add start–end range + reason; renders "Unavailable" | [C3] |
| FR-093 | Remove time off | Delete a block | [C3] |

## S8 · Admin Setup (owner only)

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-100 | Add/edit/remove **team member** | Manage staff, color, app role | [C2] |
| FR-101 | Add/edit/remove **appointment type** (+color) | Manage the type list | [C2][C3] |
| FR-102 | Add/edit/remove **referral source** | Incl. **remove "House"**, **add "Facebook"** | [C3] |
| FR-103 | Edit **budget tiers** | Adjust the 4 tiers | [C3] |
| FR-104 | Edit **property types** | Manage list | [C3] |
| FR-105 | **Field config** | Choose which custom fields appear — owner-locked for data integrity | [C2] |
| FR-106 | Reminder wording | Configure text/email reminder templates | [C2] |
| FR-107 | Integration settings | ClickUp workspace/list + token; SMS/email sender config | [C2] |

## Future (documented)

| ID | Control | Action → Result | Source |
|----|---------|-----------------|--------|
| FR-200 | Self-booking link (per-type opt-in) | Public page shows real openings for enabled types | [C1][C2] |
| FR-201 | Unified inbox | FB/IG DMs + email + text per client in one thread; "Add to ClickUp" | [C2][C3] |
| FR-202 | AI receptionist | After-hours answer, intake capture, offer self-book, drop into pipeline | [C2][C3] |
| FR-203 | Voice triage | Route/triage inbound calls | [C3] |
