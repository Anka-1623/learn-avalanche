# Contributing

The most valuable contribution: **actually try the skill and write down what happened.** What remains unverified in the beta is listed openly in the [README](README.md#verification-status-beta) and in the [verification checklist](docs/verification-checklist.md) (written in Turkish).

By taking part you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## Try it and report

1. Install with `npx skills add Anka-1623/learn-avalanche`, then start the skill in your agent (see the [README](README.md#install)).
2. Pick one item from the [verification checklist](docs/verification-checklist.md) and go through it to the end.
3. Write it up with the **Test result** issue form: which agent, which step, what you expected, what happened. If a UI label is different, include its exact text.

Found something plainly wrong (the skill wrote your code, stated a wrong fact, broke its memory file)? Use the **Bug report** form.

When sharing screenshots, make sure **nothing but your wallet address** is visible. Recovery phrases and private keys are never shared.

## Proposing changes (PRs)

- Keep them small and verifiable. Fixes like "I tried this in Remix and the label said X" are ideal.
- **The golden rule is not broken:** never put the solution to a student's exercise anywhere in the skill as agent output. Solutions live only under `answer-keys/`.
- Run the checks before opening a PR:
  ```bash
  python3 tools/check-skill.py      # frontmatter, internal paths, links, compile, no personal paths
  python3 tools/test-memory.py      # unit tests for scripts/memory.py
  ```
- If you touched `answer-keys/` or the acceptance tables: `bash .claude/skills/learn-avalanche/maintainers/forge-suite/run.sh` must be fully green (needs Foundry).
- If you changed an Avalanche-specific fact, update the date and source in `references/live-facts.md`. Don't add a fact you cannot source.
- For ecosystem programs (grants, competitions), **don't write** status, amounts or dates; the skill doesn't state them, it points to the official page.
- No flow that asks for mainnet, real money or keys will be added.
- If you change the images, edit `tools/make-art.py` and regenerate the outputs; hand-edited PNG/SVG files are not accepted. No logo or character of another brand may be used.
- `SKILL.md` is loaded in full on every invocation, so it has a size budget (enforced by `tools/check-skill.py`). Put detail in `references/` and read it only where it is needed.

## Adding a community

Add one row to `.claude/skills/learn-avalanche/references/communities.md`. Don't invent unverified links or assignments.

## Language

The skill's instructions and most of `docs/` are currently in Turkish, and **that is intentional: no per-language copies are needed.** The agent reads the instructions once and replies in whatever language the learner writes (any language, translated at runtime). Please do not add translated variants of the instructions, question lists or example voices; they only create maintenance drift. Improvements to the teaching rules go into the single source text. Public-facing files at the repository root (README, CONTRIBUTING, SECURITY, CHANGELOG) are in English.

## Releasing

For maintainers, before a version tag or when changing repository visibility:

1. `python3 tools/check-skill.py` and `python3 tools/test-memory.py` pass; `verify-facts.py` is all OK; the forge suite is green if answer keys changed.
2. The [verification checklist](docs/verification-checklist.md) was run by a human for anything the release claims; the README status table matches reality.
3. `CHANGELOG.md` has the entry; the version is bumped in `SKILL.md` (frontmatter description and header) and in the README badge.
4. **Identities:** `git log --format='%an <%ae>'` shows only addresses you are happy to publish (use the GitHub no-reply address). Full history becomes visible when a repository is made public.
5. A secret scan of the tree and the whole history is clean (keys, tokens, mnemonics, personal paths).
6. Repository page: description, topics, social preview (`docs/img/social-preview.png`, uploaded in Settings → General), Issues on, *Private vulnerability reporting* on.
7. After going public, from a clean folder: `npx skills add Anka-1623/learn-avalanche --list`, then install and start the skill once; record the result in the README status table.
8. Tag: `git tag v<version> && git push --tags`, and create the GitHub release.
