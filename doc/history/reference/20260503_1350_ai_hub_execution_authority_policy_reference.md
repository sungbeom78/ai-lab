# 작업 레퍼런스: AI Hub 위험도 기반 실행 권한 체계 구축

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
자율 에이전트(Autonomous Agent)의 역할을 단순 보조에서 '실질적 개발/운영 수행자'로 격상시키되, 시스템 안정성을 지키기 위한 위험도 기반(Risk-based) 권한 통제 체계를 도입합니다.

## 2. 대상 환경
```text
OS: Ubuntu 24.04 (WSL2)
Host: Windows 11
Local Path: /project/ai-hub
Related Domain: ahnda.com, bomts.net
```

## 3. 사전 조건
- AI Hub 프롬프트 시스템(`/project/ai-hub/prompt/system`) 구성 완료
- 이전 단계의 이력 분리 파이프라인(session, ahnda, bomts) 세팅 완료

## 4. 작업 순서

### 4.1 시스템 정책(ai_hub_work_start.md) 업데이트
```bash
# 에이전트 내부 프롬프트 파일 수정
vi /project/ai-hub/prompt/system/ai_hub_work_start.md
```
설명: 파일 내부의 "Read-Only Analysis" 등 임시 안전 모드를 완전한 "Work Modes"와 "권한 티어"로 대체합니다.

## 5. 설정 파일
적용된 핵심 정책은 다음과 같습니다.

### 5.1 AI Work Modes (작업 모드)
- **Inspect**: 읽기/분석
- **Prepare**: 계획/문서/지침 작성
- **Develop**: 개발용 코드 수정
- **Validate**: 테스트/검증
- **Operate**: 운영 상태 점검/로그 분석
- **Release**: 배포/커밋/운영 반영 (승인 필요)

### 5.2 권한 티어 (Authority Tiers)
1. **Auto Allowed**: 읽기, 문서화, 환경 점검 자동 실행
2. **Development Allowed**: 개발 코드 수정, 빌드 자동 실행
3. **Approval Required**: 운영 반영(정적 문서 포함), Git 커밋, 방화벽 수정
4. **Strong Approval Required**: 실거래/API 키/계좌 연동, `site` 직접 수정
5. **Forbidden**: 승인 없는 파괴(rm -rf), 권한 임의 변경

### 5.3 프로젝트별 맞춤 정책
- **/project/bomts-ai**: 개발 대상. 코드 수정 자유, 실거래/API 키 등만 승인 필요.
- **/project/lostway**: 분석/개발 대상. 작업 계획 선행 후 코드 수정 가능. 운영 서비스 변경은 승인 필요.
- **/project/site**: 운영 사이트 루트. 원칙상 계획 선행 및 모든 수정 시 철저한 승인 필요.

## 6. 검증 방법
```bash
cat /project/ai-hub/prompt/system/ai_hub_work_start.md | grep "Development Allowed"
```
정상 기준: 시스템 프롬프트에 새로운 권한 티어가 정상적으로 출력되어야 합니다.

## 7. 오류와 대응
| 증상 | 원인 | 대응 |
| -- | -- | -- |
| AI가 여전히 개발 코드 수정 시 승인을 요청함 | IDE의 Workspace Trust 문제 | 에디터의 `Always Allow` 권한 재확인 |

## 8. 보안 주의사항
- 본 정책 업데이트 작업 중 민감 파일(`.env`, 실제 소스 등)은 직접 건드리지 않았습니다.
- 향후 블로그 게시 시 `<IP>`, `<USER>` 처리가 필수적입니다.

## 9. 재작업 체크리스트
* [x] 사전 조건 확인
* [x] 설정 파일(프롬프트) 작성
* [x] 상태 확인
* [x] 보안 정보 치환 확인
* [x] 게시 전 민감 정보 검토

## 10. 관련 기록
```text
history/session: /project/ai-hub/doc/history/session/20260503_1350_ai_hub_execution_authority_policy_session.md
publish-source/ahnda: /project/ai-hub/doc/publish-source/ahnda/20260503_1350_ai_execution_authority_log.md
publish-source/bomts: /project/ai-hub/doc/publish-source/bomts/20260503_1350_ai_hub_execution_authority_policy.md
```
