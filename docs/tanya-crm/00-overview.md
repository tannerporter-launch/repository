# 00 · Overview

## Product vision

A single, mobile-friendly operations web app that gives the whole Takoy Designs team
**one shared calendar** and **one live pipeline view** — so any team member can see every
appointment, book a customer while they're still on the phone, and know at a glance which
leads are about to fall through the cracks. It sits *in front of* the tools the team already
uses (ClickUp for project management, Google/Apple calendars for personal scheduling) rather
than replacing them.

## Business context

| | |
|---|---|
| **Business** | Takoy Designs — custom window treatments (blinds, shades, Roman/cell shades, shutters, motorized) |
| **Owner** | Tanya Koyle |
| **Model** | Fully custom, **in-home** sales (not a storefront); orders from all major suppliers |
| **Market** | Boise / Eagle / Meridian, ID area; Mountain Time |
| **Revenue** | ~$2.8M last year → **goal $3M** this year [C1] |
| **Avg project value** | ~$6,000; social-media leads close at ~30–50% [C2] |
| **Lead sources** | Instagram ads (primary focus), Facebook, Google/website, referrals, builders, Houzz, repeat clients |
| **Builder** | Web Launch Pros (Tanner Porter) |

## The team (roster) [C2]

| Person | Role in business | App role (see doc 06) |
|--------|------------------|------------------------|
| **Tanya Koyle** | Owner — does everything, wants full visibility & control | Owner / Admin |
| **Nissa** | Admin — answers phones, books appointments | Staff (booking) |
| **Carolyn** | Sales rep (mostly sales) | Staff (sales) |
| **Tracy** | Sales / flex | Staff (sales) |
| Remote student assistant | Support tasks | Assistant (limited) |
| External install subcontractors | Installations | External / Subcontractor |

> Decision [C3]: **No role-based differentiation on the calendar** — everyone sees
> everything and any staff member can take any appointment type. "Keep it simple."
> The only restriction is that **editing configuration fields is limited to the owner** [C2].

## The core problem (why this exists)

- No shared calendar → admin can't see reps' availability → "let me have someone call you
  back" → **4–5 leads lost per month** [C1]; roughly **1 lead/week slips through** [C2].
- ~1 hour/day per person wasted on scheduling ping-pong [C1].
- **No conversion tracking** at all — Tanya can't see inquiry→consult→quote→won [C1].
- Tools are fragmented: ClickUp (PM) + a separate quoting tool ($250/mo, cumbersome) +
  Google Calendar + QuickBooks/spreadsheet for commissions — none integrated [C1].

## Scope: bought vs. deferred

**Purchased — "Operating System" package** [C2] ($9,800 setup / negotiated to a $9,506
bank-transfer total, 50% upfront; monthly support moved to on-demand):

- ✅ One unified team calendar (Who / What / date filters, color-coded by type)
- ✅ Appointment create/edit (client, budget tier, property type, type, assigned staff, slot, notes)
- ✅ Lead pipeline & conversion tracking (set rate, avg quote, won value, falling-through)
- ✅ Text **and** email appointment reminders/confirmations
- ✅ Metrics dashboard + automated weekly scorecard email
- ✅ ClickUp: auto-create a project when an appointment is booked
- ✅ Per-person time-off / vacation blocking (shows "unavailable", hides personal event detail)
- ✅ Google/Apple calendar sync
- ✅ Mobile-friendly website (no native app)

**Deferred / future phases** (documented so the build leaves room for them):

- 🔜 AI receptionist (after-hours missed-call handling) — optional add-on [C2][C3]
- 🔜 Voice triage — optional add-on [C3]
- 🔜 Unified inbox (Facebook/Instagram DMs + email + text in one thread) [C2][C3]
- 🔜 Public self-booking links (esp. networking/marketing appointments) [C1][C2]
- ❌ Custom quoting engine — **explicitly deferred** (supplier pricing too fluid/unreliable to automate confidently) [C1][C2]
- ❔ Commission tracking — stays in QuickBooks + spreadsheet for now [C1]

## Glossary

| Term | Meaning |
|------|---------|
| **Inquiry** | A raw inbound lead (call, DM, form) before a consult is booked |
| **Lead** | Synonym for a not-yet-booked inquiry; appears in "falling through the cracks" if untouched |
| **Consult** | The in-home appointment where measuring + design + pricing happen |
| **Quote** | Room-by-room price emailed to the customer after the consult |
| **Job (Won)** | A quote the customer accepted; a sale |
| **Set rate** | % of inquiries that convert into a booked consult |
| **Falling through the cracks** | Inquiries with no booked/active appointment and no recent contact |
| **Appointment type** | Category of calendar event (Initial Consult, Install Walkthrough, Design Review, Site Visit, Final Reveal, Networking, etc.), color-coded |
| **Budget tier** | Coarse project-value band captured at booking: `<$2k`, `$2–5k`, `$5–10k`, `$10k+` [C3] |
| **Time off** | A staff-owned block marking a day/week "unavailable" without exposing personal event detail [C3] |

## Source calls

- **[C1] May — Discovery (phone).** Pain discovery; established the calendar + conversion gaps.
- **[C2] June 11 — Proposal & close (Zoom).** Package chosen and paid; slide deck (Layers 1–4);
  decisions on ClickUp retention, deferred quoting, text reminders, admin-restricted fields.
- **[C3] June 22 — Build check-in (Zoom).** Live demo of the working app; confirmed unified
  calendar, budget tiers, referral-source edits (remove "House", add "Facebook"), time-off,
  mobile web, calendar sync.
