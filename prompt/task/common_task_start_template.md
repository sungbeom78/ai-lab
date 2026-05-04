# Common Task Start Template

## 0. Task Identity

- Target project:
  - [ ] ai-hub
  - [ ] bomts-ai
  - [ ] lostway
  - [ ] shared
- Task name:
- Task type:
  - [ ] read-only analysis
  - [ ] document update
  - [ ] environment setup
  - [ ] code analysis
  - [ ] patch proposal
  - [ ] code change
  - [ ] test addition
  - [ ] operation report
- Target path:
- Expected output:

---

## 1. Rule Loading

Always read:

```text
/project/ai-hub/prompt/system/ai_hub_work_start.md
```

If target project is BomTS, additionally read:

```text
/project/ai-hub/prompt/project/bomts_work_start.md
/project/ai-hub/prompt/task/bomts_task_start_template.md
```

If target project is lostway, additionally read:

```text
/project/ai-hub/prompt/project/lostway_work_start.md
/project/ai-hub/prompt/task/lostway_task_start_template.md
```

---

## 2. Pre-Work Check

```text
[Pre-Work Check]
- Target project:
- Target path:
- Files to inspect:
- Files to modify:
- Project-specific rule loaded: yes/no
- Secret involved: yes/no
- Production behavior involved: yes/no
- External network involved: yes/no
- Human approval required: yes/no
- Reason:
```

If approval is required, stop and report for that specific task, but continue with other auto-run capable tasks.

---

## 3. Work Procedure (자동 실행 우선)

1. 사전 점검은 묻지 말고 자동 실행한다.
2. 작업 시작 시 `/project/ai-hub/doc/history/session/`에 Session Log를 생성한다.
3. 작업 중 중요한 실행, 의사결정, 에러는 `event`, `decision`, `error` 디렉토리에 각각 기록한다.
4. 기존 파일 읽기 및 안전한 수정(문서, 지침 등)은 자동 적용한다.
5. 최소 범위 변경을 지키며, 기존 내용을 가급적 보존한다.
6. 위험/승인 필요 작업만 중단하고 사용자에게 승인을 요청한다.
7. 적절한 검증을 로컬에서 자동 실행한다.
8. 완료 후 `/project/ai-hub/doc/out` 등 지정된 경로에 결과를 작성하고, 웹 게시 대상인 경우 `/project/ai-hub/doc/publish-source/`에 초안을 생성한다.

---

## 4. Completion Report

```text
[Complete]
- Files changed:
- History created:
- Publish source created:
- Pending approval:
- Report:
```
