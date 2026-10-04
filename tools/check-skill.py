#!/usr/bin/env python3
"""Repository quality gate for the learn-avalanche skill. Standard library only.

    python3 tools/check-skill.py

Checks (exit code 1 if any fails):
  1. SKILL.md frontmatter: name matches the folder, description present and <= 1024 chars.
  2. SKILL.md size budget (it is loaded in full on every invocation; keep it small and fast).
  3. Every skill-internal file reference (`references/...`, `scripts/...`, `assets/...`,
     `answer-keys/...`, `maintainers/...`) resolves from the skill root, and no bare
     sibling names (`curriculum.md`) are used.
  4. The skill never points at repo-only docs other than the verification checklist.
  5. Relative links in the top-level Markdown files resolve.
  6. Every Python file compiles.
  7. No absolute personal paths (/home/<user>, /Users/<user>) in tracked text files.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(ROOT, ".claude", "skills", "learn-avalanche")
SKILL_MD_BUDGET = 20_000  # bytes
errors = []


def fail(msg):
    errors.append(msg)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def tracked():
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        return [l for l in out.split("\n") if l and os.path.isfile(os.path.join(ROOT, l))]
    except Exception:
        found = []
        for d, _, fs in os.walk(ROOT):
            if ".git" in d.split(os.sep):
                continue
            found += [os.path.relpath(os.path.join(d, f), ROOT) for f in fs]
        return found


# 1 + 2 ------------------------------------------------------------------
skill_md = os.path.join(SKILL, "SKILL.md")
text = read(skill_md)
m = re.match(r"---\n(.*?)\n---\n", text, re.S)
if not m:
    fail("SKILL.md: missing frontmatter")
else:
    fm = m.group(1)
    name = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or name.group(1) != os.path.basename(SKILL):
        fail(f"SKILL.md: name must equal the folder name ({os.path.basename(SKILL)})")
    if not desc:
        fail("SKILL.md: missing description")
    elif len(desc.group(1)) > 1024:
        fail(f"SKILL.md: description is {len(desc.group(1))} chars (max 1024)")
size = len(text.encode("utf-8"))
if size > SKILL_MD_BUDGET:
    fail(f"SKILL.md: {size} bytes exceeds the {SKILL_MD_BUDGET} byte budget (move detail into references/)")

# 3 + 4 ------------------------------------------------------------------
REF = re.compile(r"`((?:references|scripts|assets|answer-keys|maintainers)/[A-Za-z0-9_./\-]+)`")
BARE = re.compile(r"`(?:curriculum|live-facts|communities|placement|teaching-method|discipline|remix-guide|roadmap-next)\.md`")
DOCS = re.compile(r"(?<![/\w])docs/[\w.\-]+\.md")
skill_docs = []
for d, _, fs in os.walk(SKILL):
    if "answer-keys" in d or "forge-suite" in d:
        continue
    skill_docs += [os.path.join(d, f) for f in fs if f.endswith(".md")]
for f in sorted(skill_docs):
    rel = os.path.relpath(f, SKILL)
    s = read(f)
    for ref in REF.findall(s):
        ref = ref.rstrip("/.")
        if "*" in ref or "<" in ref:
            continue
        if not os.path.exists(os.path.join(SKILL, ref)):
            fail(f"{rel}: reference `{ref}` does not resolve from the skill root")
    for b in BARE.findall(s):
        fail(f"{rel}: bare reference {b} (use references/<name>.md)")
    for dref in DOCS.findall(s):
        if dref != "docs/verification-checklist.md":
            fail(f"{rel}: points at repo-only doc {dref} (not installed with the skill)")

# 5 ----------------------------------------------------------------------
LINK = re.compile(r"\]\(([^)\s]+)\)")
for top in ("README.md", "CONTRIBUTING.md", "SECURITY.md", "CODE_OF_CONDUCT.md", "CHANGELOG.md"):
    p = os.path.join(ROOT, top)
    if not os.path.exists(p):
        continue
    for target in LINK.findall(read(p)):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        path = target.split("#")[0]
        if path and not os.path.exists(os.path.join(ROOT, path)):
            fail(f"{top}: broken link ({target})")
for d, _, fs in os.walk(os.path.join(ROOT, "docs")):
    for f in fs:
        if not f.endswith(".md"):
            continue
        p = os.path.join(d, f)
        for target in LINK.findall(read(p)):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = target.split("#")[0]
            if path and not os.path.exists(os.path.normpath(os.path.join(d, path))):
                fail(f"{os.path.relpath(p, ROOT)}: broken link ({target})")

# 6 ----------------------------------------------------------------------
files = tracked()
for rel in files:
    if rel.endswith(".py"):
        try:
            compile(read(os.path.join(ROOT, rel)), rel, "exec")
        except SyntaxError as e:
            fail(f"{rel}: does not compile ({e.msg}, line {e.lineno})")

# 7 ----------------------------------------------------------------------
PERSONAL = re.compile(r"/(?:home|Users)/[a-z][\w.\-]*/")
for rel in files:
    if rel.endswith((".png", ".jpg", ".svg", ".pyc")):
        continue
    try:
        s = read(os.path.join(ROOT, rel))
    except (UnicodeDecodeError, OSError):
        continue
    for hit in PERSONAL.findall(s):
        if hit not in ("/home/user/",):
            fail(f"{rel}: personal absolute path {hit}")
            break

if errors:
    print("FAIL")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"OK: skill checks passed (SKILL.md {size} bytes, {len(skill_docs)} skill docs, {len(files)} tracked files)")
