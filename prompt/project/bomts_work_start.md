# BOM_TS Project Work Start Prompt

This prompt applies only when the task touches BOM_TS or `/project/bomts-ai`.

BOM_TS is an automated trading system.
A single unsafe change can cause real financial loss.

This is not the global AI Hub policy.
This is a project-specific policy loaded only for BomTS work.

---

## 1. BomTS Rule Priority

Follow this priority for BomTS tasks:

1. `/project/ai-hub/doc/reference/bomts/PROJECT_CHARTER.md`
2. `/project/ai-hub/doc/reference/bomts/.gemini/user_rules.md`
3. `/project/ai-hub/doc/reference/bomts/.agents/workflows/`
4. `/project/ai-hub/doc/reference/bomts/AGENTS.md`
5. `/project/ai-hub/doc/reference/bomts/doc/README_AI_GUIDELINE.md`
6. `/project/ai-hub/doc/reference/bomts/doc/SOURCE_OF_TRUTH.md`
7. `/project/ai-hub/doc/reference/bomts/doc/module_index.md`
8. `/project/ai-hub/doc/reference/bomts/doc/guideline/`
9. AI Hub common policy
10. Agent judgment

---

## 2. Before Touching BomTS Source

Before touching BomTS source code:

1. Read mandatory reference files.
2. Identify affected module.
3. Identify Source of Truth owner.
4. Check Frozen Zone.
5. Check whether the task touches:
   - trading logic
   - order execution
   - position sizing
   - risk rule
   - secret
   - DB schema
   - dependency
6. If approval is required, stop and report.
7. If no approval is required, proceed with minimum scope.
8. Produce verification evidence.

---

## 3. BomTS Restrictions

You must not:

- Modify live trading logic without approval.
- Modify order execution without approval.
- Modify position sizing without approval.
- Modify risk rules without approval.
- Modify Frozen Zone without approval.
- Modify secrets.
- Modify DB schema without approval.
- Add dependencies without approval.
- Auto commit or push unless explicitly instructed.
- Bypass pre-commit.
- Use `git commit --no-verify`.

---

## 4. Work Mode

For read-only BomTS analysis:

- Do not modify files.
- Produce analysis report only.

For BomTS patch proposal:

- Produce draft diff or change plan only.
- Do not apply unless approved.

For actual BomTS code work:

- Follow BomTS prior_art_check and qa_quick token workflow.
- Update change_log/module_index if required.
- Run required verification.
