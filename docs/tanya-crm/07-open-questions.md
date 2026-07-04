# 07 · Open Questions — the variables still needed to finish planning

Direct answer to *"Let me know if I am missing any variables needed to plan out this custom web
app."* These are the decisions/data not yet nailed down in the three calls. Ordered by how much
they block the build. Tags: **[C1]** May · **[C2]** June 11 · **[C3]** June 22.

## 🔴 Blockers — needed before the relevant build step ships

1. **Lead/inquiry source of truth.** The pipeline "falling through the cracks" list needs
   un-booked inquiries to come from *somewhere*. In the demo it's calendar-driven — but a cold
   Instagram DM that never books won't appear unless it's captured. Decide: manual entry, a
   Facebook/Instagram lead-form webhook, or wait for the future unified inbox? (Affects step 7.) [C3]
2. **Business hours + time zone confirm (Mountain).** Drives reminder send windows, SMS quiet
   hours, and any future self-booking availability. What are the actual working hours per day? [C1]
3. **Reminder wording + cadence.** June 11 action item still pending from Tanya: preferred
   text/email wording, branding, and how far ahead reminders fire (e.g., 24h + 1h?). (Step 8.) [C2]
4. **SMS sender + A2P 10DLC registration.** Which number sends texts, and completing brand/campaign
   registration for compliant business texting. Without this, texts (the priority channel) can't
   go live. (Step 8, NFR-031.) [C2]
5. **ClickUp specifics.** Workspace/list ID + API token, and **which ClickUp stages map to the
   pipeline** (measuring / quoting / installation). Needed for auto-project creation. (Step 10.) [C2]
6. **Google Calendar sync scope.** One-way or two-way per user? Who grants OAuth consent for each
   staff member? Confirm Apple/iCal is view-only-personal (owner keeps it) vs. needs its own sync. (Step 9.) [C3]

## 🟠 Configuration values — needed to seed the lists

7. **Appointment types + colors.** Final list (Initial Consult, Install Walkthrough, Design Review,
   Site Visit, Final Reveal, Networking, Warranty…?) and each color. Seen in demos but not confirmed. [C3]
8. **Property types.** The New Appointment "property type" field needs real values (Residential /
   New build / Commercial / builder job?). Not enumerated on any call. [C2][C3]
9. **Referral sources — final list.** Confirmed: remove "House", add "Facebook". Keep Website,
   Referral, Instagram, Google, Houzz, Repeat client? Anything else (BNI/networking, builder)? [C3]
10. **Budget tiers — confirmed** as `<$2k / $2–5k / $5–10k / $10k+` [C3]. (Listed for completeness;
    no action unless Tanya changes them.)
11. **Team roster + contact info.** Tanya sent onboarding info (names/emails/phones). Confirm it's
    complete for all who need logins (Tanya, Nissa, Carolyn, Tracy, assistant) and set each person's
    role/level. [C2][C3]
12. **Appointment status values.** Confirm the status set (scheduled/confirmed/completed/
    rescheduled/cancelled) matches how the team actually tracks it. [C3]

## 🟡 Scope / boundary decisions

13. **Quote data source.** Quoting engine is deferred [C1][C2]. So "Quotes sent" / "Avg quote" in
    the pipeline will be a **manual flag + amount** on the appointment. Confirm that's acceptable
    (vs. no quote metric at all until a future integration).
14. **Commission tracking.** Today it's QuickBooks + a spreadsheet with a bookkeeper [C1]. In or out
    of scope for this app? (Recommend: out for launch, revisit later.)
15. **Self-booking.** Which appointment types are self-book-enabled (Tanya leaned toward
    networking/marketing only, not consults)? Off by default per type. [C1][C2]
16. **Assistant permissions.** Should the remote student assistant be able to cancel/edit *others'*
    appointments, or just create? Currently modeled the same as staff (doc 06). [C2]
17. **Future-phase go/no-go + budget.** AI receptionist, voice triage, unified inbox — Tanner is
    re-sending the options email; Tanya to review and pick. These stay documented-not-built until
    chosen. [C2][C3]

## 🟢 Operational / housekeeping

18. **Account provisioning & offboarding.** Who creates logins, password policy, and how access is
    revoked when someone leaves. [C2]
19. **Domain / URL** for the app (subdomain of takoydesigns.com? a separate ops domain?). [C3]
20. **Data migration.** Any existing ClickUp/Google Calendar data to import at launch, or start
    fresh? [C1]
21. **Weekly scorecard recipients + day/time.** Confirmed to Tanya Monday-ish [C2]; confirm exact
    send time and whether reps get their own.

---

### Already answered (so we don't re-ask)
- Unified calendar, everyone sees everything, any staff any type — **yes** [C3].
- Config editing restricted to owner — **yes** [C2].
- Text **and** email reminders — **yes**, text prioritized [C2][C3].
- Mobile-friendly website, no native app — **yes** [C3].
- Keep ClickUp; auto-create project on booking — **yes** [C2].
- Custom quoting — **deferred** [C1][C2].
- Package/pricing/payment — **closed & paid** (Operating System, 50% upfront via bank transfer) [C2].
