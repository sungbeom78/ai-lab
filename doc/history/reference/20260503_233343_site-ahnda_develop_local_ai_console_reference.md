# 작업 레퍼런스: Local AI Console Execution

- Date: 20260503_233343
- Project: site-ahnda
- Mode: develop
- Model: qwen2.5-coder:7b
- Task: ahnda.com 정적 MVP 웹페이지를 지금 바로 구현해라.

목표:
어설퍼도 좋으니 웹페이지가 실제로 떠야 한다.
이번 작업의 최우선 목표는 /project/site/ahnda/index.html 이 브라우저에서 정상적으로 보이는 것이다.

중요:
- 모든 사용자-facing 문구는 한국어로 작성한다.
- 이번 작업은 설계가 아니라 실제 구현이다.
- 반드시 파일을 생성하거나 수정한다.
- 단, 허용된 범위 밖은 수정하지 않는다.
- /project/site/ahnda 하위만 수정 가능하다.
- /project/site/bomts 수정 금지.
- /project/bomts-ai 수정 금지.
- /project/lostway 수정 금지.
- git commit/push 금지.
- systemd, Cloudflare, firewall, portproxy, SSH 설정 수정 금지.
- .env, secret, token, API key 생성/수정/출력 금지.
- rm -rf 사용 금지.
- 외부 CDN 사용 금지.
- 외부 API 사용 금지.

먼저 할 일:
1. /project/site/ahnda 디렉토리가 있는지 확인한다.
2. 없다면 생성한다.
3. 기존 index.html이 있으면 내용을 확인한다.
4. 기존 index.html이 의미 있는 파일이면 백업한다.
   백업 파일명:
   index.html.bak_YYYYMMDD_HHMMSS
5. 기존 파일이 비어 있거나 테스트 파일이면 그대로 덮어써도 된다.

반드시 생성할 파일:

/project/site/ahnda/index.html
/project/site/ahnda/assets/css/style.css
/project/site/ahnda/assets/js/app.js
/project/site/ahnda/data/schedule.json
/project/site/ahnda/data/work_log.json
/project/site/ahnda/data/memo.json
/project/site/ahnda/data/study.json

웹페이지 내용:
ahnda 개인 작업실 MVP를 만든다.

페이지 제목:
ahnda

부제:
오늘의 일정, 작업 기록, 메모, 스터디를 한 곳에서 정리하는 개인 작업실

필수 섹션:
1. 오늘의 대시보드
2. 일정
3. 작업 로그
4. 메모
5. 스터디 기록

대시보드에는 아래 카드 4개를 표시한다.
- 오늘 일정
- 최근 작업
- 최근 메모
- 최근 스터디

각 카드에는 JSON 데이터에서 읽은 요약을 표시한다.

Schedule에는 schedule.json 데이터를 표시한다.
Work Log에는 work_log.json 데이터를 표시한다.
Memo에는 memo.json 데이터를 표시한다.
Study에는 study.json 데이터를 표시한다.

디자인:
- 어두운 배경
- 카드형 UI
- 모바일에서도 보기 좋게 1열로 변환
- 데스크탑에서는 카드가 2~4열로 보이게 한다
- 너무 복잡하지 않게 한다
- 보기 좋게 여백과 border-radius를 적용한다

JavaScript:
- app.js에서 fetch로 data/*.json 파일을 읽는다.
- DOMContentLoaded 후 실행한다.
- 데이터 로딩 실패 시 화면에 오류 메시지를 표시한다.
- innerHTML 사용 시 escapeHtml을 적용한다.
- 외부 라이브러리 사용 금지.

샘플 데이터:
각 JSON 파일에는 최소 3개 항목을 작성한다.
실제 IP, 계정명, 비밀번호, token, API key, secret은 절대 넣지 않는다.

검증:
작업 후 반드시 아래 명령을 실행한다.

1. 파일 생성 확인:
find /project/site/ahnda -maxdepth 3 -type f | sort

2. JSON 문법 확인:
python -m json.tool /project/site/ahnda/data/schedule.json > /dev/null
python -m json.tool /project/site/ahnda/data/work_log.json > /dev/null
python -m json.tool /project/site/ahnda/data/memo.json > /dev/null
python -m json.tool /project/site/ahnda/data/study.json > /dev/null

3. 민감 정보 후보 확인:
grep -RInE "api_key|apikey|token|secret|password|passwd" /project/site/ahnda || true

4. 정적 서버 실행 테스트:
cd /project/site/ahnda
python -m http.server 18080

단, 서버 실행은 테스트용이다.
이미 서비스 서버가 있다면 별도 서버 실행은 생략해도 된다.
실행 가능하면 브라우저 확인 URL은 다음과 같다.
http://localhost:18080

작업 기록:
아래 기록을 생성한다.

- /project/ai-hub/doc/history/session/YYYYMMDD_HHMMSS_site-ahnda_static_mvp_session.md
- /project/ai-hub/doc/publish-source/ahnda/YYYYMMDD_HHMMSS_site_ahnda_static_mvp_log.md
- /project/ai-hub/doc/reference/bomts/YYYYMMDD_HHMMSS_site_ahnda_static_mvp_reference.md
- /project/ai-hub/doc/publish-source/bomts/YYYYMMDD_HHMMSS_site_ahnda_static_mvp_publish.md

완료 후 보고:
1. 기존 /project/site/ahnda 상태
2. 백업한 파일 목록
3. 생성한 파일 목록
4. 수정한 파일 목록
5. 구현된 화면 섹션
6. JSON 문법 확인 결과
7. 민감 정보 점검 결과
8. 정적 서버 테스트 결과
9. 브라우저 확인 URL
10. 생성된 작업 기록 경로
11. 남은 제한사항
12. 다음 작업 제안

중요:
이번 작업은 “일단 웹페이지가 뜨는 것”이 최우선이다.
완벽하지 않아도 된다.
단, index.html이 실제로 보이고, CSS/JS/JSON이 연결되어야 한다.
- Output: /project/ai-hub/out/local-ai-job/20260503_233343_site-ahnda_develop_qwen2_5-coder_7b_result.md

## Summary
Local AI Web Console executed the task successfully.

## Next Action
Review the output file and validate proposed code or commands.

## Security Notice
- Replaced IPs with <IP>
- Replaced ports with <PORT>
- Replaced users with <USER>
