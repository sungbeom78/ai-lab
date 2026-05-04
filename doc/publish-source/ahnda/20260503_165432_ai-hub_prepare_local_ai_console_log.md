# 작업 로그: Local AI Console Execution

- Date: 20260503_165432
- Project: ai-hub
- Mode: prepare
- Model: qwen2.5-coder:7b
- Task: Local AI Web Console의 UI와 job result 조회 기능을 개선해라.

중요:
- 모든 응답과 화면에 표시되는 사용자용 문구는 한국어로 작성해라.
- 이번 작업은 /project/ai-hub/app/local_ai_console 하위만 대상으로 한다.
- /project/site, /project/bomts-ai, /project/lostway는 절대 수정하지 마라.
- git commit/push 하지 마라.
- systemd, Cloudflare, firewall, portproxy, SSH 설정은 수정하지 마라.
- .env, secret, token, API key는 생성/수정/출력하지 마라.
- rm -rf 사용 금지.

현재 목표:
Local AI Web Console을 실제 사용하기 편하게 개선한다.

반드시 구현할 기능:

1. Execution Result 복사 기능
- Execution Result 영역의 현재 내용을 복사하는 버튼을 추가해라.
- 버튼 이름은 “결과 복사”로 한다.
- 복사 성공 시 “복사 완료” 메시지를 화면에 표시한다.
- 복사 실패 시 “복사 실패” 메시지를 표시한다.

2. 모델 응답 한국어 출력 강화
- job_context.py에서 모델에게 전달하는 최종 prompt에 아래 규칙을 강하게 추가해라.
  “모든 응답은 한국어로 작성한다.”
  “코드, 파일명, 경로, 명령어는 영어/원문을 유지한다.”
  “사용자에게 보여주는 설명, 요약, 계획, 위험, 다음 작업은 한국어로 작성한다.”
- Local AI Job Result 기본 응답 섹션명은 유지해도 되지만, 각 섹션 내용은 한국어로 작성하도록 지시해라.
- 가능하면 섹션명도 한국어 병기를 추가해라.

3. Recent Jobs 파일 클릭 팝업
- Recent Jobs 목록의 result 파일명을 클릭하면 팝업 모달이 열리게 해라.
- 팝업에는 해당 markdown result 파일 내용이 표시되어야 한다.
- 팝업 제목에는 파일명을 표시한다.
- 팝업에는 닫기 버튼을 추가한다.
- 팝업 바깥을 클릭하거나 ESC를 누르면 닫히게 하면 더 좋다.

4. GitHub 스타일 markdown 렌더링
- Recent Jobs 팝업에서는 markdown 원문을 그대로 pre로만 보여주지 말고, GitHub markdown처럼 보기 좋게 렌더링해라.
- 외부 CDN 사용은 금지한다.
- 외부 라이브러리 설치도 이번 작업에서는 하지 않는다.
- 따라서 최소 markdown renderer를 app.js 안에 직접 구현해라.
- 최소 지원:
  - #, ##, ### heading
  - fenced code block ```
  - inline code
  - bullet list
  - numbered list
  - bold
  - paragraph
- 보안상 HTML escape를 먼저 적용하고, 허용한 markdown 문법만 변환해라.
- script 태그나 임의 HTML이 실행되지 않게 해라.

5. 팝업 markdown 복사 기능
- 팝업 안에 “Markdown 복사” 버튼을 추가해라.
- 렌더링된 HTML이 아니라 원본 markdown 내용을 복사해야 한다.
- 복사 성공/실패 메시지를 표시해라.

6. API 보완
- result markdown 조회 endpoint가 없다면 추가해라.
- endpoint 예시:
  GET /api/jobs/{job_id}
- 또는 기존 구현 방식이 있으면 유지하되 UI와 연결해라.
- 반드시 path traversal 방어를 적용해라.
- /project/ai-hub/out/local-ai-job 하위의 *_result.md 파일만 읽을 수 있게 해라.
- 다른 경로 파일은 읽지 못하게 해라.

수정 대상 후보:
- /project/ai-hub/app/local_ai_console/main.py
- /project/ai-hub/app/local_ai_console/job_context.py
- /project/ai-hub/app/local_ai_console/templates/index.html
- /project/ai-hub/app/local_ai_console/static/app.js
- /project/ai-hub/app/local_ai_console/static/style.css
- /project/ai-hub/app/local_ai_console/README.md

필요한 경우에만 아래 파일을 수정해라.
- /project/ai-hub/app/local_ai_console/output_writer.py

검증:
1. Python syntax check
python -m py_compile /project/ai-hub/app/local_ai_console/*.py

2. 서버 실행
/project/ai-hub/script/run_local_ai_console.sh

3. Health 확인
curl http://localhost:11004/api/health

4. Jobs 목록 확인
curl http://localhost:11004/api/jobs

5. Dry-run job 실행
curl -X POST http://localhost:11004/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder:7b",
    "project": "ai-hub",
    "mode": "prepare",
    "task": "한국어 응답 테스트. Local AI Console의 개선점을 한국어로 요약해라.",
    "dry_run": false,
    "temperature": 0.2
  }'

6. 웹 UI에서 확인
- Execution Result에 한국어 응답이 표시되는지 확인
- “결과 복사” 버튼이 동작하는지 확인
- Recent Jobs 파일 클릭 시 팝업이 열리는지 확인
- 팝업에서 markdown이 보기 좋게 렌더링되는지 확인
- “Markdown 복사” 버튼이 동작하는지 확인

이번 작업 기록:
아래 기록을 생성해라.
- /project/ai-hub/doc/history/session/YYYYMMDD_HHMMSS_ai-hub_local_ai_console_result_viewer_session.md
- /project/ai-hub/doc/publish-source/ahnda/YYYYMMDD_HHMMSS_local_ai_console_result_viewer_log.md
- /project/ai-hub/doc/reference/bomts/YYYYMMDD_HHMMSS_local_ai_console_result_viewer_reference.md
- /project/ai-hub/doc/publish-source/bomts/YYYYMMDD_HHMMSS_local_ai_console_result_viewer_publish.md

완료 후 보고:
1. 수정한 파일 목록
2. 생성한 파일 목록
3. 한국어 응답 강화 반영 위치
4. Execution Result 복사 기능 구현 결과
5. Recent Jobs 팝업 구현 결과
6. Markdown 렌더링 방식
7. Markdown 복사 기능 구현 결과
8. path traversal 방어 방식
9. 검증 명령 실행 결과
10. 웹에서 확인해야 할 사항
11. 남은 제한사항
12. 다음 작업 제안

주의:
이번 작업은 설계 문서만 만들고 끝내지 마라.
반드시 Local AI Web Console의 실제 UI와 API를 개선해라.
단, 수정 범위는 /project/ai-hub/app/local_ai_console 하위와 관련 기록 문서로 제한한다.
- Output: /project/ai-hub/out/local-ai-job/20260503_165432_ai-hub_prepare_qwen2_5-coder_7b_result.md

## Summary
Local AI Web Console executed the task successfully.

## Next Action
Review the output file and validate proposed code or commands.

## Security Notice
- Replaced IPs with <IP>
- Replaced ports with <PORT>
- Replaced users with <USER>
