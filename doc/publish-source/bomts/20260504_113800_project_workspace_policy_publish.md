# On-Premise AI Workspace: 넓게 열고 좁게 수정하는 개발 환경 구축

- Date: 2026-05-04
- Category: DevOps / AI Infrastructure
- Status: Draft

## 배경

로컬 AI 개발 환경(desktop-ai)에서 여러 프로젝트를 통합 관리하려면
하나의 workspace root 아래에 일관된 정책이 필요하다.

기존에는 `ai-hub` 단독으로 작업 범위를 정의했지만,
site 개발, bomts-ai 관리, lostway 서비스 등 여러 영역을 다루면서
workspace 전체를 아우르는 정책이 필요해졌다.

## 문제

- 프로젝트마다 수정 권한과 위험도가 다르다
- AI 에이전트가 전체 파일시스템에 접근 가능하면 사고 위험이 있다
- 기록이 분산되면 나중에 추적이 어렵다
- git 전략이 없으면 대형 바이너리와 비밀 파일이 커밋될 수 있다

## 해결 방향

### 핵심 원칙: "넓게 열고, 좁게 수정한다"

- workspace root는 `/project` 전체
- 모든 프로젝트를 볼 수 있지만, 수정 범위는 매 작업마다 명확히 제한
- 경로별로 Auto Allowed / Development Allowed / Approval Required / Strong Approval / Forbidden 티어 적용

### 작업 모드

Inspect → Prepare → Develop → Validate → Operate → Release 순서로 진행.
Release만 사용자 승인 필요, 나머지는 티어에 따라 자율 진행.

### 4종 기록 정책

모든 의미 있는 작업은 4종 기록을 남긴다:
1. Session 기록 (내부 원장)
2. ahnda 로그 (개인 회고)
3. bomts 기술 레퍼런스 (재현 가능 문서)
4. bomts 게시 후보 (기술 블로그 초안)

## 구현 내용

### 생성한 파일

| 파일 | 역할 |
|------|------|
| `README.md` | workspace 개요, 디렉토리 구조, 수정 정책 요약 |
| `workspace.yaml` | 프로젝트 매니페스트 (경로, 역할, modify_policy) |
| `.gitignore` | 대형 바이너리, 캐시, 민감 파일 제외 |
| `doc/workspace_policy.md` | 전체 정책 상세 (권한 티어, 기록 정책 등) |
| `doc/git_strategy.md` | 독립 repo + manifest 전략, submodule 검토 |

### 경로별 수정 정책 요약

```text
ai-hub        → Auto Allowed (자유 수정)
site/ahnda    → Development Allowed (실험형 개발)
site/bomts    → Approval Required (별도 지시 시)
bomts-ai      → Approval Required (실거래는 Strong)
lostway       → Approval Required
script        → Development Allowed (시스템 스크립트는 승인)
doc, publish  → Auto Allowed
log           → Read Only
model, rag-index, runtime → 상태 확인만
```

## 검증

- 5개 파일 생성 확인
- 민감 정보 키워드 검사 통과
- YAML 기본 문법 확인

## 다음 단계

1. site/ahnda 마운트 후 ahnda 포털 MVP 개발
2. Local AI Console 상태 확인 및 기능 개선
3. git init/commit (사용자 승인 후)
4. 개별 프로젝트별 하위 지침 정리 (필요 시)
