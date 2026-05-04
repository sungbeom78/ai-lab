# BOM_TS Reference Map

## Purpose

This directory stores a read-only reference copy of BOM_TS project rules.

The AI Hub uses this reference to guide:
- BomTS read-only operation reports
- BomTS incident analysis
- BomTS patch proposal
- BomTS documentation generation
- BomTS Antigravity task start protocol

## Source

- Repository: https://github.com/sungbeom78/bomiyang-trade-system
- Branch: main

## Priority Order

1. PROJECT_CHARTER.md
2. .gemini/user_rules.md
3. .agents/workflow/
4. AGENTS.md
5. doc/README_AI_GUIDELINE.md
6. doc/SOURCE_OF_TRUTH.md
7. doc/module_index.md
8. doc/guideline/
9. Agent judgment

## Important Notes

- PROJECT_CHARTER.md contains only automation-enforced articles.
- AGENTS.md contains broader autonomous coding rules.
- .gemini/user_rules.md defines Antigravity/Codex/Claude behavior.
- doc/README_AI_GUIDELINE.md defines BomTS-specific AI work restrictions.
- doc/SOURCE_OF_TRUTH.md defines ownership, Frozen Interface, and data SoT.
- doc/module_index.md defines module responsibility and forbidden behavior.
- doc/guideline/ contains task-specific rules.

## Local Usage

Before any BomTS-related task, the AI agent must:
1. Read the priority documents.
2. Identify affected module.
3. Check Frozen Zone.
4. Check Source of Truth ownership.
5. Check naming/glossary rules.
6. Decide whether human approval is required.
7. Only then proceed.

## Prohibition

The reference copy must not be edited directly.
If the source repo changes, update this directory by sync.