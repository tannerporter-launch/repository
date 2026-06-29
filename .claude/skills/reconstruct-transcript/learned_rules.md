# Learned transcript rules (memory)

Durable, non-substitution learnings the agent applies when reconstructing
transcripts. **Term-level word fixes do NOT go here** — those go in
`.claude/skills/youtube/corrections.json` (auto-applied). Use this file for
things a simple find-and-replace can't capture.

The agent appends here when the user provides a fix that is a rule, preference,
or fact rather than a single word swap. Keep entries dated and specific.

---

## Participants & roles
<!-- name ↔ role/company, so speaker labels and attribution are correct -->
- 2026-06-27: **Sabri Suby** — founder of **King Kong** (agency, kingkong.co) and
  **Kong** (AI ad-creative tool, go.kingkong.co/kong). Auto-captions mishear his
  name as "Sabri", "Subrey", or "Mubry" → always **Sabri** / **Sabri Suby**.

## Speaker-labeling patterns
<!-- e.g. "the host is usually the first speaker", "two-person call: Rep vs Prospect" -->
- 2026-06-27: Sabri Suby's videos are **single-speaker monologues** — present as
  continuous prose under one speaker label, not back-and-forth turns. Quoted
  inner monologue ("they think, 'Sabri, how do I…'") is him role-playing the
  viewer, not a second speaker.

## Formatting & style preferences
<!-- e.g. timestamp style, how to mark uncertainty, paragraphing, headings -->
- 2026-06-27: For numbered "hacks" content, paragraph the reconstruction by hack
  and keep each hack's "do this now" instruction intact (it maps to an action item).

## Recurring structural fixes
<!-- e.g. "intro music section is always garbled — drop it", known duplicate patterns -->
- _(none yet)_

## Domain notes (ads/marketing) — context-dependent fixes NOT safe for the global glossary
<!-- 'bias'/'row' are common words, so these are judgment calls, not blanket swaps -->
- 2026-06-27: **ROAS** is mis-transcribed many ways — "rorwaz", "rorowaz",
  "row as", and sometimes a bare **"row"** ("a six row" → "a six ROAS").
  The first three are in the glossary; **"row" is NOT** (too common) — correct it
  to ROAS by context (when preceded by a number or discussing return on ad spend).
- 2026-06-27: **"media bias" → "media buyer"** in an ads context ("not what your
  media bias says" → "media buyer"). Not glossared because "media bias" is a real
  phrase; fix by context.
- 2026-06-27: **Andromeda** = Meta's ad-delivery AI system; **CBO** = Campaign
  Budget Optimization; **VSL** = Video Sales Letter. Keep capitalization.

### Dev / mobile tooling (from the "Claude Code mobile apps" course)
- 2026-06-27: Auto-captions mangle **Claude/Claude Code** as "cloud code",
  "clot", "claw", "clad", "clod" and **Anthropic** as "entropic", "Enro". These
  are real words / too ambiguous for the global glossary — fix by context to
  **Claude / Claude Code / Anthropic**. (Unambiguous spellings like "enthropic",
  "superbase" ARE in corrections.json.)
- 2026-06-27: Other context-only dev fixes: "anti-gravity" → **Antigravity**
  (Google IDE); "dribble" → **Dribbble**; "platform.cloud.com" →
  **platform.claude.com**; "claude.ai/lo" → **claude.ai/code**;
  "Mifflin St(j)eor" equation; "Nick Sarah/Sarrive" → **Nick Saraev**.
- 2026-06-27: Glossary canonicalizes: Supabase, PostgREST, Antigravity, Expo Go,
  React Native, Excalidraw, TestFlight, MyFitnessPal, Claude Code, Anthropic.

### Business / AI-consulting (from Nick Saraev videos)
- 2026-06-27: **Nick Saraev** runs **Maker School** (community on **Skool**,
  skool.com) and **Leftclick** (AI consulting agency). Single-speaker monologues.
- 2026-06-27: Context-only fixes (real words — NOT safe for the global glossary):
  "school" → **Skool** (the platform) when it means the community tool, not a
  literal school; "Santa" → **Asana** (PM tool) in an access/tooling context;
  "Tears" / "tears" as a sign-off → **"Cheers."**; a stray "nad" → **n8n**
  ("random nad workflow" → "n8n workflow").
- 2026-06-27: Tools in his stack: Make.com, n8n, Instantly (cold email), Apify,
  Anymailfinder, PandaDoc / Better Proposals, Gumroad, Loom, Upwork.
