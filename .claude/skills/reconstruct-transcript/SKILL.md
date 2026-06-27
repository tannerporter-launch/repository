---
name: reconstruct-transcript
description: "Use when the user pastes or points to a raw/auto-generated transcript (meeting, sales/client/prospect call, interview, or video) and wants it cleaned up, reconstructed, corrected, summarized, or analyzed — or when they provide a corrected version / a fix to remember. Produces a faithful reconstructed transcript plus summary, sequential action items by role, objections/risks, sales insights, and key facts. For fetching a YouTube transcript first, use the `youtube` skill."
user-invocable: true
allowed-tools: Read, Edit, Bash(python3 *)
---

# Reconstruct & analyze a transcript

Turn a messy/auto-generated transcript into the most accurate reconstruction
possible, then analyze it. Works on any transcript text (Zoom, Fireflies,
YouTube captions, etc.). To first *fetch* a YouTube transcript, use the
`youtube` skill, then process it here.

## Before you start: load memory

Always apply what we've learned before reconstructing:

1. **Term glossary** — `.claude/skills/youtube/corrections.json` (misheard →
   correct: names, tools, acronyms, jargon). Apply deterministically; you can
   run it over pasted text with:
   ```bash
   python3 .claude/skills/reconstruct-transcript/scripts/correct_text.py transcript.txt
   ```
2. **Learned rules** — `.claude/skills/reconstruct-transcript/learned_rules.md`
   (participants & roles, speaker patterns, formatting preferences, recurring
   structural fixes). Read and apply these.

## Step 1 — Reconstruct the transcript

Each transcript may contain: incorrect words, missing sections, duplicated
sections, speaker-label errors, punctuation errors, formatting issues,
hallucinated phrases, garbled passages, and mis-transcribed names/tools/acronyms.

Requirements:
- **Preserve the full conversation** — every meaningful detail: side comments,
  objections, commitments, questions, numbers, names, and next steps. **Do not
  summarize or omit meaningful content** in the reconstruction.
- **Correct obvious transcription errors** when the intended meaning is
  reasonably clear (apply the glossary + context).
- **Fix speaker labels** where context allows; use **clear speaker labels**.
- **Clean punctuation and readability** without changing meaning.
- Remove duplicated/garbled artifacts; note where a section appears **missing**.
- Mark uncertain wording as `[unclear]` or `[low confidence: possible wording…]`.
- If speaker attribution is uncertain, label it `[Speaker unclear]`.

## Step 2 — Produce the output, in this order

### 1. Reconstructed Transcript
The full, cleaned conversation with clear speaker labels and uncertainty markers.

### 2. Summary
Concise but complete — no meaningful content dropped.

### 3. Action Items (sequential)
List in the order they should be done. **Categorize by business role/function**
(e.g. Sales, Marketing, Ops, Finance, Product/Tech, Client/Customer). For each:
- **Task**
- **Context**
- **Why it matters**
- **Deadline / timing** (if mentioned)

### 4. Objections, Risks & Friction
Any objections, hesitations, doubts, risks, pricing concerns, timing concerns,
technical concerns, or unstated friction.

### 5. Sales / Strategy Insights
*(Only if this is a business, sales, client, or prospect call.)*
- Pain points
- Buying signals
- Decision criteria
- Urgency level
- Budget signals
- Likely next best step
- Recommended follow-up angle

### 6. Key Facts & Context
Names · company names · industry · tools/software · pricing · dates · deadlines ·
needs · current systems · desired outcomes.

## Step 3 — Remember fixes the user provides (the learning loop)

Whenever the user supplies a correction — a corrected transcript version, or
"X should be Y", or "this name is …" — **capture it so it sticks next time**:

1. Identify each specific fix by comparing against the prior version/context.
2. Classify and store:
   - **Term-level substitution** (a word/name/tool/acronym consistently
     misheard → its correct form): add it to
     `.claude/skills/youtube/corrections.json` under `corrections` as
     `"misheard (lowercase)": "Correct"`. This is auto-applied everywhere.
   - **Non-substitution rule** (a participant's name↔role, a speaker pattern, a
     formatting/labelling preference, a recurring structural fix): append a
     dated bullet to `learned_rules.md`.
3. Apply the fix to the current output and **briefly confirm what you stored and
   where**, so the user can see the memory growing.

Keep entries precise and high-precision — prefer specific terms over broad words
that could cause false replacements (the glossary matches whole words).
