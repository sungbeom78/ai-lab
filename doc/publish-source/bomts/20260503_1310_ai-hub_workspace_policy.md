# 작업 레퍼런스: AI Hub 자동화 작업 이력 분리 파이프라인 구축

- Date: 2026-05-03
- Project: ai-hub
- Area: Architecture & Policy
- Environment: WSL2 / AI Hub
- Status: Completed
- Visibility:
  - [ ] Internal
  - [x] Publish Candidate
  - [ ] Published

## 1. 목적
LLM 기반 자율 에이전트(Autonomous Agent)가 수행한 작업 이력을 목적에 맞게 분리(개인 회고용 vs 기술 레퍼런스용)하여 지식 베이스의 품질과 웹 퍼블리싱 효율을 극대화합니다.

## 2. 대상 환경
```text
OS: Ubuntu 24.04 (WSL2)
Host: Windows 11
Local Path: /project/ai-hub
Related Domain: ahnda.com, bomts.net
```

## 3. 사전 조건
- AI Hub 공통 프롬프트 디렉토리(`/project/ai-hub/prompt`) 구성
- 자동 실행 권한 구조 적용 완료

## 4. 작업 순서

### 4.1 템플릿 디렉토리 구조화
```bash
# 기록용 디렉토리 생성 (이전 세션에서 진행됨)
mkdir -p /project/ai-hub/doc/history/{session,event,decision,error}
mkdir -p /project/ai-hub/doc/publish-source/{ahnda,bomts}
```

### 4.2 시스템 프롬프트 업데이트
`ai_hub_work_start.md`의 Section 8을 업데이트하여 에이전트가 작업 완료 시 반드시 3종의 문서를 남기도록 강제 지침을 주입합니다.

## 5. 설정 파일
생성된 핵심 템플릿들:
- `/project/ai-hub/prompt/task/ahnda_publish_template.md`
- `/project/ai-hub/prompt/task/bomts_reference_template.md`
- `/project/ai-hub/prompt/task/session_log_template.md`

## 6. 검증 방법
에이전트가 작업을 마칠 때 지정된 `publish-source` 경로에 템플릿에 맞춘 마크다운 파일이 자동 생성되는지 확인합니다.

## 7. 오류와 대응
- 현재 시스템 정책 파일 수정 중 발생한 오류 없음.

## 8. 보안 주의사항
- 본 기술 레퍼런스 작성 시, 실제 서버의 IP, Port, 계정명 등은 반드시 `<IP>`, `<PORT>`, `<USER>` 형태로 치환하여 기록하도록 프롬프트에 명시했습니다.

## 9. 재작업 체크리스트
* [x] 사전 조건 확인
* [x] 디렉토리 생성
* [x] 설정 파일(템플릿) 작성
* [x] 명령 실행(프롬프트 업데이트)
* [x] 보안 정보 치환 확인
* [x] 게시 전 민감 정보 검토

## 10. 관련 기록
```text
history/session: 20260503_1310_ai-hub_first_order_job_session.md
publish-source/ahnda: 20260503_1310_ai-hub_workspace_policy.md
publish-source/bomts: 20260503_1310_ai-hub_workspace_policy.md
```
