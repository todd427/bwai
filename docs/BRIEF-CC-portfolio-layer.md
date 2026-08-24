# <span style="color:#1F3A5F">BWAI — CC Brief: Portfolio Layer + CLI Refresh</span>

<span style="color:#7F8C8D">**Owner:** Todd McCaffrey · **Date:** 2026-08-24 · **Status:** Ready for implementation</span>
<span style="color:#7F8C8D">**Executor:** Claude Code · **Repo:** bwai · **Branch:** work on `master` or a `portfolio-layer` feature branch, Todd's call at run time</span>
<span style="color:#7F8C8D">**Companion docs:** README.md · docs/WEEK-0-LAUNCH-PAD.md · docs/POSITIONING-vs-MIT.md</span>

---

## <span style="color:#16A085">1. Why (strategic frame)</span>

Claude Academy (relaunched by Anthropic 2026-08-20, academy.claude.com) now covers BWAI's tool-instruction layer for free: Platform 101, Claude Code 101, the 9-hour API course, MCP, agent skills, subagents. BWAI's response is not to compete on instruction but to become the **practicum**: cohort, continuous build, and a **portfolio** — the closing artifact Academy structurally cannot produce.

Positioning line: **Academy gives you a badge; BWAI gives you a URL.**

The portfolio's differentiator is the **process record**. In 2026, working code proves nothing — anyone can generate it. What can't be generated is evidence of *directed* work: decisions, pushbacks, failure analysis. Every project therefore carries an **AI Collaboration Statement**, and the portfolio compiles projects + process records into one deployed site. The same statement doubles as the academic-integrity mechanism for the ATU NFQ L9 delivery.

This brief covers the **code work only**. Course content (Weeks 1–6 sessions) is authored separately and is out of scope here.

---

## <span style="color:#16A085">2. Work packages</span>

### <span style="color:#2980B9">WP1 — README template upgrade (`bwai new-project`)</span>

The README generated in `cli.py` `new_project()` currently has: What This Does / What I Learned / How To Run / Live Demo. Replace with a structured template the portfolio generator (WP2) can parse:

```markdown
# {name}

**Building With AI** — Week {week}: {theme}
_{project_type}_

## Problem
_What problem does this solve? Who has it?_

## Approach
_How you solved it. Key design decisions._

## AI Collaboration Statement
_What the AI did. What you did. What you rejected, and why.
This is the part a reader can't fake and a hiring manager can't ignore._

## What Broke
_What went wrong, what you learned fixing it._

## How To Run
(keep existing content)

## Live Demo
**URL:** _Railway deployment URL_

<!-- bwai:meta
week: {week}
type: {project_type}
status: draft
-->
```

- The `bwai:meta` HTML comment block is the machine-readable anchor for WP2. Keep it simple `key: value`, parse with a few lines of string handling — no YAML dependency.
- Section headings are the parse contract: WP2 extracts `## Problem`, `## AI Collaboration Statement`, and the Live Demo URL by heading. Don't rename them later without updating both sides.

### <span style="color:#2980B9">WP2 — `bwai portfolio` command (new)</span>

