# Local AI Web Console

## 목적
desktop-ai 내부의 Ollama 로컬 모델을 CLI가 아닌 웹에서 편리하게 실행하고, 결과와 이력을 자동으로 파일로 남기기 위한 MVP 콘솔입니다.

## 실행 방법
```bash
/project/ai-hub/script/run_local_ai_console.sh
```

## 접속 정보
- **URL**: http://localhost:11004
- **API Endpoint**: 
  - `GET /api/health`
  - `GET /api/models`
  - `POST /api/jobs`
  - `GET /api/jobs`

## 출력 위치
- **작업 결과 (Markdown/JSON)**: `/project/ai-hub/out/local-ai-job`
- **Session 기록**: `/project/ai-hub/doc/history/session`
- **Ahnda 로그**: `/project/ai-hub/doc/publish-source/ahnda`
- **BomTS 기술 레퍼런스**: `/project/ai-hub/doc/reference/bomts`
- **BomTS 게시 후보**: `/project/ai-hub/doc/publish-source/bomts`

## Dry-run 사용법
웹 UI에서 `Dry Run (No Ollama Call)` 체크박스를 활성화한 뒤 Run을 누르면, 실제 Ollama 모델 추론 대기 없이 최종 조립된 Prompt 텍스트만 생성되어 파일로 저장됩니다. 프롬프트 구조 검증 시 유용합니다.

## 현재 제한사항
- 실제 프로젝트 소스 코드(`/project/site`, `/project/bomts-ai` 등)를 AI가 자동으로 수정하는 기능은 구현되지 않았습니다. (읽기 전용 MVP)
- 외부 API(OpenAI 등)는 지원하지 않으며 오직 localhost의 Ollama 환경만 연결됩니다.

## 다음 개선 방향
- 작업 결과로 도출된 코드를 클릭 한 번에 실제 파일로 패치(patch)하는 자동화 연동
- Job 결과 Markdown을 웹 화면에서 더 예쁘게 보여주는 렌더링 기능 추가
