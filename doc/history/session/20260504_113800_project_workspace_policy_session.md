# Session 기록: /project Workspace 정책 정리

- Date: 2026-05-04
- Time: 11:38
- Project: project (workspace root)
- Task: workspace_policy
- Mode: Prepare → Develop → Validate
- Status: Completed

## 1. 작업 목적

`/project` 전체를 workspace root로 사용하면서,
기존 ai-hub 중심 작업 지침을 `/project` 전체에서 사용할 수 있도록 재정리.

## 2. 수행 내용

### Inspect
- `/project` 루트 구조 확인 (ls -la)
- 심볼릭 링크 대상 확인 (ai-hub → /mnt/d/project/ai-hub 등)
- 기존 ai-hub 레퍼런스 파일 스타일 확인
- site, lostway 경로는 Permission denied (마운트 필요)

### Develop
- `/project/README.md` 신규 생성
- `/project/workspace.yaml` 신규 생성
- `/project/.gitignore` 신규 생성
- `/project/doc/workspace_policy.md` 신규 생성
- `/project/doc/git_strategy.md` 신규 생성

### Validate
- 생성 파일 존재 및 비어있지 않음 확인
- YAML 문법 확인
- 민감 정보 후보 검사

## 3. 생성한 파일

```text
/project/README.md                    — workspace 개요
/project/workspace.yaml               — 프로젝트 매니페스트
/project/.gitignore                   — git 제외 목록
/project/doc/workspace_policy.md      — 전체 정책 상세
/project/doc/git_strategy.md          — Git 전략
```

## 4. 수정한 파일

없음 (모두 신규 생성)

## 5. 검증

- 파일 존재 확인: OK
- 민감 정보 검사: 민감 키워드 없음
- YAML 기본 문법: OK

## 6. 남은 문제

- `site`, `lostway` 심볼릭 링크가 Permission denied — 마운트 스크립트 실행 필요
- git init/commit은 사용자 승인 대기

## 7. 다음 작업

- `/project/site/ahnda` 마운트 후 ahnda 포털 MVP 개발 시작
- Local AI Console 상태 확인 및 기능 개선
- 개별 프로젝트별 하위 지침 정리 (필요 시)

## 8. 관련 기록

```text
session:         /project/ai-hub/doc/history/session/20260504_113800_project_workspace_policy_session.md
ahnda log:       /project/ai-hub/doc/publish-source/ahnda/20260504_113800_project_workspace_policy_log.md
bomts reference: /project/ai-hub/doc/reference/bomts/20260504_113800_project_workspace_policy_reference.md
bomts publish:   /project/ai-hub/doc/publish-source/bomts/20260504_113800_project_workspace_policy_publish.md
```
