# Changelog

All notable changes to the YouTube skill build.

## [1.1.0] — 2026-06-26

Audit-driven overhaul for reliability, repeatability, and maintainability.

### Changed
- **Discoverability (critical):** moved skills from `.agents/skills/` to
  `.claude/skills/`. Claude Code discovers project skills only in
  `.claude/skills/` (and `~/.claude/skills/`), so the previous layout was a
  no-op — the skills were never loaded by Claude Code's skill system.
  (Verified against code.claude.com/docs/en/skills and the `skills` CLI
  agent-path mapping.)
- **Consolidated** the 12 overlapping skills into one `youtube` skill (full
  toolkit) plus two thin aliases (`transcript`, `youtube-full`).
- **Reconciled API docs with the live OpenAPI spec** (`openapi.json`, v1.0.0):
  search/channel pagination is cursor-based via `continuation`; the previously
  documented `limit` parameter does not exist on the public API.
- **Bundled** `yt_transcript.py` inside the skill and referenced it via
  `${CLAUDE_SKILL_DIR}` so it resolves from any working directory.
- **Slimmed frontmatter** to Claude Code-supported fields and added
  `allowed-tools` to reduce permission prompts. Removed no-op fields
  (`version`, `compatibility`, `required_environment_variables`, `metadata`).
- Corrected the Python floor to **3.9+** (required by yt-dlp).

### Added
- `requirements.txt` (yt-dlp floor pin).
- `tests/test_yt_transcript.py` (offline unit tests) + `.github/workflows/ci.yml`
  (CI on Python 3.9/3.11/3.12).
- `.gitignore` (ignores `.claude/settings.local.json`, `out/`, `__pycache__`).
- Real top-level `README.md` with setup, usage, troubleshooting, maintenance,
  and uninstall/rollback. This `CHANGELOG.md`.
- Documented credential pattern: `TRANSCRIPT_API_KEY` via
  `.claude/settings.local.json` `env` (never in chat or tracked files).

### Removed
- `skills-lock.json` and the `npx skills` lockfile/update flow (skills are now
  managed directly in this repo).

## [1.0.0] — 2026-06-26

### Added
- Installed 12 YouTube/transcript skills via `npx skills add
  ZeroPointRepo/youtube-skills`.
- `scripts/yt_transcript.py`: local `yt-dlp` fallback that auto-engages on any
  TranscriptAPI failure and emits title/description/transcript; flags `--out`,
  `--list-langs`, `--format`, `--lang`, `--no-api`, `--no-install`; retry on
  transient API errors (408/429/5xx).

### Security
- Removed `references/auth-setup.md` from all skills (it instructed the agent to
  write API keys/tokens to temp files to evade redaction and to auto-register an
  account). Replaced with a safe, key-via-env setup instruction.
