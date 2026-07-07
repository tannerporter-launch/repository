# 06 · Roles & Permissions

Two decisions from the calls shape everything here:

- **[C3] No role-based differentiation on the calendar** — *"I just want everyone to see
  everything… we should all be able to look… and the ability to add anything we want."* Any staff
  member can be assigned any appointment type.
- **[C2] Config editing is owner-restricted** — *"administrative access to edit fields will be
  restricted to the business owner to maintain data integrity."*

So permissions are deliberately **flat for day-to-day work** and **locked only at the config layer**.

## Roles (user levels)

| Role | Who | Purpose |
|------|-----|---------|
| **Owner / Admin** | Tanya | Full access + the only one who edits configuration/fields |
| **Staff** | Nissa, Carolyn, Tracy | Full day-to-day: view everything, book/edit/cancel appointments, use pipeline, manage own time-off |
| **Assistant** | Remote student assistant | Same view + booking help, but **cannot** manage staff/config (limited) |
| **External · Subcontractor** | Installers | Not app users in core scope; stored as records; (future) may get a read-only install view |
| **External · Client** | Customers | No login in core scope; (future) self-booking page only |

## Permission matrix

| Capability | Owner | Staff | Assistant | External |
|------------|:-----:|:-----:|:---------:|:--------:|
| View team calendar (everyone) | ✅ | ✅ | ✅ | ❌ |
| Filter Who / What | ✅ | ✅ | ✅ | ❌ |
| Create appointment | ✅ | ✅ | ✅ | ❌* |
| Edit / cancel **any** appointment | ✅ | ✅ | ✅ | ❌ |
| Assign appointment to any staff | ✅ | ✅ | ✅ | ❌ |
| View pipeline & metrics | ✅ | ✅ | ✅ | ❌ |
| Email/text a lead from pipeline | ✅ | ✅ | ✅ | ❌ |
| Manage **own** time off | ✅ | ✅ | ✅ | ❌ |
| Receive weekly scorecard | ✅ | ○ (optional) | ❌ | ❌ |
| **Add / edit / remove staff** | ✅ | ❌ | ❌ | ❌ |
| **Edit appointment types** | ✅ | ❌ | ❌ | ❌ |
| **Edit referral sources** | ✅ | ❌ | ❌ | ❌ |
| **Edit budget tiers / property types** | ✅ | ❌ | ❌ | ❌ |
| **Field config (which fields appear)** | ✅ | ❌ | ❌ | ❌ |
| Integration settings (ClickUp/SMS/email) | ✅ | ❌ | ❌ | ❌ |
| Access Setup tab at all | ✅ | ❌ | ❌ | ❌ |
| (Future) Self-book via public link | — | — | — | ✅* |

`*` External access is future-phase only (self-booking page); no login in the core build.
`○` Scorecard to staff is a per-person opt-in the owner can toggle.

> Note: Staff and Assistant differ only in that Assistant cannot be given elevated tasks later;
> for the launch their day-to-day capabilities are the same. If Tanya wants to tighten this
> (e.g., stop the student assistant from cancelling others' appointments), it's a one-line RLS
> change — flagged in doc 07.

## Mapping to Supabase Row-Level Security

Enforce in the **database**, not just the UI (NFR-020).

```
-- Internal read: any authenticated internal user sees all appointments/clients/leads
policy "internal read all"        on appointments  for select using ( is_internal(auth.uid()) );
policy "internal read clients"    on clients       for select using ( is_internal(auth.uid()) );

-- Transactional write: any internal user can create/edit/cancel appointments
policy "internal write appts"     on appointments  for all    using ( is_internal(auth.uid()) );

-- Time off: a user manages only their own rows
policy "own time off"             on time_off      for all    using ( staff_id = auth.uid() );

-- Config tables: OWNER ONLY (data integrity, [C2])
policy "owner edits config"       on appointment_types  for all using ( is_owner(auth.uid()) );
policy "owner edits config srcs"  on referral_sources   for all using ( is_owner(auth.uid()) );
policy "owner edits tiers"        on budget_tiers       for all using ( is_owner(auth.uid()) );
policy "owner edits proptypes"    on property_types     for all using ( is_owner(auth.uid()) );
policy "owner manages staff"      on staff_members      for all using ( is_owner(auth.uid()) );
-- (config tables remain readable by all internal users for dropdowns)
policy "internal read config"     on appointment_types  for select using ( is_internal(auth.uid()) );
```

Helper predicates: `is_internal(uid)` = role in (`owner`,`staff`,`assistant`); `is_owner(uid)` =
role = `owner`. These back the Setup-tab visibility (FR-004) and the owner-only config buttons
(FR-100–FR-107).
