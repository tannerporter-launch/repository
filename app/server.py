#!/usr/bin/env python3
"""
server.py

Local web UI for the yt-reference-pipeline. Paste a YouTube link, and the app
drives the pipeline skill through the Claude CLI, streaming live progress back
to the browser. Nothing is reimplemented here. The UI is a thin, reliable
wrapper over the skills and the Notion MCP that already do the work.

Run:
    python3 app/server.py
    then open http://127.0.0.1:8765

Environment:
    YT_UI_PORT          port to serve on, default 8765
    YT_UI_CLAUDE        claude binary, default "claude"
    YT_UI_CLAUDE_ARGS   extra args for the claude call, default
                        "--dangerously-skip-permissions"
                        (needed so a one-click run does not stop for prompts)
    YT_UI_MOCK          set to 1 to emit a scripted demo stream without calling
                        claude or the network, for testing the UI

No third-party packages. Standard library only.
"""

import json
import os
import queue
import re
import shlex
import subprocess
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("YT_UI_PORT", "8765"))
CLAUDE = os.environ.get("YT_UI_CLAUDE", "claude")
CLAUDE_ARGS = os.environ.get("YT_UI_CLAUDE_ARGS", "--dangerously-skip-permissions")
MOCK = os.environ.get("YT_UI_MOCK") == "1"

YT_RE = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com/(watch\?v=|shorts/|live/)|youtu\.be/)[\w-]{6,}",
    re.IGNORECASE,
)
NOTION_URL_RE = re.compile(r"https://(?:www\.)?(?:notion\.so|app\.notion\.com)/[^\s)\"']+")

# Active jobs, keyed by job id. Each value is an event queue.
JOBS = {}

PROMPT_TEMPLATE = (
    "Use the yt-reference-pipeline skill to process this YouTube URL end to end. "
    "The only input is the URL. Run Worker 1 (yt-external-example-asset) to build "
    "the External Example asset in the Reference Assets Notion database, then "
    "Worker 2 (yt-internal-application-asset) to build the linked Internal "
    "Application asset, then the Actionability Loop per the skill. When finished, "
    "print the Notion page URL of each asset on its own line, labeled EXTERNAL: "
    "and INTERNAL: . URL: {url}"
)


