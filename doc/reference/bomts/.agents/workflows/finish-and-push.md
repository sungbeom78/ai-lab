---
description: Autonomous workflow from work completion through commit and push
---

# finish-and-push

> When given a coding task, execute this loop end-to-end without asking for
> intermediate approval. Stop only at user-approval-required points
> (Section 3) or at unrecoverable errors (Section 4).

// turbo-all

---

## 0. Trigger conditions

This workflow applies when:
- User issues a coding task ("implement X", "fix Y", "modify Z")
- User has not explicitly forbidden commit/push

Skip this workflow only when:
- User explicitly says "do not commit" / "stop before commit"
- Task is design/analysis only (no code changes)

---

## 1. Step sequence (in order)

### Step 0. Prior Art Check (mandatory pre-flight)

```bash
python script/operation/charter/prior_art_check.py "<keyword>"
```

The keyword should describe what you're touching: filename, module name,
or short task description. The script searches:
- cache/task/registry.md (active tasks)
- doc/change_log.md (last 7 days)
- doc/change_log_archive/ (last 30 days)
- doc/SOURCE_OF_TRUTH.md (frozen zone awareness)
- doc/module_index.md (where the module lives)

It outputs findings and issues a session token at `cache/task/.prior_art_*.lock`.

**This token is required by Step 7. Without it, commit is blocked.**

If the search reveals:
- Active in_progress task on this area -> read its handoff.md before proceeding
- Recent modifications to the same files -> understand them; don't duplicate
- Frozen Zone overlap warning -> stop, request user approval (Section 3)

### Step 1. Do the work

Make the code changes. Read existing files before modifying.
Avoid creating duplicate logic.

### Step 2. qa_quick

```bash
python script/operation/charter/run_qa_quick_token.py
```

- PASS -> proceed
- FAIL -> diagnose -> fix -> rerun
- 2 consecutive FAILs -> report to user, stop

Never skip qa_quick. Never report "done" without qa_quick PASS.

### Step 3. Append to doc/change_log.md

Prepend a new entry at top-of-file:

```
## [yyyy-MM-dd HH:mm:ss]
### Modified / Added / Fixed / Removed
- One-line reason
- File: <path>
### Notes (optional)
- Follow-up or caveats
```

One commit may include multiple entries (one per logical change).
Never merge multiple changes into one entry. Never overwrite existing entries.

### Step 4. Update doc/module_index.md (only if public API changed)

If you added a new public class/function or changed a signature in src/, update
`doc/module_index.md` per GEMINI.md RULE 5-1 format:

```
## [Module Name]
- Path: src/path/to/file.py
- Classes: ClassName
- Responsibility: (what it does)
- Entry Point: method_name()
- Related Modules: ...
- Config: settings.yaml > section
```

If unsure whether a change qualifies, the pre-commit hook will tell you.

### Step 5. Glossary audit

Run the scanner. Do not guess.

```bash
python script/operation/audit_identifiers.py --changed-only
```

The scanner is the source of truth for identifier issues.

* PASS -> proceed
* WARN -> inspect generated report under `tmp/audit/audit_identifiers/`
* ERROR/FATAL -> fix before proceeding

For each unregistered word reported in files touched by this task:

1. Determine whether it is legacy or newly introduced by this task.
2. If legacy and unrelated -> record as legacy warning; do not rename casually.
3. If introduced by this task:

   * Check registered base forms and variants.
   * Check 3+ synonyms in `glossary/dictionary/words.json`.
   * If registered synonym/base exists -> rename code to registered word.
   * If genuinely new -> run `new-identifier-procedure.md` and wait for user approval.

### Step 6. git add (explicit files only)

```bash
git add <file1> <file2> ... doc/change_log.md
```

Never use `git add .` or `git add -A` (risk of including unintended files).
Include `doc/module_index.md` if Step 4 was performed.
Do not commit generated audit reports under `tmp/audit/` unless the user explicitly asks.

### Step 7. git commit

The pre-commit hooks run automatically. They will check:
- Workflow gate: prior_art_check token
- Workflow gate: qa_quick PASS token
- Article 1 (root files)
- Article 2 (OS scripts, platform isolation)
- Article 3 (Frozen Zone)
- Article 4.A (change_log staged)
- Article 4.B (auto-archive if needed)
- Article 5.A (encoding)
- Article 5.B (module_index for public API changes)
- Glossary audit (warn-only)

**Token verification**: Before this step succeeds, pre-commit verifies both:

```text
cache/task/.prior_art_*.lock
cache/task/.qa_quick_pass.lock
```

No prior-art token -> go back to Step 0.
No qa_quick PASS token -> go back to Step 2.

Commit message format:
```
<type>: <one-line summary>

<optional details>
- Bullet 1
- Bullet 2
```

`<type>`: feat / fix / docs / refactor / test / chore

