# BOM_TS Task Start Template

## 0. Task Identity

- Project: BOM_TS
- Task name:
- Task type:
  - [ ] read-only analysis
  - [ ] operation report
  - [ ] incident analysis
  - [ ] patch proposal
  - [ ] code change
  - [ ] document update
  - [ ] test addition
  - [ ] environment setup
- Target path:
- Related module:
- Expected output:

---

## 1. Mandatory Reference Load

Before doing any BomTS-related work, read the following files.

### Highest Priority

- `/project/ai-hub/doc/reference/bomts/PROJECT_CHARTER.md`
- `/project/ai-hub/doc/reference/bomts/.gemini/user_rules.md`
- `/project/ai-hub/doc/reference/bomts/AGENTS.md`

### Project Documentation

- `/project/ai-hub/doc/reference/bomts/doc/README_AI_GUIDELINE.md`
- `/project/ai-hub/doc/reference/bomts/doc/SOURCE_OF_TRUTH.md`
- `/project/ai-hub/doc/reference/bomts/doc/module_index.md`

### Workflow Reference

For code-affecting work, also read:

- `/project/ai-hub/doc/reference/bomts/.agents/workflows/change-code-procedure.md`
- `/project/ai-hub/doc/reference/bomts/.agents/workflows/edit-file-procedure.md`
- `/project/ai-hub/doc/reference/bomts/.agents/workflows/safe-command-policy.md`

For identifier creation or rename, also read:

- `/project/ai-hub/doc/reference/bomts/doc/guideline/06_glossary_rules.md`
- `/project/ai-hub/doc/reference/bomts/.agents/workflows/new-identifier-procedure.md`

For QA or completion work, also read:

- `/project/ai-hub/doc/reference/bomts/doc/guideline/10_qa.md`
- `/project/ai-hub/doc/reference/bomts/.agents/workflows/finish-and-push.md`

---

## 2. Pre-Work Check

Before touching any source file, fill this out.

```text
[Pre-Work Check]
- Task scope:
- Target file:
- Affected module:
- Source of Truth owner:
- Frozen Zone involved: yes/no
- Trading logic involved: yes/no
- Order execution involved: yes/no
- Position sizing involved: yes/no
- Risk rule involved: yes/no
- Config involved: yes/no
- Secret involved: yes/no
- DB schema involved: yes/no
- New dependency involved: yes/no
- New identifier involved: yes/no
- Human approval required: yes/no
- Reason:
```

If human approval is required, stop and report before making changes.

---

## 3. Work Mode

### 3.1 Read-Only Analysis Mode

Use this mode for:

* operation report
* incident analysis
* log review
* architecture review
* documentation review

Rules:

* Do not modify source files.
* Do not modify config.
* Do not modify secret.
* Do not commit.
* Produce findings and recommended next action.

Output format:

```text
[Analysis Complete]
- Scope:
- Files inspected:
- Findings:
- Risk:
- Recommended next action:
```

---

### 3.2 Patch Proposal Mode

Use this mode when a change is needed but not yet approved.

Rules:

* Inspect minimum required files.
* Produce draft patch or file-level change plan.
* Do not apply patch unless explicitly approved.
* Do not commit.
* Do not push.

Output format:

```text
[Patch Proposal]
- Problem:
- Cause:
- Proposed files:
- Proposed change:
- Required test:
- Risk:
- Approval required:
```

---

### 3.3 Code Change Mode

Use this mode only when explicitly instructed to modify BomTS source code.

Procedure:

1. Run prior art check in the BomTS repository.
2. Read mandatory reference files.
3. Identify Source of Truth owner.
4. Check Frozen Zone.
5. Check glossary/naming impact.
6. Apply minimum-scope change.
7. Run syntax check for changed Python files.
8. Run required QA.
9. Update `doc/change_log.md` if required.
10. Update `doc/module_index.md` if public class/function/signature changed.
11. Report verification evidence.

Do not bypass pre-commit.
Do not use `git commit --no-verify`.

---

## 4. Forbidden Actions

The agent must not:

* Modify live trading logic without approval.
* Modify order execution logic without approval.
* Modify position sizing logic without approval.
* Modify risk rules without approval.
* Modify Frozen Zone without approval.
* Modify API key or secret.
* Modify DB schema without approval.
* Add new dependency without approval.
* Auto deploy.
* Auto push to `main`.
* Open Ollama or internal API to LAN without explicit approval.
* Use `git commit --no-verify`.

---

## 5. Completion Format

For read-only analysis:

```text
[Analysis Complete]
- Scope:
- Files inspected:
- Findings:
- Risk:
- Next action:
```

For patch proposal:

```text
[Patch Proposal Complete]
- Files proposed:
- Reason:
- Test required:
- Risk:
- Approval required:
```

For committed BomTS work, use the BomTS completion format:

```text
[Done]
- Files: N changed
- qa_quick: PASS
- commit: <short_hash> <message>
- push: ok (origin/<branch>)
```