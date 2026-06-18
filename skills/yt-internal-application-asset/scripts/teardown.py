#!/usr/bin/env python3
"""
teardown.py

Step 5 link and landing-page teardown for Worker 2.

For each link, this script runs the free local-first fallback chain so Claude
has both the copy and the visual flow to analyze:

Tier 1, default and free:
- Clean page text via Jina Reader, by prefixing the URL with https://r.jina.ai/
- Full-page screenshot via local headless Playwright chromium, full_page=True

Tier 3, hosted fallback:
- If the local browser is blocked or hits a captcha, and a hosted screenshot
  API key is present, capture through that hosted API. Only PUBLIC URLs are ever
  sent to a hosted service.

Tier 2, the interactive multi-step funnel walk through Playwright MCP, is not in
this script. That escalation is driven by Claude through the @playwright/mcp
server, and only for links flagged interactive. See the SKILL.md.

A link that cannot be reached by any available tier is marked unreachable and
the run continues. One dead link never fails the whole teardown.

Usage:
    python3 teardown.py --links links.json --outdir shots/ --out teardown.json
    python3 teardown.py --url "https://example.com" --outdir shots/

links.json is a JSON array of objects each with at least a "url" key, which is
the shape produced by extract.py under the "links" field.

Environment:
    SCREENSHOTONE_API_KEY   enables the Tier 3 hosted fallback (free tier ok)
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

PRIVATE_HOST_RE = re.compile(
    r"^(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|169\.254\.|\[?::1\]?)",
    re.IGNORECASE,
)
# Words that usually signal a block wall or captcha on a fetched page.
BLOCK_SIGNALS = ("captcha", "are you a robot", "access denied", "verify you are human",
                 "cloudflare", "request blocked", "enable javascript and cookies")


def log(msg):
    print(f"[teardown] {msg}", file=sys.stderr, flush=True)


def trust_system_ca():
    """Trust the active system CA bundle (works behind a TLS proxy)."""
    for cand in (
        os.environ.get("YT_PIPELINE_CA_BUNDLE"),
        os.environ.get("SSL_CERT_FILE"),
        os.environ.get("REQUESTS_CA_BUNDLE"),
        "/etc/ssl/certs/ca-certificates.crt",
    ):
        if cand and os.path.exists(cand):
            os.environ.setdefault("SSL_CERT_FILE", cand)
            try:
                import certifi

                certifi.where = lambda c=cand: c
            except Exception:  # noqa: BLE001
                pass
            return


def is_public_url(url):
    """Return True only for a public http or https URL safe to send to a host."""
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:  # noqa: BLE001
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    host = parsed.hostname or ""
    if PRIVATE_HOST_RE.match(host):
        return False
    if "." not in host:
        return False
    return True


def slugify(url):
    """Make a filesystem-safe stem from a URL."""
    stem = re.sub(r"[^a-zA-Z0-9]+", "_", url)[:80].strip("_")
    return stem or "link"


def jina_reader_text(url):
    """Tier 1 text. Fetch clean page text through Jina Reader."""
    reader_url = "https://r.jina.ai/" + url
    try:
        req = urllib.request.Request(
            reader_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; yt-reference-pipeline)"},
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        return text.strip() or None
    except Exception as exc:  # noqa: BLE001
        log(f"jina reader failed for {url}: {str(exc)[:120]}")
        return None


def looks_blocked(text):
    if not text:
        return False
    low = text[:4000].lower()
    return any(sig in low for sig in BLOCK_SIGNALS)


def playwright_screenshot(url, path):
    """Tier 1 visual. Full-page screenshot via local headless chromium.

    Returns one of: "ok", "blocked", "error".
    """
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # noqa: BLE001
        log(f"playwright not importable: {str(exc)[:120]}")
        return "error"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_context(
                viewport={"width": 1440, "height": 900},
                user_agent="Mozilla/5.0 (compatible; yt-reference-pipeline)",
            ).new_page()
            page.goto(url, wait_until="networkidle", timeout=45000)
            time.sleep(1.5)  # let late content settle
            body_text = (page.inner_text("body") or "")[:4000]
            page.screenshot(path=path, full_page=True)
            browser.close()
        if looks_blocked(body_text):
            return "blocked"
        return "ok"
    except Exception as exc:  # noqa: BLE001
        msg = str(exc).lower()
        log(f"playwright screenshot failed for {url}: {str(exc)[:140]}")
        if "executable doesn't exist" in msg or "playwright install" in msg:
            log("chromium is not installed. Run: python3 -m playwright install chromium")
        return "error"


def screenshotone_fallback(url, path):
    """Tier 3 visual. Hosted screenshot API, public URLs only."""
    api_key = os.environ.get("SCREENSHOTONE_API_KEY")
    if not api_key:
        return False
    if not is_public_url(url):
        log(f"refusing to send non-public url to hosted API: {url}")
        return False
    params = urllib.parse.urlencode(
        {
            "access_key": api_key,
            "url": url,
            "full_page": "true",
            "format": "png",
            "block_cookie_banners": "true",
            "block_ads": "true",
        }
    )
    api_url = "https://api.screenshotone.com/take?" + params
    try:
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        if data:
            with open(path, "wb") as handle:
                handle.write(data)
            return True
    except Exception as exc:  # noqa: BLE001
        log(f"screenshotone fallback failed for {url}: {str(exc)[:120]}")
    return False


def teardown_one(url, outdir):
    """Run the fallback chain for a single url and return a record."""
    record = {
        "url": url,
        "public": is_public_url(url),
        "jina_ok": False,
        "jina_text_path": None,
        "screenshot_ok": False,
        "screenshot_path": None,
        "screenshot_method": None,
        "reachable": False,
        "notes": [],
    }

    # Tier 1 text.
    text = jina_reader_text(url)
    if text:
        text_path = os.path.join(outdir, slugify(url) + ".txt")
        with open(text_path, "w", encoding="utf-8") as handle:
            handle.write(text)
        record["jina_ok"] = True
        record["jina_text_path"] = text_path
        if looks_blocked(text):
            record["notes"].append("jina text shows a possible block or captcha wall")

    # Tier 1 visual.
    shot_path = os.path.join(outdir, slugify(url) + ".png")
    status = playwright_screenshot(url, shot_path)
    if status == "ok":
        record["screenshot_ok"] = True
        record["screenshot_path"] = shot_path
        record["screenshot_method"] = "playwright-local"
    else:
        if status == "blocked":
            record["notes"].append("local browser hit a block or captcha, trying hosted fallback")
        # Tier 3 visual.
        if screenshotone_fallback(url, shot_path):
            record["screenshot_ok"] = True
            record["screenshot_path"] = shot_path
            record["screenshot_method"] = "screenshotone-hosted"
        else:
            record["notes"].append("no screenshot captured by any tier")

    record["reachable"] = record["jina_ok"] or record["screenshot_ok"]
    if not record["reachable"]:
        record["notes"].append("unreachable by every tier, marked unreachable and skipped")
    return record


def load_links(args):
    urls = []
    if args.url:
        urls.append(args.url)
    if args.links and os.path.exists(args.links):
        with open(args.links, encoding="utf-8") as handle:
            data = json.load(handle)
        for item in data:
            if isinstance(item, str):
                urls.append(item)
            elif isinstance(item, dict) and item.get("url"):
                urls.append(item["url"])
    # De-duplicate while keeping order.
    seen = set()
    ordered = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            ordered.append(u)
    return ordered


def main():
    parser = argparse.ArgumentParser(description="Step 5 link teardown fallback chain.")
    parser.add_argument("--links", help="JSON file of links (from extract.py)")
    parser.add_argument("--url", help="A single URL to tear down")
    parser.add_argument("--outdir", default="teardown_assets", help="Output directory")
    parser.add_argument("--out", help="Write the teardown JSON summary to this path")
    args = parser.parse_args()

    trust_system_ca()
    os.makedirs(args.outdir, exist_ok=True)
    urls = load_links(args)
    if not urls:
        log("no links provided")
        sys.exit(1)

    results = []
    for url in urls:
        log(f"tearing down {url}")
        results.append(teardown_one(url, args.outdir))

    summary = {
        "total": len(results),
        "reachable": sum(1 for r in results if r["reachable"]),
        "unreachable": sum(1 for r in results if not r["reachable"]),
        "results": results,
    }
    text = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text)
        log(f"summary written to {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
