#!/usr/bin/env python3
"""Fetch a Builder Hub page as readable text (docs, academy lessons, blog).

Why this exists:
  1. Appending `.md` returns clean markdown for /docs/ pages, but for many Academy lessons the server
     answers with the full HTML app shell (~1 MB). This helper tries `.md` first, detects the HTML
     fallback, and strips it to text so raw HTML never lands in the agent's context.
  2. The site does not 404 removed pages: it REDIRECTS them to an unrelated page (e.g. the retired
     /docs/dapps/... section lands on /docs/primary-network or on an Academy lesson). The script
     compares the requested path with the final URL and prints a WARNING when they differ, so a stale
     path is noticed instead of being taught as if it were the right page.

Usage:
  fetch-doc.py <url-or-path> [--grep REGEX] [--max-chars N]

Examples:
  fetch-doc.py /docs/tooling/ai-llm/mcp-server
  fetch-doc.py /docs/cross-chain/icm-contracts/addresses --grep '0x[0-9a-fA-F]{40}'
  fetch-doc.py /docs/avalanche-l1s/add-utility/deploy-smart-contract --grep '(?i)cancun|pectra'
"""
import argparse
import html
import re
import sys
import urllib.parse
import urllib.request

BASE = "https://build.avax.network"
UA = "Mozilla/5.0 (learn-avalanche skill)"


def get(url: str) -> tuple[str, str, str]:
    """Returns (body, content_type, final_url) after following redirects."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace"), r.headers.get("content-type", ""), r.geturl()


def path_of(url: str) -> str:
    return urllib.parse.urlparse(url).path.rstrip("/")


def html_to_text(raw: str) -> str:
    # Keep code blocks readable: turn block-level closers into newlines first.
    raw = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", raw, flags=re.S)
    raw = re.sub(r"</(p|div|li|h[1-6]|pre|tr|section|article)>", "\n", raw)
    raw = re.sub(r"<br\s*/?>", "\n", raw)
    text = html.unescape(re.sub(r"<[^>]+>", "", raw))
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def looks_like_html(body: str) -> bool:
    return body.lstrip()[:15].lower().startswith(("<!doctype", "<html"))


def page_title(raw_html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", raw_html, flags=re.S | re.I)
    return html.unescape(m.group(1)).strip() if m else "(no <title>)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--grep", help="only print lines matching this regex (Python syntax, 2 lines of context)")
    ap.add_argument("--max-chars", type=int, default=12000)
    args = ap.parse_args()

    url = args.target if args.target.startswith("http") else BASE + "/" + args.target.lstrip("/")
    url = re.sub(r"\.mdx?$", "", url.rstrip("/"))
    want = path_of(url)

    body, source, title, final = None, "", "", url
    try:
        md, _, final_md = get(url + ".md")
        if not looks_like_html(md) and len(md.strip()) > 200:
            body, source, final = md, "markdown (.md endpoint)", final_md
            title = md.lstrip().splitlines()[0].lstrip("# ").strip()
    except Exception:
        pass

    if body is None:
        try:
            raw, _, final = get(url)
        except Exception as e:  # network / real 404
            print(f"ERROR: could not fetch {url}: {e}", file=sys.stderr)
            return 1
        title = page_title(raw)
        body, source = html_to_text(raw), "html stripped to text"
        # Academy pages carry the whole course sidebar first; the lesson starts at its own breadcrumb.
        m = re.search(r"Lesson \d+ of \d+", body)
        if m:
            body = body[m.start():]

    got = path_of(final)
    if got.endswith(".md"):
        got = got[:-3]
    warn = "" if got == want else f"REDIRECTED: asked {want} but the site served {got}. The path is stale; find the current one (llms-full.txt heading search or MCP docs_search)."

    if args.grep:
        lines, rx, keep = body.splitlines(), re.compile(args.grep), set()
        for i, line in enumerate(lines):
            if rx.search(line):
                keep.update(range(max(0, i - 2), min(len(lines), i + 3)))
        body = "\n".join(lines[i] for i in sorted(keep)) or "(no match)"

    print(f"<!-- source: {url} | {source} -->")
    print(f"<!-- title: {title} -->")
    if warn:
        print(f"<!-- WARNING: {warn} -->")
    print(body[: args.max_chars])
    if len(body) > args.max_chars:
        print(f"\n<!-- truncated: {len(body)} chars total; raise --max-chars or use --grep -->")
    return 2 if warn else 0


if __name__ == "__main__":
    sys.exit(main())
