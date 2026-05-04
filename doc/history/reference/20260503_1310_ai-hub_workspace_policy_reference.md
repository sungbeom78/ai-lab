# 작업 레퍼런스: AI Hub 작업 이력 분리 구조 재현

- Date: 2026-05-03
- Project: ai-hub
- Area: Architecture & Policy
- Environment: WSL2 / AI Hub
- Status: Completed
- Visibility:
  - [x] Internal
  - [ ] Publish Candidate
  - [ ] Published

## 1. 목적
AI Hub 환경에서 수행된 작업의 이력을 단순 로그가 아닌 목적별(개인 회고용 ahnda.com, 기술 레퍼런스용 bomts.net)로 분리하고 이를 자동화하는 구조를 세팅합니다.

## 2. 대상 환경
```text
OS: Ubuntu 24.04 (WSL2)
Host: Windows 11
Local Path: /project/ai-hub
Related Domain: ahnda.com, bomts.net
```

## 3. 사전 조건
- `/project/ai-hub` 공통 작업 디렉토리 존재
- 시스템 및 태스크 프롬프트 기본 구조 존재

## 4. 작업 순서

### 4.1 작업 이력 디렉토리 구조화

```bash
mkdir -p /project/ai-hub/doc/history/session
mkdir -p /project/ai-hub/doc/history/event
mkdir -p /project/ai-hub/doc/history/decision
mkdir -p /project/ai-hub/doc/history/error
mkdir -p /project/ai-hub/doc/reference/bomts
mkdir -p /project/ai-hub/doc/publish-source/ahnda
mkdir -p /project/ai-hub/doc/publish-source/bomts
```

설명:
이 작업에 필요한 내부 원장용(`history`), 기술 원본 레퍼런스용(`reference`), 게시 초안용(`publish-source`) 디렉토리를 일괄 생성합니다.

확인:
```bash
ls -la /project/ai-hub/doc/history
ls -la /project/ai-hub/doc/reference
ls -la /project/ai-hub/doc/publish-source
```

정상 결과 예시:
`session`, `bomts`, `ahnda` 등 각 하위 디렉토리가 표시됨.

### 4.2 템플릿 생성
다음 3종의 마크다운 템플릿을 `/project/ai-hub/prompt/task/` 하위에 작성합니다.
- `ahnda_publish_template.md`
- `bomts_reference_template.md`
- `session_log_template.md`

### 4.3 시스템 지침 파일(`ai_hub_work_start.md`) 수정
작업 완료 시 반드시 3대 필수 기록을 남기도록 `ai_hub_work_start.md`에 정책(Section 8)을 추가합니다.

필수 3대 기록:
1. `history/session`: 작업 세션 전체 기록
2. `publish-source/ahnda`: 개인 작업 로그 초안
3. `reference/bomts` (또는 `publish-source/bomts`): 재현 가능한 기술 레퍼런스

## 5. 설정 파일

파일: `/project/ai-hub/prompt/system/ai_hub_work_start.md`
내용 (추가된 정책 일부):
```text
### 8.3 작업 완료 시 3대 필수 기록
작업이 완료되면 항상 아래 3개의 이력을 남겨야 합니다.
1. `history/session`: 작업 세션 전체 기록 (내부 작업 원장)
2. `publish-source/ahnda`: 개인 작업 로그 초안 (ahnda용)
3. `reference/bomts` 또는 `publish-source/bomts`: 재현 가능한 기술 레퍼런스 (bomts용)
```

## 6. 검증 방법

```bash
cat /project/ai-hub/prompt/system/ai_hub_work_start.md | grep "3대 필수 기록"
```

정상 기준: 해당 문자열이 시스템 프롬프트 상에 명확히 표기되어 출력되어야 함.

## 7. 오류와 대응

| 증상 | 원인 | 대응 |
| -- | -- | -- |
| 디렉토리 생성 실패 | `/project/ai-hub/doc` 권한 부재 | 권한(`chmod` 또는 `chown`) 재확인 후 `mkdir` 재시도 |

## 8. 보안 주의사항
- 실제 IP, 계정명, 포트, 비밀번호, API key, token, secret은 반드시 placeholder로 치환한다.
- (예: `<IP>`, `<PORT>`, `<USER>`)

## 9. 재작업 체크리스트
* [x] 사전 조건 확인
* [x] 디렉토리 생성
* [x] 설정 파일 작성
* [x] 명령 실행
* [x] 상태 확인
* [x] 보안 정보 치환 확인
* [x] 게시 전 민감 정보 검토

## 10. 관련 기록
```text
history/session: /project/ai-hub/doc/history/session/20260503_1310_ai-hub_first_order_job_session.md
publish-source/ahnda: /project/ai-hub/doc/publish-source/ahnda/20260503_1310_ai-hub_workspace_policy.md
publish-source/bomts: /project/ai-hub/doc/publish-source/bomts/20260503_1310_ai-hub_workspace_policy.md
```