If touching Frozen Zone with user approval, append:
```
CHARTER-FROZEN-APPROVED: <reason + user approval reference>
```

### Step 8. git push

```bash
git push
```

If push rejected (non-fast-forward) -> `git pull --rebase` -> resolve -> push.
If conflict requires manual resolution -> stop, report to user.

### Step 9. Report (mandatory before submitting)

**Before writing the final report**, verify token state:

```bash
python script/operation/charter/prior_art_check.py "<keyword>"
python script/operation/charter/run_qa_quick_token.py
```

Include the results inline in the report. Format:

```
[Done]
- Files: N changed
- qa_quick: PASS  (Duration: Xs, Checked: N items)
- commit: <short_hash> <first line of message>
- push: ok (origin/<branch>)

[Token Status]
- Prior Art : ✅ 유효 (issued HH:MM:SS, valid 60min)
- QA Quick  : ✅ PASS (HH:MM:SS)
```

If either token is expired or missing at report time:
- Re-run the corresponding script
- Include renewed token info in the report
- **Never submit a final report with expired tokens**

No checklist, no self-evaluation, no boilerplate beyond this format.
Pre-commit passing = charter compliance. The user knows.

---

## 2. Block handling (when pre-commit blocks at Step 7)

| Block | Self-handling |
|-------|---------------|
| Prior Art token missing/expired | Re-run `python script/operation/charter/prior_art_check.py "<keyword>"` |
| qa_quick token missing/expired | Re-run `python script/operation/charter/run_qa_quick_token.py` |
| Article 1 (root file) | `git mv <file> sandbox/` or `git restore --staged <file>` |
| Article 2 (.bat etc.) | Rewrite in Python at `script/operation/<name>.py`, unstage `.bat` |
| Article 2 (sys.platform) | Move OS branching to `src/common/platform.py` |
| Article 3 (Frozen Zone) | **STOP -> user approval** (Section 3) |
| Article 4.A (change_log) | Re-do Step 3, `git add doc/change_log.md` |
| Article 4.B (archive) | Hook performs archive automatically; just re-commit |
| Article 5.A (encoding) | Open problem file, save as UTF-8 LF, `git add` |
| Article 5.B (module_index) | Re-do Step 4, `git add doc/module_index.md` |

3 retries on the same block -> stop, report to user.
**Never use `git commit --no-verify`** unless user explicitly orders it.

---

## 3. User-approval-required points (stop and ask)

Stop the workflow and request user approval when:
- Frozen Zone change detected (Article 3)
- 10+ files changing
- New dependency in pyproject.toml or requirements.txt
- DB schema migration
- New environment variable
- 4+ new glossary identifiers
- prior_art_check.py reveals an active in_progress task on the same files

When stopping, report concisely:
- What needs to change
- Why
- Scope of impact
- Wait for response.

---

## 4. Unrecoverable errors

Report to user and stop when:
- qa_quick fails 2 consecutive times after fix attempts
- Same pre-commit block 3 times despite handling
- git push fails with conflict requiring manual resolution
- Telegram notification fails on new identifier (cannot proceed without approval)

Report format:
```
[Stopped] <reason>
- Step: <which step>
- Error: <one-line>
- Tried: <what you attempted>
- Need: <what you need from user>
```

---

## 5. Examples

### Example 1: Routine fix
```
Step 0: prior_art_check.py "circuit_breaker"
        -> 1 entry last 7 days, no active task, token issued
Step 1: edit src/risk/circuit_breaker.py
Step 2: qa_quick PASS
Step 3: append to change_log.md
Step 4: skipped (no public API change)
Step 5: skipped (no new identifiers)
Step 6: git add src/risk/circuit_breaker.py doc/change_log.md
Step 7: commit (pre-commit all pass)
Step 8: push ok
Step 9: report

[Done]
- Files: 2 changed
- qa_quick: PASS
- commit: a3f7c91 fix: adjust circuit breaker threshold
- push: ok (origin/main)
```

### Example 2: Frozen Zone
```
Step 0: prior_art_check.py "models.Position"
        -> FROZEN ZONE WARNING: src/common/models.py
Step 1 stopped immediately.

[Stopped] Frozen Zone change required
- Need: User approval to add 'realized_pnl' field to Position model
- Impact: 4 readers in src/execution/, 1 in src/report/
- Awaiting: explicit user approval -> will use CHARTER-FROZEN-APPROVED marker
```

### Example 3: Self-recovery
```
Step 7 blocked: Article 4.A - change_log.md not staged
-> re-do Step 3 (forgot to update)
-> git add doc/change_log.md
-> git commit (this time passes)
-> push ok
-> report
```

---

*This workflow makes Article 0 / Article 9 / RULE 1 / section 1-A enforceable
through the prior-art-check token. Without the token, commit cannot proceed.*
