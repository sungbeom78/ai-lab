# BOM_TS - AI Working Rules

> Applies to Antigravity / Codex / Claude.
> `PROJECT_CHARTER.md` takes precedence over this file.

---

## 1. Identity

You are an AI writing code for **BOM_TS** - an automated trading system.
A single line of bad code can cause real financial loss.
Choose safety over speed, discipline over freedom.

---

## 2. Work Loop (development -> commit -> push, autonomous)

When given a coding task, run this loop **without asking for approval at each step**:

```
(0) Run prior_art_check.py to obtain session token
(1) Do the work
(2) Run run_qa_quick_token.py to execute qa_quick and obtain PASS token
(3) Append to doc/change_log.md
(4) Update doc/module_index.md if public class/function changed
(5) Run glossary audit for changed files if identifiers were touched
(6) git add -> git commit -> git push
(7) Report (4 lines, see Section 6)
```

### 2-A. Step 0 is MANDATORY before touching code

```bash
python script/operation/charter/prior_art_check.py "<keyword or filename>"
```

This single command performs:
- Searches `cache/task/registry.md` for active tasks
- Searches `doc/change_log.md` (last 7 days) and archive (last 30 days)
- Reads `doc/SOURCE_OF_TRUTH.md` for relevant Frozen Zones
- Reads `doc/module_index.md` for the relevant module
- Reads `doc/README_AI_GUIDELINE.md` if exists
- Outputs a session token (saved to `cache/task/.prior_art_<timestamp>.lock`)

The token is required by both `finish-and-push.md` and the pre-commit hook
`charter-prior-art-token`. Without a fresh token, commit is blocked.

This replaces the unenforceable rules: Article 0 (5-line ack), Article 9 (registry),
GEMINI.md RULE 1 (doc-first), AGENTS.md §1-A (Prior Art Check).
**Bypassing prior_art_check.py = bypassing all four.**

### 2-B. When autonomous commit & push IS allowed
- Routine code changes / bug fixes
- Documentation updates
- Test additions
- 0-3 new identifiers (glossary clean)

### 2-C. When user approval IS required (stop and ask)
- Frozen Zone changes (Article 3)
- 10+ files changed
- New dependencies (`pyproject.toml`, `requirements.txt`)
- DB schema migrations
- New environment variables
- 4+ new identifiers (glossary)

### 2-D. When pre-commit blocks - fix it yourself, don't dump on user

| Block reason | Action |
|--------------|--------|
| Article 1 (root file) | `git mv` to `sandbox/` or `git restore --staged` |
| Article 2 (OS script) | Rewrite in Python or unstage |
| Article 3 (Frozen Zone) | STOP -> request user approval |
| Article 4 (change_log) | Append entry, `git add doc/change_log.md` |
| Article 5.A (encoding) | Re-save problem file as UTF-8 LF |
| Article 5.B (module_index) | Update `doc/module_index.md`, `git add` |
| Glossary FATAL/ERROR | Run `new-identifier-procedure.md` (Telegram notify) |

3 retries failing -> immediate user report. **Never use `git commit --no-verify`.**

---

## 3. Mandatory (auto-enforced)

| Rule | Enforcement |
|------|-------------|
| Charter Articles 1-5 | pre-commit hooks |
| Prior Art Check | `prior_art_check.py` token + `charter-prior-art-token` pre-commit hook |
| qa_quick before commit | `run_qa_quick_token.py` + `charter-qa-quick-token` pre-commit hook |
| Glossary check on changed identifiers | `audit_identifiers.py --changed-only` + `new-identifier-procedure` for genuine new words |
| change_log.md per change | pre-commit |
| module_index.md per public API change | pre-commit |
| change_log.md auto-archive | pre-commit (>500 lines or monthly) |

---

## 4. Recommended (no auto-enforcement, but expected)

| Rule | Why no enforcement |
|------|---------------------|
| GEMINI RULE 2 (minimum scope) | Subjective |
| GEMINI RULE 9 (Korean responses) | Style preference |
| GEMINI RULE 10 (autonomous execution) | Policy, not gate |
| AGENTS §9-A (regression tests) | Scope-dependent |
| AGENTS §6-A (TRADING_ENV check) | Runtime check, not commit-time |

These are documented but the AI is trusted to apply judgment.

---

## 5. Glossary - scanner is the source of truth

Do not guess whether an identifier is valid. Run the scanner.

```bash
python script/operation/audit_identifiers.py --changed-only
```

The scanner supports targeted checks such as:

```bash
python script/operation/audit_identifiers.py --files src/path/file.py
python script/operation/audit_identifiers.py --dir src/execution
python script/operation/audit_identifiers.py --tables PG_DSN table_name
python script/operation/audit_identifiers.py --db-env PG_DSN
```

The scanner writes reports under:

```text
tmp/audit/audit_identifiers/
```

### 5-A. If scanner reports PASS

Proceed.

### 5-B. If scanner reports WARN with unregistered words

Inspect the generated report and classify each unregistered word:

1. Existing legacy word unrelated to this task

   * Do not rename casually.
   * Mention as legacy warning if relevant.

2. Variant of registered base word

   * Use the registered base form.
   * Example: `running` -> `run`, `cancelling` -> `cancel`.

3. Synonym of registered word

   * Use the registered synonym.
   * Example: `transmit` -> `send`, `abort` -> `cancel`.

4. Genuinely new domain word

   * Run `new-identifier-procedure.md`.
   * Send Telegram notification through `notify_new_identifier.py`.
   * Wait for user approval before registering.

### 5-C. If scanner reports ERROR/FATAL

Fix before proceeding. Do not commit.

---

## 6. Completion report format (replaces AGENTS §13-A checklist)

After successful commit & push, output this 4-line summary - nothing more:

```
[Done]
- Files: N changed
- qa_quick: PASS
- commit: <short_hash> <first line of message>
- push: ok (origin/<branch>)
```

Long checklists are forbidden. pre-commit passing = charter compliance.

---

## 7. When user is frustrated

- No excuses
- No new rule proposals
- Follow the charter
- If in doubt, read the charter; do not ask new questions

---

## 8. Tool-specific

### Antigravity
- "Always run" auto-approve: tier-A only
- Workflow `// turbo-all` annotations: respected
- Knowledge Items < PROJECT_CHARTER

### Codex / OMX
- AGENTS.md applies; PROJECT_CHARTER overrides on conflict

### Claude (chat mode)
- Design / planning focus; same charter applies if generating files
