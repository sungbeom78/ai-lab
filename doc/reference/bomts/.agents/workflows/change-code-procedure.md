---
description: Code change procedure - verification order, completion steps, and failure handling
---

# 코드 변경 절차

## 규칙 위치 (Source of Truth)
이 절차는 아래 문서의 규칙을 수행하기 위한 것이다:
- doc/README_AI_GUIDELINE.md § 변경 전 체크리스트
- doc/README_AI_GUIDELINE.md § Frozen Zone
- doc/README_AI_GUIDELINE.md § RULE B (qa_quick 필수)
- doc/SOURCE_OF_TRUTH.md (데이터 소유 모듈)
- doc/module_index.md (모듈 금지행위)
- doc/guidelines/09_data_flow.md (레이어 규칙)

## 관련 워크플로우
- 파일 수정 도구 사용 → /edit-file-procedure
- 명령 실행 시 자동 승인 여부 → /safe-command-policy

---

## Step 0 — 최근 이력 조회 (Prior Art Check, 필수)

> **목적**: 동일하거나 관련된 수정이 최근에 이미 이루어졌는지 확인하여, 작업의 파편화·이중 수정·SoT 훼손을 방지한다.
> 이 단계는 긴급 오류/장애 대응 시에도 **반드시** 수행한다. 생략 불가.

1. **Change Log 조회** — `doc/change_log.md` 에서 수정 대상 파일 또는 관련 키워드를 검색한다.
   - 조회 범위: 최소 **7일 이내**, 권장 **30일 이내**.
   - 검색 방법: `grep_search` 또는 대시보드 `/admin/tasks` 하단 변경 이력 타임라인에서 키워드 검색.
   - 확인 사항:
     - 동일 파일에 최근 수정이 있었는가? → 변경 의도와 충돌하지 않는지 확인.
     - 동일 증상/오류에 대한 수정 이력이 있는가? → 이전 수정이 불충분했는지, 재발인지 판별.
     - 관련 모듈에 구조 변경이 있었는가? → 호환성 확인.

2. **Task Registry 조회** — `cache/task/registry.md` 에서 `in_progress` 또는 최근 `done` 상태의 관련 작업이 있는지 확인한다.
   - 진행 중인 관련 타스크가 있다면 → 해당 `handoff.md`를 읽고, 현재 작업이 해당 타스크 범위에 속하는지 판단한다.
   - 속한다면 → 독립 수정 대신 해당 타스크의 `runlog`에 추가하는 방식으로 작업한다.

3. **판단 기록** — 조회 결과를 간략히 기록한다 (change_log.md 항목의 Notes 또는 runlog):
   - "관련 이력 없음" 또는
   - "관련 수정 존재: [날짜] [내용 요약] — 이번 수정과의 관계: [설명]"

> ⚠️ 이 단계를 생략하고 수정한 경우, 완료 보고(COMPLETION REPORT) 시 "Prior Art Check 미수행"으로 간주한다.

---

## Step 1 — 수정 전 확인 순서

> 아래는 doc/README_AI_GUIDELINE.md § 변경 전 체크리스트를 수행하는 순서이다.
> 규칙 본문은 해당 문서를 참조.

1. `doc/SOURCE_OF_TRUTH.md` 열어 수정 대상의 데이터 소유 모듈 확인
2. `doc/module_index.md` 열어 해당 모듈의 금지행위(Forbidden) 확인
3. `doc/guidelines/09_data_flow.md`의 레이어 규칙 위반 여부 확인
4. `doc/README_AI_GUIDELINE.md` § Frozen Zone 해당 여부 확인
5. 관련 불변 규칙(INV-xxx) 유효성 확인

---

## Step 2 — 수정 중 (파일 편집)

> /edit-file-procedure 워크플로우에 따라 수행

---

## Step 3 — 수정 후 마무리 순서

// turbo-all
1. `python -m py_compile <수정파일>` — 문법 검증
2. `python run_test.py qa_quick` — QA 실행 (PASS 필수) 혹은 웹페이지 '/admin/settings'의 '실행상태 점검' 수행 후 성공 확인
3. `doc/module_index.md` 업데이트 (모듈/파일 추가·변경 시)
4. `doc/change_log.md` 최상단에 변경 기록 추가

---

## §SUBMODULE — 서브모듈 작업 시 별도 절차

> glossary 등 Git submodule 작업은 **해당 서브모듈 내의 `.agents/workflows/`를 따른다**.
> main 프로젝트의 이 절차와 별개로 관리된다.

| 서브모듈 | 전용 workflow 위치 |
|-----------|-------------------|
| `glossary/` | `glossary/.agents/workflows/change-code-procedure.md` |

## 실패 시 처리

| 실패 단계 | 조치 |
|----------|------|
| `py_compile` 실패 | 문법 오류 수정 후 재시도 |
| `qa_quick` 1회 실패 | 실패 원인 분석 → 코드 수정 → qa_quick 재실행 |
| `qa_quick` 2회 연속 실패 | 추가 변경 즉시 중단, 변경 내역과 실패 원인을 사용자에게 보고 |
| Frozen Zone 해당 | 작업 즉시 중단, 사용자 승인 요청 |

---

## 예외 상황 처리

| 상황 | 조치 |
|------|------|
| 문서 참조 경로가 존재하지 않거나 읽기 실패 | 작업 즉시 중단, 사용자에게 경로 확인 요청 |
| workflow 간 규칙 충돌 발생 | 작업 즉시 중단, 충돌 내용을 사용자에게 보고 후 판단 요청 |
| 동일 단계 3회 이상 반복 (수정→실패→수정 루프) | 무한 루프 방지 위해 즉시 중단, 현재 상태를 사용자에게 보고 |
