# Project Path Policy

이 문서는 AI Hub 환경의 각 프로젝트 및 디렉토리 구조 매핑을 정의합니다.

## 1. 기반 경로 (Windows SSD 연동)
- `/project/ai-hub`: 공통 AI 작업 허브 및 지침 공간
- `/project/bomts-ai`: BomTS 프로젝트 및 Reference 지침
- `/project/doc`: 전체 공통 문서 저장소
- `/project/log`: 로그 저장소
- `/project/publish`: 게시 후보 산출물 공간 (실제 서비스 루트 아님)
- `/project/script`: 셸 스크립트 도구들

## 2. 서비스/원격 마운트 경로 (SSHFS 등)
- `/project/lostway`: 서비스 서버 Linux의 `/project/lostway` 마운트 지점 (상담/대화 서비스)
- `/project/site`: NUC-main Linux의 `/project/site` 마운트 지점
  - `/project/site/ahnda`: `www.ahnda.com` 실제 서비스 루트
  - `/project/site/bomts`: `www.bomts.net` / `www.bomts.com` 실제 서비스 루트

## 3. 로컬 환경 전용 (AI 실행 등)
- `/project/model` -> `~/ai-local/model`: 로컬 다운로드 모델 공간
- `/project/rag-index` -> `~/ai-local/rag-index`: RAG 검색용 벡터/인덱스 저장소
- `/project/runtime` -> `~/ai-local/runtime`: 런타임 캐시 및 실행 파일 공간

## 4. 디렉토리 명명 규칙
- 새로 생성되는 디렉토리는 단수형, 원형 사용을 원칙으로 합니다 (예: `doc`, `model`, `script`, `publish` 등).
- 단, 원본 Reference나 서비스의 기존 구조는 그대로 유지합니다.
