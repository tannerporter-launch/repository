# Agent setup instructions — Screenwatch

You are setting up "screenwatch" on the user's machine: a background daemon that captures a screenshot + frontmost-app metadata every 5 seconds into daily folders, for later AI analysis. Reference implementations are in this folder — adapt them, don't reinvent them. **You are not done until you have verified a real image file AND a metadata line with a non-empty app name exist on disk.**

## Target layout (all platforms)

```
~/screenwatch/                       (Windows: %USERPROFILE%\screenwatch\)
├── days/YYYY-MM-DD/
│   ├── HH-MM-SS.webp (or .jpg)     screenshots, ~1568px wide, ~40-100KB
│   └── log.jsonl                    one line per 5s tick:
│                                    {"t","epoch","app","window","url","img"}
├── notes/YYYY-MM-DD.md              analysis output (created later)
├── observations.md                  recurring-inefficiency ledger (created later)
└── daemon.log                       capture errors
```

Core parameters (keep unless the user objects): 5s interval; skip when idle >90s; if app+window+url unchanged, save an image only every 6th tick; resize to 1568px wide; WebP quality ~35 if ffmpeg exists, else JPEG ~55; delete image folders older than 30 days but never delete notes/observations.

## macOS

Use `mac/capture-loop.sh` (tested, working) and `mac/com.screenwatch.plist`. Steps:

1. Copy `capture-loop.sh` to `~/screenwatch/bin/`, make executable. It auto-detects ffmpeg and falls back to `sips` JPEG.
2. **Permissions require an app bundle with a compiled main executable.** Screen Recording grants attach to a bundle's code identity — a bare script under launchd is attributed to `/bin/bash` and silently denied, and a script *inside* a bundle is still attributed to the interpreter. Build the wrapper:
   - Create `~/Applications/Screenwatch.app/Contents/{MacOS,}`, add `mac/Info.plist`, compile `mac/wrapper.c` with `cc -o .../Contents/MacOS/screenwatch mac/wrapper.c` (needs Xcode CLT; run `xcode-select --install` if missing), then `codesign -s - --force --identifier com.screenwatch ~/Applications/Screenwatch.app`.
3. Install the launchd agent: fill the plist's paths, copy to `~/Library/LaunchAgents/com.screenwatch.plist`, `launchctl bootstrap gui/$(id -u) ...`.
4. Have the user grant **Screen & System Audio Recording** AND **Accessibility** to `~/Applications/Screenwatch.app` in System Settings → Privacy & Security (they must click + and navigate to `~/Applications` — the home-folder one, Cmd+Shift+G helps). Prompts often DON'T appear for launchd daemons — send them to System Settings directly. If they granted before you re-signed the binary, the grant is stale: they must remove (–) and re-add the app.
5. Restart the daemon after any grant: `launchctl kickstart -k gui/$(id -u)/com.screenwatch`.

### macOS gotchas (each cost us real debugging time — don't rediscover them)
- `screencapture` **refuses dot-prefixed filenames** (`.tmp.png`) with `cannot write file to intended destination` — the *exact same message* as a permission denial. Never use hidden temp names, and don't assume that message means TCC.
- AppleScript resolves app dictionaries at **compile time**: `tell application "Arc" ... URL of active tab ...` is a syntax error on machines without Arc, killing the whole script. Query System Events first, then run a *separate* per-browser osascript only when that browser is frontmost (the reference script does this).
- Re-signing the wrapper binary invalidates existing TCC grants (ad-hoc signatures are hash-based). Compile once, sign once, THEN have the user grant.
- Grants only take effect after the process restarts.
- launchd doesn't inherit the user's PATH — use absolute paths for homebrew binaries.

## Windows

Use `windows/capture-loop.ps1` as the base. It uses .NET (`System.Drawing`) for capture/resize/JPEG, `GetForegroundWindow`/`GetWindowText` P/Invoke for app+window metadata, and `GetLastInputInfo` for idle skip. Browser URL capture is skipped on Windows (window titles carry the page title, which is usually enough — note this to the user; UI Automation URL capture is an optional upgrade).

1. Copy the script to `%USERPROFILE%\screenwatch\bin\`.
2. Register a logon task (per `windows/install-notes.md`): `schtasks /Create /TN Screenwatch /SC ONLOGON /TR "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File %USERPROFILE%\screenwatch\bin\capture-loop.ps1"` then `/Run` it once to start now.
3. No screen-recording permission dialogs on Windows; it should just work. If frames are black, the user is on a protected/DRM surface or an RDP session — note it and move on.
4. If `ffmpeg` is on PATH, prefer WebP re-encode; otherwise JPEG ~50 is fine.

## Linux

No reference script; write one. X11: `scrot` or `import` + `xdotool getactivewindow getwindowname` + `xprintidle`. Wayland: `grim` (wlroots) or `gnome-screenshot`; active-window metadata depends on compositor (`hyprctl activewindow`, `swaymsg -t get_tree`) — do your best and log what's unavailable as empty strings. Run it as a systemd user unit (`systemctl --user enable --now screenwatch.service`). Same folder layout, same dedupe/idle/prune rules.

## Analysis setup (all platforms)

- If the user runs **Claude Code**: install `skill/screenwatch/` into `~/.claude/skills/screenwatch/` so they get `/screenwatch analyze`, `/screenwatch optimize`, `/screenwatch status`. On Windows adjust the paths inside SKILL.md.
- Otherwise: point them at `ANALYSIS-PROMPTS.md` — copy-paste prompts that work in any agent that can read files and images.
- Offer (don't force) a scheduled nightly analysis if their agent supports scheduled/cron runs.

## Mandatory end-to-end verification

1. Daemon process is running (and survives a restart of the process manager).
2. At least one image file exists in today's folder and is between 15KB and 500KB.
3. The newest `log.jsonl` line has a **non-empty `"app"`** (empty means the metadata permission/tooling is broken — on macOS that's the Accessibility/Automation grant).
4. Open one captured image yourself (you, the agent, with vision) and confirm on-screen text is legible.
5. Tell the user: where files live, how to pause/resume (mac: `launchctl bootout`/`bootstrap`; win: `schtasks /End /TN Screenwatch` / `/Run`), the ~30-day image retention, and the privacy note from README.md.

If any check fails, debug it now — do not declare success on a partial setup.