def sse(event, data):
    """Format one Server-Sent Event frame."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n".encode("utf-8")


def classify_step(tool_name, payload_text):
    """Map a tool call to a UI step key, or None if it does not map."""
    low = payload_text.lower()
    if "extract.py" in low:
        return "extract"
    if "teardown.py" in low:
        return "analyze"
    if "notion-create-pages" in (tool_name or "").lower() or "create-pages" in low:
        if "internal application" in low:
            return "int"
        if "external example" in low:
            return "ext"
    return None


def emit_pages_from_text(text, q, state):
    """Find Notion page URLs in any text and push page events, classified."""
    for url in NOTION_URL_RE.findall(text):
        url = url.rstrip(".,);")
        # Skip the database container url, we only want asset pages.
        if url in state["pages_seen"]:
            continue
        kind = None
        window = text.lower()
        # Classify by nearby label or by the explicit EXTERNAL/INTERNAL markers.
        idx = text.find(url)
        near = text[max(0, idx - 120): idx + 40].lower()
        if "internal" in near or "int |" in near:
            kind = "internal"
        elif "external" in near or "ext |" in near:
            kind = "external"
        elif "internal application" in window and "external example" not in window:
            kind = "internal"
        else:
            kind = "external" if not state["ext_done"] else "internal"
        state["pages_seen"].add(url)
        if kind == "external":
            state["ext_done"] = True
        q.put(sse("page", {"kind": kind, "url": url, "title": ""}))


def handle_stream_line(line, q, state):
    """Parse one claude stream-json line and translate it to UI events."""
    line = line.strip()
    if not line:
        return
    try:
        obj = json.loads(line)
    except Exception:  # noqa: BLE001
        q.put(sse("log", {"line": line[:500], "cls": "muted"}))
        return

    otype = obj.get("type")
    if otype == "system":
        if obj.get("subtype") == "init":
            q.put(sse("log", {"line": "Session started.", "cls": "muted"}))
        return

    if otype == "assistant":
        for block in obj.get("message", {}).get("content", []):
            btype = block.get("type")
            if btype == "text":
                text = block.get("text", "").strip()
                if text:
                    q.put(sse("log", {"line": text, "cls": ""}))
                    emit_pages_from_text(text, q, state)
            elif btype == "tool_use":
                name = block.get("name", "")
                payload_text = name + " " + json.dumps(block.get("input", {}))[:1500]
                step = classify_step(name, payload_text)
                if step:
                    # Mark any earlier active step done, then activate this one.
                    advance_steps(step, q, state)
                friendly = friendly_tool(name, block.get("input", {}))
                if friendly:
                    q.put(sse("log", {"line": friendly, "cls": "muted"}))
        return

    if otype == "user":
        # Tool results come back as user messages, scan for Notion urls.
        for block in obj.get("message", {}).get("content", []):
            if block.get("type") == "tool_result":
                content = block.get("content", "")
                if isinstance(content, list):
                    content = " ".join(
                        c.get("text", "") for c in content if isinstance(c, dict)
                    )
                emit_pages_from_text(str(content), q, state)
        return

    if otype == "result":
        text = obj.get("result", "") or ""
        emit_pages_from_text(text, q, state)
        is_err = obj.get("is_error") or obj.get("subtype") not in (None, "success")
        # Mark remaining steps done on success.
        if not is_err:
            for k in STEP_ORDER:
                if state["step_state"].get(k) != "done":
                    q.put(sse("step", {"key": k, "state": "done"}))
                    state["step_state"][k] = "done"
        q.put(sse("done", {"ok": not is_err, "error": text[:400] if is_err else ""}))
        state["finished"] = True


STEP_ORDER = ["extract", "clean", "ext", "analyze", "int"]


def advance_steps(target, q, state):
    """Activate target step and mark all earlier steps done."""
    ti = STEP_ORDER.index(target)
    for i, k in enumerate(STEP_ORDER):
        if i < ti and state["step_state"].get(k) != "done":
            q.put(sse("step", {"key": k, "state": "done"}))
            state["step_state"][k] = "done"
    if state["step_state"].get(target) != "done":
        q.put(sse("step", {"key": target, "state": "active"}))
        state["step_state"][target] = "active"
    # The clean step has no tool of its own, so activate it once extraction runs.
    if target == "ext" and state["step_state"].get("clean") != "done":
        q.put(sse("step", {"key": "clean", "state": "done"}))
        state["step_state"]["clean"] = "done"


def friendly_tool(name, tool_input):
    """A short human label for a tool call, or empty to hide it."""
    low = name.lower()
    blob = json.dumps(tool_input).lower()
    if "extract.py" in blob:
        return "Extracting transcript, title, and description with yt-dlp."
    if "teardown.py" in blob:
        return "Tearing down the links, text and screenshots."
    if "create-pages" in low:
        if "internal application" in blob:
            return "Writing the Internal Application asset to Notion."
        if "external example" in blob:
            return "Writing the External Example asset to Notion."
        return "Writing a Notion page."
    if "playwright" in low:
        return "Capturing a page screenshot."
    if low.startswith("mcp__notion"):
        return None
    if name == "Bash":
        return None
    return None


def build_command(url):
    """Build the claude CLI argument list for a run."""
    prompt = PROMPT_TEMPLATE.format(url=url)
    args = [CLAUDE, "-p", prompt, "--output-format", "stream-json", "--verbose"]
    args += shlex.split(CLAUDE_ARGS)
    return args


def mock_stream():
    """Scripted stream-json lines for testing without claude or network."""
    ext = "https://app.notion.com/p/383c94537b3b81669abddb2205e76c7e"
    intl = "https://app.notion.com/p/383c94537b3b810c8afbfac5cbb9590a"
    yield {"type": "system", "subtype": "init"}
    yield {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": "python3 skills/yt-external-example-asset/scripts/extract.py URL"}}]}}
    yield {"type": "assistant", "message": {"content": [
        {"type": "text", "text": "Transcript extracted. Cleaning with the reused formatter prompt."}]}}
    yield {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "mcp__Notion__notion-create-pages",
         "input": {"pages": [{"properties": {"Asset Type": "External Example"}}]}}]}}
    yield {"type": "user", "message": {"content": [
        {"type": "tool_result", "content": "Created External Example page " + ext}]}}
    yield {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": "python3 skills/yt-internal-application-asset/scripts/teardown.py"}}]}}
    yield {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "mcp__Notion__notion-create-pages",
         "input": {"pages": [{"properties": {"Asset Type": "Internal Application"}}]}}]}}
    yield {"type": "user", "message": {"content": [
        {"type": "tool_result", "content": "Created Internal Application page " + intl}]}}
    yield {"type": "result", "subtype": "success", "is_error": False,
           "result": "Done. EXTERNAL: " + ext + " INTERNAL: " + intl}


def run_job(url, q):
    """Run the pipeline for one url, pushing SSE events onto q."""
    state = {"step_state": {}, "pages_seen": set(), "ext_done": False, "finished": False}
    try:
        if MOCK:
            import time

            for obj in mock_stream():
                handle_stream_line(json.dumps(obj), q, state)
                time.sleep(0.4)
        else:
            cmd = build_command(url)
            q.put(sse("log", {"line": "Launching: " + " ".join(shlex.quote(c) for c in cmd[:3]) + " ...", "cls": "muted"}))
            proc = subprocess.Popen(
                cmd, cwd=os.path.dirname(HERE), stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, bufsize=1,
            )
            for line in proc.stdout:
                handle_stream_line(line, q, state)
            proc.wait()
            if not state["finished"]:
                ok = proc.returncode == 0
                q.put(sse("done", {"ok": ok, "error": "" if ok else f"claude exited with code {proc.returncode}"}))
    except FileNotFoundError:
        q.put(sse("done", {"ok": False, "error": f"Could not find the claude binary '{CLAUDE}'. Install Claude Code or set YT_UI_CLAUDE."}))
    except Exception as exc:  # noqa: BLE001
        q.put(sse("done", {"ok": False, "error": str(exc)[:300]}))
    finally:
        q.put(None)  # sentinel, closes the SSE stream


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep the console quiet
        pass

    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as fh:
                self._send(200, fh.read(), "text/html; charset=utf-8")
            return
        if parsed.path == "/events":
            job = parse_qs(parsed.query).get("job", [""])[0]
            q = JOBS.get(job)
            if not q:
                self._send(404, b"unknown job")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            try:
                while True:
                    item = q.get()
                    if item is None:
                        break
                    self.wfile.write(item)
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                JOBS.pop(job, None)
            return
        self._send(404, b"not found")

    def do_POST(self):
        if urlparse(self.path).path != "/run":
            self._send(404, b"not found")
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            body = json.loads(self.rfile.read(length) or "{}")
        except Exception:  # noqa: BLE001
            body = {}
        url = (body.get("url") or "").strip()
        if not YT_RE.match(url):
            self._send(200, json.dumps({"error": "That does not look like a YouTube link."}).encode(), "application/json")
            return
        job_id = uuid.uuid4().hex
        q = queue.Queue()
        JOBS[job_id] = q
        threading.Thread(target=run_job, args=(url, q), daemon=True).start()
        self._send(200, json.dumps({"job_id": job_id}).encode(), "application/json")


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    mode = "MOCK" if MOCK else "live"
    print(f"YouTube to Reference Assets UI ({mode}) running at http://127.0.0.1:{PORT}")
    print("Press Ctrl C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
