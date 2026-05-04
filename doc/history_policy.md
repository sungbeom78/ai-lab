# History Policy

## 1. 목적 (Why)
AI Hub 내의 모든 작업 흐름, 오류, 의사결정을 누락 없이 이력으로 남겨 차후의 분석, 복구, 지식 축적을 용이하게 합니다.
특히 이 이력 데이터는 향후 `www.ahnda.com`, `www.bomts.com` 등 웹사이트에 개발/운영 블로그 글감으로 가공되어 게시될 수 있는 원천 자료가 됩니다.

## 2. 기록 대상 및 분류 (What)
이력은 아래와 같이 분류되어 저장됩니다.

- **Session (`doc/history/session/`)**: 특정 Task/작업 세션 전체의 맥락, 목표, 진행, 결과를 요약한 마스터 기록
- **Reference (`doc/history/reference/`)**: AI 작업 중 자동 생성된 기술 레퍼런스 기록 (yyyyMMdd_HHmmss_* 패턴)
- **Event (`doc/history/event/`)**: 중요한 실행 명령, 결과, 시스템 변화 등 개별 이벤트 기록
- **Decision (`doc/history/decision/`)**: 아키텍처, 정책, 설계 등 중요한 의사결정과 그 사유
- **Error (`doc/history/error/`)**: 실패, 중단, 사용자 승인 보류 등 문제 상황 및 원인 분석

> **주의**: `doc/reference/bomts/` 는 BomTS 레포지토리 규칙 사본 전용 경로다.
> AI 작업 자동 생성 레퍼런스 파일은 반드시 `doc/history/reference/` 에 저장한다.

## 3. 파일명 규칙
- 형식: `YYYYMMdd_HHmmss_<프로젝트>_<작업명>.md`
- 예시:
  - `20260503_150332_ai-hub_prepare_local_ai_console_reference.md`
  - `20260504_113800_project_workspace_policy_session.md`

## 4. 활용 (Publish 흐름)
작업 이력이 일정 수준 축적되면, 이를 기반으로 `publish-source` 초안을 작성하여 향후 웹 게시를 위한 글감으로 승급(Promotion)시킵니다.
