# 04 · Non-Functional Requirements

Quality attributes for hosting, speed, security, and reliability. Tags: **[C1]** May ·
**[C2]** June 11 · **[C3]** June 22. IDs use `NFR-###`.

## Performance & speed

| ID | Requirement | Target / notes | Source |
|----|-------------|----------------|--------|
| NFR-001 | Calendar loads fast on mobile | First meaningful paint < ~1.5s on 4G/LTE; a rep on the phone can book without waiting | [C1][C3] |
| NFR-002 | Booking is near-instant | Book action confirms in < ~1s; async work (SMS/email/ClickUp) runs in background, not blocking the UI | [C1] |
| NFR-003 | Pipeline recompute | KPIs/funnel/falling-through reflect new bookings within seconds | [C3] |
| NFR-004 | Filter responsiveness | Who/What filters update the grid client-side, no full reload | [C3] |

## Hosting & backend

| ID | Requirement | Target / notes | Source |
|----|-------------|----------------|--------|
| NFR-010 | Managed, serverless hosting | Frontend on edge (Lovable/Vercel); DB on Supabase managed Postgres — minimal ops for a small business | — |
| NFR-011 | Accessible anywhere | Public web app reachable on any phone/desktop browser; no VPN, no install | [C1][C3] |
| NFR-012 | Scales with the team | Handle team growth (new reps, second salesperson) without re-architecting; usage is small-team scale, not high-traffic | [C1][C2] |
| NFR-013 | Availability | Aim ≥ 99.9% (lean on Supabase/Vercel SLAs); scheduling is business-critical during work hours (MT) | [C1] |

## Security & privacy

| ID | Requirement | Target / notes | Source |
|----|-------------|----------------|--------|
| NFR-020 | Row-Level Security | Enforce roles in the DB (Supabase RLS), not just the UI (see doc 06) | [C2] |
| NFR-021 | Owner-restricted config | Only the owner can edit config fields (types/sources/tiers/field config) to protect data integrity | [C2] |
| NFR-022 | PII handling | Customer name/phone/email/address are PII — encrypt at rest (Supabase default) and in transit (HTTPS/TLS) | [C3] |
| NFR-023 | Secret management | Twilio/Resend/Google/ClickUp keys in server-side secrets only, never shipped to the browser | — |
| NFR-024 | Least privilege | Staff/assistant/external roles get only the access their job needs | [C2][C3] |
| NFR-025 | Auth hygiene | Owner provisions accounts; support password reset and offboarding (revoke access) | [C2] |

## Messaging compliance & deliverability

| ID | Requirement | Target / notes | Source |
|----|-------------|----------------|--------|
| NFR-030 | Text open-rate priority | Texts are the primary reminder channel because email gets ignored | [C2][C3] |
| NFR-031 | SMS compliance | A2P 10DLC brand/campaign registration; include opt-out (STOP); honor quiet hours (no late-night texts, Mountain Time) | [C2] |
| NFR-032 | Email deliverability | Authenticated sender (SPF/DKIM via Resend) so confirmations/scorecards don't hit spam | [C2] |
| NFR-033 | Reminder reliability | Scheduled sends fire on time; retries on transient provider failures | [C2] |

## Calendar-sync reliability

| ID | Requirement | Target / notes | Source |
|----|-------------|----------------|--------|
| NFR-040 | Two-way Google sync | App appointments push out; external busy blocks pull in as "Unavailable" to prevent conflicts | [C2][C3] |
| NFR-041 | Privacy of personal events | Personal calendar events show only as "Unavailable" on the team calendar — no detail leaks | [C3] |
| NFR-042 | Conflict prevention | Same-staff double-booking is blocked at write time (see FR-058) | [C3] |
| NFR-043 | Sync resilience | Sync failures are logged and retried; a sync outage never blocks in-app booking | [C3] |

## Data integrity, backup, auditability

| ID | Requirement | Target / notes | Source |
|----|-------------|----------------|--------|
| NFR-050 | Backups | Automated daily Postgres backups (Supabase); point-in-time recovery where available | — |
| NFR-051 | No lost leads | The pipeline's falling-through logic must never silently drop an inquiry — that's the core value | [C1][C3] |
| NFR-052 | Auditable changes | Track who created/edited/cancelled an appointment (owner wants to "know what's happening") | [C1] |
| NFR-053 | ClickUp consistency | If ClickUp project creation fails, surface it and allow retry — don't lose the linkage | [C2] |

## Usability

| ID | Requirement | Target / notes | Source |
|----|-------------|----------------|--------|
| NFR-060 | Simplicity first | "Keep it simple" — minimal clicks to book; no role gymnastics | [C3] |
| NFR-061 | Mobile ergonomics | Tap targets ≥44px; side-panel as bottom sheet on phones; no horizontal scroll at 375px | [C1][C3] |
| NFR-062 | Fits existing habits | Sits in front of ClickUp + personal calendars; enhances, doesn't replace | [C1][C2] |

## Cost

| ID | Requirement | Target / notes | Source |
|----|-------------|----------------|--------|
| NFR-070 | Sane run cost | Keep monthly running cost modest — Tanya is cost-sensitive (balked at $1000s/mo quoting tools; chose on-demand support over a recurring subscription) | [C1][C2] |
| NFR-071 | Replace pain, not add it | Should relieve the $250/mo cumbersome quoting workflow frustration, not stack another heavy tool | [C1] |
