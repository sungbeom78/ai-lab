# [2026-05-05] AI Hub에 OpenClaw 탭 연동 작업

- **시간**: 2026-05-05 16:50
- **대상**: `/project/ai-hub/app/local_ai_console/`
- **지침**: 사용자 추가 요청 - "AI Hub 웹 페이지에 OpenClaw 대화 탭 연동"

## 작업 목표
AI Hub(11004) 웹 UI 내에 OpenClaw Bridge Server(11006)와 연동되는 상태 패널 및 접속 링크를 제공하는 탭을 신규 추가.

## 실행 내역
1. **API 추가**: `/api/openclaw/config` 엔드포인트를 `main.py`에 추가하여, 서버에서 설정된 `OPENCLAW_WEB_URL`과 `OPENCLAW_API_URL`을 프론트엔드로 전달하도록 구성.
2. **UI 탭 추가**: `index.html` 좌측 사이드바에 "🤖 OpenClaw Chat" 메뉴 아이템 추가 및 관련 `tab-content` 영역 구성.
3. **기능 구현**:
   - `app.js`에 `loadOpenClawStatus` 함수 추가.
   - API 설정값을 불러와 UI에 Web/API URL 표시.
   - OpenClaw Bridge Server의 `/api/health` 엔드포인트에 직접 비동기 통신(fetch)하여 상태(API Health, Ollama 연결 여부, Chat/Code 모델 가용성 등)를 확인하고 UI 텍스트 업데이트.
   - "OpenClaw Chat 새 창 열기 ↗" 버튼을 제공하여, 별도의 Web UI나 외부 뷰어로 접근할 수 있도록 동적 링크(href) 연동.
4. **서버 재시작**: AI Hub 서버(PID 46470)를 안전하게 중지하고 백그라운드 데몬 형태로 재기동 완료. (`/tmp/ai-hub-console.log`에서 정상 구동 및 config API 200 OK 응답 확인)

## 변경된 파일 목록
- `/project/ai-hub/app/local_ai_console/main.py`
- `/project/ai-hub/app/local_ai_console/templates/index.html`
- `/project/ai-hub/app/local_ai_console/static/app.js`

## 향후 과제
- 현재는 iframe 임베딩 대신, "새 탭 열기"와 "상태 표시"라는 3순위(대안 B) 형태로 구현됨. 추후 데스크탑 앱 형태의 완벽한 웹 프론트엔드가 생길 경우 iframe `src`로 쉽게 변경 가능.
