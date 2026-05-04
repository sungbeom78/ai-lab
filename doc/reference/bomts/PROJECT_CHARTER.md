# PROJECT_CHARTER.md - BOM_TS Constitution

> **Version**: 2.0.0
> **Effective**: 2026-04-30
> **Frozen Until**: 2026-07-31
> **Replaces**: v1.0 (2026-04-28) - 10 articles -> 5 articles

---

## Charter Philosophy

> This charter contains ONLY articles that are **physically enforced by automation**.
> "Articles AI is hoped to follow" have no place here. If not enforced, not a charter.
> AI behavior guidelines belong in `.gemini/user_rules.md` and `.agents/workflows/`.

**Conflict Priority**: PROJECT_CHARTER > .gemini/user_rules.md > .agents/workflows/ > others

---

## 5 Absolute Articles (all enforced by pre-commit + CI)

### Article 1. No new files in repo root

Forbidden in repo root except:
`run.py`, `run_test.py`, `README.md`, `AGENTS.md`, `GEMINI.md`,
`PROJECT_CHARTER.md`, `.gitignore`, `.pre-commit-config.yaml`,
`pyproject.toml`, `LICENSE`, `.env.example`

Specifically blocked: `_diag_*.py`, `tmp_*.py`, `scratchpad*.py`,
root-level `.bat`/`.ps1`/`.vbs`/`.sh`

Scratch / experimental / diagnostic code -> **`sandbox/` only** (gitignored).

**Enforcement**: `charter-no-root-scratch` + `charter-no-tmp-prefix`

---

### Article 2. No OS-specific scripts

Forbidden new file types: `.ps1` / `.bat` / `.vbs` / `.sh` / `.cmd`
OS branching MUST go through `src/common/platform.py` only.
Direct use of `sys.platform` / `platform.system()` / `os.name` forbidden elsewhere.

#### Frozen Exception (1 file)
| File | Rationale | Approved |
|------|-----------|----------|
| `script/operation/legacy/restart_mt5_bridge.bat` | Shim only - all logic in `.py` | 2026-04-28 |

**Enforcement**: `charter-no-os-scripts` + `charter-platform-isolation`

---

### Article 3. Frozen Zone protection

The following may NOT be modified without explicit user approval:
- `src/common/models.py` public fields
- `config/settings.yaml` existing keys
- `script/db/schema*.sql` existing columns
- `src/adapter/*/base.py` public interface
- `src/storage/redis_client.py` key patterns
- `PROJECT_CHARTER.md` (frozen until 2026-07-31)

When approved, commit message MUST include:
```
CHARTER-FROZEN-APPROVED: <rationale>
```

**Enforcement**: `charter-frozen-zone`

---

### Article 4. change_log.md companion update + auto archive

When `src/`, `script/db/`, or `config/` changes, the SAME commit MUST include
`doc/change_log.md` update.

Format (prepend to top-of-file):
```
## [yyyy-MM-dd HH:mm:ss]
### Modified / Added / Fixed / Removed
- One-line reason
- File: <path>
```

**Auto archive**: When `change_log.md` exceeds 500 lines OR on the 1st of each
month, contents are automatically moved to
`doc/change_log_archive/YYYYMM_change_log.md` and the file is reset.
This was the original behavior (per GEMINI.md RULE 5-3) and is now enforced
by pre-commit hook.

**Enforcement**: `charter-changelog-required` + `charter-changelog-archive`

---

### Article 5. Encoding hygiene + module_index update

#### 5.A Encoding
All text files: **UTF-8 No-BOM, LF, trailing newline**.

Forbidden:
- PowerShell `Set-Content` / `Out-File` (cp949/UTF-16 leak)
- Python `'utf-8-sig'` encoding (BOM injection)
- CRLF line endings

#### 5.B module_index.md companion update (per GEMINI.md RULE 5-1)
When new public class/function is added or signature changed in `src/`, the same
commit MUST include `doc/module_index.md` update.

**Enforcement**: `charter-encoding-check` + `charter-module-index` +
`mixed-line-ending` + `end-of-file-fixer`

---

## What is NOT in the Charter (intentionally)

The following live in workflows / user_rules instead, but are still **mandatory**
when applicable - they're enforced through different mechanisms:

| Removed Article | New Location | Enforcement |
|-----------------|--------------|-------------|
| Article 0 (5-line ack) | DELETED | Replaced by `prior_art_check.py` token gate |
| Article 3 (qa_quick) | `finish-and-push.md` + `run_qa_quick_token.py` | `charter-qa-quick-token` pre-commit hook |
| Article 5 (Glossary check-id) | `audit_identifiers.py` + `new-identifier-procedure.md` | scanner-driven audit + Telegram approval for genuine new words |
| Article 6 (workflow bypass) | DELETED | Workflow gates are enforced by token hooks |
| Article 9 (task registry) | `prior_art_check.py` + `check_prior_art_token.py` | `charter-prior-art-token` pre-commit hook |
| Article 10 (violation report) | DELETED | Replaced by fail-fast hooks and explicit workflow stop conditions |

**Prior Art Check** (was AGENTS.md §1-A) is now enforced via
`script/operation/charter/prior_art_check.py` and
`script/operation/charter/check_prior_art_token.py`.

`prior_art_check.py` generates a session token, and the pre-commit hook
`charter-prior-art-token` blocks commit when the token is missing or expired.

`qa_quick` is enforced the same way:
`run_qa_quick_token.py` runs `python run_test.py qa_quick` and issues
`cache/task/.qa_quick_pass.lock`; `charter-qa-quick-token` blocks commit when
the token is missing or expired.

---

## Charter Amendment

Charter is **frozen until 2026-07-31**. Amendments require:
1. Explicit user approval (response containing literal "PROJECT_CHARTER amendment approved")
2. Version bump (semver)
3. Permanent record in `PROJECT_CHARTER_change_log.md`
4. Notification to all AI tools (Antigravity / Codex / Claude)

---

## Appendix A. `restart_mt5_bridge.bat` handling

This file is the only Frozen Exception under Article 2.

**Structure:**
- `script/operation/legacy/restart_mt5_bridge.bat` - shim only (1 line)
- `script/operation/restart_mt5_bridge.py` - all logic

**Rules:**
- Adding logic to the `.bat` file = Article 2 violation
- This exception cannot be cited to justify NEW OS-specific scripts
- Preserved permanently for Task Scheduler / shortcut compatibility

---

*This charter is enforceable, not aspirational.*
