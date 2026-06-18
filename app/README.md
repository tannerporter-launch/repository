# YouTube to Reference Assets, local UI

A small local web app. Paste a live YouTube link, click Run, and watch it build
the External Example asset and the linked Internal Application asset in your
Notion Reference Assets database.

## Why it works this way

The UI does not reimplement the pipeline. It drives the yt-reference-pipeline
skill through your Claude CLI, so you get the same MCP-quality transcript
cleanup, analysis, and Notion rendering, with a one-field front end on top. The
server streams live progress from the run back to the browser.

## Requirements

- Claude Code CLI on your PATH, the command `claude`. Check with `claude --version`.
- The three skills installed where Claude can load them, for example ~/.claude/skills, with the shared folder alongside them.
- Notion MCP connected in your Claude setup, which is what the skill uses to write pages.
- Python 3. No third-party packages, standard library only.
- For the link teardown screenshots: `python3 -m playwright install chromium` once.

## Run

- Start it: `bash app/start.sh`
- Or directly: `python3 app/server.py`
- Open http://127.0.0.1:8765
- Paste a YouTube link, click Run.

## What you see

- Five live steps: yt-dlp extraction, transcript cleanup, External Example page, analysis and link teardown, Internal Application page.
- Result cards that link straight to the two Notion pages.
- A live log you can expand.
- Recent runs, stored in your browser only.

## Settings

- YT_UI_PORT, the port, default 8765.
- YT_UI_CLAUDE, the claude binary, default claude.
- YT_UI_CLAUDE_ARGS, extra args for the claude call, default --dangerously-skip-permissions so a one-click run does not pause for permission prompts. Remove it if you prefer to approve each tool call in a separate Claude session.
- YT_UI_MOCK, set to 1 to preview the UI with a scripted run, no network and no claude call.

## Security note

- The default --dangerously-skip-permissions lets the headless run use tools without prompting, which is what makes it one-click. It runs on your machine, against your own skills and your own Notion. If you would rather review each action, unset YT_UI_CLAUDE_ARGS and run the prompt in an interactive Claude session instead.

## Try the look first

- `YT_UI_MOCK=1 python3 app/server.py` then open the page and click Run to see the full animation against sample data.
