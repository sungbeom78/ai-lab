# Work Session: Local AI Web Console Phase 2 - Safe Apply

## 1. Summary
- Date: 2026-05-03
- Project: ai-hub / site-ahnda
- Task: Local AI Console 내에 Safe Apply 기능(ahnda 정적 MVP 전용) 추가
- Mode: Develop & Validate

## 2. Actions
- `safe_apply.py` 생성: `/api/apply/site-ahnda-static-mvp/preview` 및 `apply` 엔드포인트 구현.
- 허용 목록(allowlist) 적용 및 경로 탐색, 민감 정보(api_key, password 등), 외부 링크 등 차단 로직 적용.
- 기존 파일이 있을 경우 덮어쓰기 전 `.bak_` 파일로 백업.
- `main.py`에 라우터 등록.
- `index.html`, `app.js`에 UI 적용 (ahnda MVP 미리보기 및 적용 버튼 추가).
- 서비스 재시작 후 `curl`을 통해 미리보기 검증 완료.

## 3. Pending
- 현재 `/project/site/ahnda`에 실제 파일을 생성하기 전 사용자 승인 대기 중.
- 사용자 승인 후 "ahnda MVP 적용" 버튼 또는 `curl -X POST http://localhost:11004/api/apply/site-ahnda-static-mvp` 명령으로 파일 생성 예정.
