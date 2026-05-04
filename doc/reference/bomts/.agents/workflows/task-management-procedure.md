---
description: AI Task state management procedure for maintaining context across sessions
---

# Task Management Procedure (작업 상태 관리 절차)

## 규칙 위치 (Source of Truth)
이 절차는 아래 문서의 규칙을 수행하기 위한 것이다:
- `doc/plan/last_report_plan__task_upgrade.md`

---

## 1. 새 작업 시작 (Start a New Task)
**중요 원칙**: AI는 모든 내용(Manifest, Runlog, Handoff, Registry 등)을 **반드시 한국어(Korean)**로만 작성해야 하며, 표 형태가 적합한 곳에는 마크다운 표 생성을 적극적으로 활용한다. 추가로, 모든 일시(Timestamp)는 반드시 **한국 시간(KST, UTC+9)** 기준으로 기록한다.

새로운 작업이 시작되면 다음 순서로 수행한다.
1. `task_id` 생성 (포맷: `<yyyyMMdd>_<task_name>`, 예: `20260421_add_task_workflow`)
2. `cache/task/registry.md` 에 새 작업 등록 (없으면 생성).
3. `doc/reference/task_manifest/<task_id>_task_manifest.md` 생성:
   - task title, objective, scope, non-scope, related docs, related files, sensitive areas, acceptance / verification criteria, approval-required areas, current known status, constraints, execution notes 포함.
4. `cache/task/<task_id>_handoff.md` 생성: 초기 handoff(시작 상태와 다음 액션) 명시.
5. `cache/task/<task_id>_runlog.md` 생성: 의미 있는 액션 단위로 누적하는 이력 파일 생성.
6. (선택) 범위/판단 변화 이력 파일 `tmp/task/history/<task_id>_task_manifest_history.md` 생성.

---

## 2. 작업 진행 중 (During the Task)
작업 흐름 중 다음을 갱신한다.
- 의미 있는 변경 후 `runlog` append.
- 진행 상태 (Status) 변화 시 `handoff` 갱신.
- 범위 및 제약사항 변경 시 `manifest` 갱신 + `history` append.

---

## 3. 기존 작업 이어가기 (Resume Existing Task)
사용자가 이전 작업을 이어서 하도록 요청한 경우 (Resume):
1. 전체 아키텍처 재분석부터 시작하지 않는다.
2. `cache/task/registry.md` 에서 active task를 찾는다.
3. 해당 task의 `handoff`를 먼저 읽는다.
4. `manifest` 범위 내에서 명시된 상태로부터 작업을 재개한다.

---

## 4. 작업 종료 및 세션 중단 전 (Before Ending Task / Session)
세션 종료 직전 반드시 다음을 수행한다.
1. `cache/task/<task_id>_handoff.md` 최신화 (완료된 것, 남은 것, 바로 다음 액션, 마지막으로 수정한 파일 등).
2. `cache/task/<task_id>_runlog.md` 에 로그 기록 append.
3. `cache/task/registry.md` 상태 갱신 (진행 중: `in_progress`, 대기: `blocked`, 완료: `done` 등) 및 `last_updated` 갱신.
