# AI Agent Task Start Format

## 0. Task Identity

- Project:
- Task name:
- Task type:
  - [ ] environment setup
  - [ ] document update
  - [ ] code analysis
  - [ ] code change
  - [ ] bug fix
  - [ ] test addition
  - [ ] operation report
  - [ ] patch proposal
  - [ ] lostway planning
  - [ ] BomTS read-only analysis
- Target path:
- Related module:
- Expected output:

---

## 1. Mandatory Rule Loading

Before doing any work, read the following files.

### Common AI Hub Rules

- `/project/ai-hub/config/model_routing.yaml`
- `/project/ai-hub/config/tool_permission.yaml`
- `/project/ai-hub/config/path_policy.yaml`

### BomTS Reference Rules

If the task touches BomTS, read:

- `/project/ai-hub/doc/reference/bomts/PROJECT_CHARTER.md`
- `/project/ai-hub/doc/reference/bomts/.gemini/user_rules.md`
- `/project/ai-hub/doc/reference/bomts/AGENTS.md`
- `/project/ai-hub/doc/reference/bomts/doc/README_AI_GUIDELINE.md`
- `/project/ai-hub/doc/reference/bomts/doc/SOURCE_OF_TRUTH.md`
- `/project/ai-hub/doc/reference/bomts/doc/module_index.md`

If the task changes code, additionally read:

- `/project/ai-hub/doc/reference/bomts/.agents/workflow/change-code-procedure.md`
- `/project/ai-hub/doc/reference/bomts/.agents/workflow/edit-file-procedure.md`
- `/project/ai-hub/doc/reference/bomts/doc/guideline/09_data_flow.md`
- `/project/ai-hub/doc/reference/bomts/doc/guideline/10_qa.md`

If the task creates or renames identifiers, additionally read:

- `/project/ai-hub/doc/reference/bomts/doc/guideline/06_glossary_rules.md`
- `/project/ai-hub/doc/reference/bomts/.agents/workflow/new-identifier-procedure.md`

---

## 2. Pre-Work Check

Answer these before touching files.

```text
[Pre-Work Check]
- Task scope:
- Target files:
- Affected module:
- Source of Truth owner:
- Frozen Zone involved: yes/no
- Trading logic involved: yes/no
- Order execution involved: yes/no
- Config or secret involved: yes/no
- New dependency involved: yes/no
- New identifier involved: yes/no
- Human approval required: yes/no
- Reason:
```

If human approval is required, stop and report.

---

## 3. Allowed Actions

The agent may:

* Read files
* Search code
* Generate analysis reports
* Generate draft patches
* Generate test plans
* Run safe read-only commands
* Run approved test commands
* Update documentation drafts

---

## 4. Forbidden Actions

The agent must not:

* Modify secret files
* Modify API keys
* Modify live trading logic without approval
* Modify order execution logic without approval
* Modify risk rules without approval
* Modify Frozen Zone without approval
* Auto commit
* Auto push
* Auto deploy
* Open Ollama or internal APIs to LAN without approval
* Use `git commit --no-verify`

---

## 5. Work Procedure

For analysis-only tasks:

```text
1. Read required rules.
2. Inspect minimum required files.
3. Produce findings.
4. Produce recommended next action.
5. Do not modify source files.
```

For code-change tasks:

```text
1. Run prior art check if working directly inside BomTS repo.
2. Read required rules.
3. Identify Source of Truth and Frozen Zone.
4. Inspect minimum files.
5. Create or update tests first if bug fix.
6. Apply minimal change.
7. Run py_compile for changed Python files.
8. Run qa_quick or proposed equivalent.
9. Update change_log and module_index if required.
10. Report evidence.
```

For AI Hub tasks:

```text
1. Respect singular directory naming.
2. Keep reference files read-only.
3. Store generated output under doc, log, publish, or runtime.
4. Do not modify BomTS source unless explicitly instructed.
```

---

## 6. Completion Report

For analysis-only task:

```text
[Analysis Complete]
- Scope:
- Files inspected:
- Findings:
- Risk:
- Next action:
```

For draft patch task:

```text
[Patch Draft Complete]
- Files proposed:
- Reason:
- Test required:
- Risk:
- Approval required:
```

For committed BomTS task, use BomTS format only:

```text
[Done]
- Files: N changed
- qa_quick: PASS
- commit: <hash> <msg>
- push: ok (origin/<branch>)
```