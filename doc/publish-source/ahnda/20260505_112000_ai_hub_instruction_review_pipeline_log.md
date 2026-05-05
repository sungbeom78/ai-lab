# AI Hub Instruction Review Pipeline 구축 작업 로그

## 2026-05-05

오늘은 ai-hub에 "Instruction Review Pipeline"을 만들었다.

### 무엇을 했나

ai-hub Local AI Console에 새 탭 2개를 추가하고, 백엔드에 지침 평가 API를 구현했다.

사용자가 개발 지침 초안을 입력하면:
1. Stage 1: 구조 정리 (모호한 표현 제거, 범위 명확화)
2. Stage 2: 실전 개발 검증 (실패 시나리오, API 안전 처리, 로그/검증 보강)
3. Stage 3: 최종 승인 → Developer Request 문서 생성

이제 ahnda.com 개발도, lostway 시뮬레이션도 이 흐름으로 진행한다.
"만들어줘" → ai-hub에 초안 입력 → 평가 → Developer Request → opai 개발자에게 전달.

### 왜 이렇게 만들었나

직접 즉흥적으로 코딩 지시를 내리면 나중에 무엇을 왜 만들었는지 추적하기 어렵다.
ai-hub를 지휘소로 만들어, 모든 개발 지시가 평가를 거쳐 문서화되도록 했다.

### 결과

- 서버: http://localhost:11004 (정상 기동)
- Instruction Review 탭: 초안 입력 → 평가 실행 → 파일 저장 동작 확인
- Developer Requests 탭: 저장된 요청 목록 표시
- sample_drafts 3종 준비: ahnda 캘린더, ahnda 스터디, lostway 시뮬레이션

### 다음

- Google AI 실제 평가 모드 테스트 (API key 입력 후)
- ahnda 캘린더 개발 시작 (ai-hub 통해 opai에게 요청)