New command in `cli.py` (or split into `portfolio.py` if `cli.py` gets unwieldy — it's already ~700 lines, prefer the split).

**Behaviour:**

```bash
bwai portfolio build     # generate static site into portfolio/
bwai portfolio serve     # local preview (python -m http.server on portfolio/)
bwai portfolio deploy    # publish to GitHub Pages
```

- **build:** walk `projects/week*/*/README.md`, parse the template sections + meta block, emit a single-page static site: header (student name from git config), one card per project — name, week, problem summary, live-demo link, GitHub link, collapsible AI Collaboration Statement. Ordered by week. Projects missing a Live Demo URL render with a visible "not deployed" tag rather than being skipped — honesty is part of the pedagogy.
- **Static output:** hand-rolled HTML + one embedded CSS file. **No framework, no build chain, no npm.** Students must be able to read the generated source. A single Python string template (or `string.Template`) is fine; Jinja2 is already transitively available via FastAPI if genuinely needed, but prefer zero new deps.
- **deploy:** push `portfolio/` to a `gh-pages` branch of the student's fork (`git subtree` or a temp-branch dance — pick the least fragile, document the choice in the code). Print the resulting `https://{user}.github.io/{repo}/` URL. Handle the not-a-fork / no-remote case with the same friendly-hint style `submit` uses.
- Rich console output consistent with the rest of the CLI (Panels, check marks).

**Non-goals for WP2:** no themes, no config file, no per-student customisation. One good default. Resist scope.

### <span style="color:#2980B9">WP3 — Mechanical rot fixes</span>

1. **Model string.** `claude-sonnet-4-20250514` is hardcoded in `check_env()` and as the `api-test` default, and appears in docs/WEEK-0-LAUNCH-PAD.md Step 5. Centralise as `DEFAULT_MODEL` in one place, overridable via `BWAI_MODEL` env var. Set it to the current Sonnet alias — `claude-sonnet-4-6` as of Aug 2026, but **verify against the live model list at implementation time**, don't trust this brief's snapshot. Update the Week 0 doc to match, and add one sentence there noting that model strings age — it's a teaching moment, not just a fix.
2. **Token counting is wrong, not just stale.** `token-count` uses tiktoken `cl100k_base` — an OpenAI tokenizer. Claude tokenises differently; we are teaching students incorrect numbers. Replace with the Anthropic `count_tokens` API (`client.messages.count_tokens`), falling back to a clearly-labelled character-based estimate (chars/3.5, printed as "rough estimate — offline") when no API key is present. Drop the tiktoken dependency.
3. **Hardcoded pricing.** The `$0.000003` input-price in `token-count` goes into a named constant with a "prices change — check the pricing page" note in the output, or drop the cost row entirely. Prefer dropping it.
4. **`[COURSE_ORG]` placeholder** in docs/WEEK-0-LAUNCH-PAD.md — replace with the real repo URL (todd427/bwai unless Todd says otherwise at run time).
5. **`verify.py`** — sync its model string and package list with the above; confirm it still passes in a fresh venv.
6. Remove `tools/bwai.egg-info/` and `__pycache__/` from the repo; add both to `.gitignore`.

### <span style="color:#2980B9">WP4 — Tests</span>

- Unit tests for the README meta-block parser and section extractor (the WP2 parse contract) — these are the fragile bits.
- A test that scaffolds a project into a tmpdir via the click test runner, then runs `portfolio build` over it and asserts the card appears in the output HTML.
- No live-API tests; mock the Anthropic client for `token-count`.

---

## <span style="color:#16A085">3. Acceptance criteria</span>

- [ ] `bwai new-project demo --week 3` produces the new README template with the meta block
- [ ] `bwai portfolio build` over ≥2 scaffolded projects yields one HTML page, cards ordered by week, undeployed projects visibly tagged
- [ ] `bwai portfolio deploy` publishes to gh-pages and prints the Pages URL (manual verification on a fork)
- [ ] No `claude-sonnet-4-20250514` string anywhere in the repo
- [ ] `bwai token-count` returns API-accurate counts with a key, labelled estimate without one; tiktoken gone from requirements
- [ ] `pytest` green; fresh-venv `pip install -e tools/` + `verify.py` passes
- [ ] egg-info and pycache gone from git history's tip (no filter-branch needed, just rm + ignore)

## <span style="color:#16A085">4. Out of scope</span>

Weeks 1–6 session content · Anseo API changes · demo-day process design · Codespaces devcontainer changes beyond the model string · any multi-theme portfolio styling.

---

<span style="color:#7F8C8D">*Written by Claude (chat) from the 2026-08-24 BWAI review session; context in Mnemos under "Claude – BWAI update review & portfolio layer – 2026-08-24".*</span>
