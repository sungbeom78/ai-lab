# 기술 블로그 초안: Local AI Console Execution

- Date: 20260503_232910
- Project: site-ahnda
- Mode: develop
- Model: qwen2.5-coder:7b
- Task: ahnda.com 개인 작업 관리 MVP를 실제로 구현해라.

중요:
- 모든 응답과 사용자-facing 문구는 한국어로 작성해라.
- 코드, 파일명, 경로, HTML class name, JavaScript variable name은 영어를 사용해도 된다.
- 이번 작업은 설계가 아니라 실제 구현 작업이다.
- 단, 지정된 범위 밖은 절대 수정하지 마라.
- git commit/push 하지 마라.
- systemd, Cloudflare, firewall, portproxy, SSH 설정은 수정하지 마라.
- .env, secret, token, API key는 생성/수정/출력하지 마라.
- rm -rf 사용 금지.

작업 목표:
ahnda.com에 개인 작업 관리 MVP를 만든다.
이 MVP는 일정, 작업 로그, 메모, 스터디 기록을 한 화면에서 확인할 수 있는 정적 웹페이지다.

이번 구현의 핵심:
- 눈에 보이는 결과물을 만든다.
- 복잡한 서버/DB/로그인 기능은 만들지 않는다.
- 정적 HTML/CSS/JavaScript + JSON 샘플 데이터 기반으로 구현한다.
- 사용자가 매일 열어보고 “오늘 뭐 하지?”, “최근 뭐 했지?”, “공부는 어디까지 했지?”를 확인할 수 있어야 한다.
- 모바일에서도 보기 좋게 만든다.

수정 허용 범위:
- /project/site/ahnda 하위 파일 생성/수정 가능
- 단, 기존 파일이 있다면 삭제하지 말고 먼저 백업하거나 내용을 확인한 뒤 최소 수정한다.
- /project/ai-hub/doc/history/session 기록 생성 가능
- /project/ai-hub/doc/publish-source/ahnda 기록 생성 가능
- /project/ai-hub/doc/reference/bomts 기록 생성 가능
- /project/ai-hub/doc/publish-source/bomts 기록 생성 가능

수정 금지:
- /project/bomts-ai 수정 금지
- /project/lostway 수정 금지
- /project/site/bomts 수정 금지
- /project/site/ahnda 이외의 site 경로 수정 금지
- Windows/WSL 시스템 설정 수정 금지

먼저 확인할 것:
1. /project/site/ahnda 디렉토리가 존재하는지 확인한다.
2. 현재 파일 목록을 확인한다.
3. 기존 index.html이 있으면 내용을 확인한다.
4. 기존 파일을 덮어쓸 필요가 있으면, 먼저 같은 디렉토리에 backup 파일을 만든다.
   예:
   index.html.bak_YYYYMMDD_HHMMSS
5. 기존 파일이 거의 비어 있거나 초기 상태라면 그대로 수정해도 된다.

구현할 파일 구조:

/project/site/ahnda
  ├─ index.html
  ├─ assets
  │   ├─ css
  │   │   └─ style.css
  │   └─ js
  │       └─ app.js
  └─ data
      ├─ schedule.json
      ├─ work_log.json
      ├─ memo.json
      └─ study.json

각 파일 역할:

1. index.html
- 전체 페이지 구조
- 대시보드 영역
- 일정 영역
- 작업 로그 영역
- 메모 영역
- 스터디 영역
- 모바일 대응 meta viewport 포함
- assets/css/style.css 연결
- assets/js/app.js 연결

2. assets/css/style.css
- 전체 UI 스타일
- 카드형 레이아웃
- 반응형 디자인
- 데스크탑에서는 2~3열 카드 배치
- 모바일에서는 1열 배치
- 너무 화려하지 않게, 깔끔하고 차분한 느낌
- ahnda.com 개인 작업실 느낌
- 다크 모드 느낌의 배경을 기본으로 하되, 가독성 좋은 색 사용
- CSS 변수 사용 권장

3. assets/js/app.js
- JSON 데이터 로딩
- Dashboard 요약 생성
- 일정 목록 렌더링
- 작업 로그 목록 렌더링
- 메모 목록 렌더링
- 스터디 목록 렌더링
- 데이터 로딩 실패 시 사용자에게 오류 메시지 표시
- 모든 화면 문구는 한국어

4. data/schedule.json
- 일정 샘플 데이터

5. data/work_log.json
- 작업 로그 샘플 데이터

6. data/memo.json
- 메모 샘플 데이터

7. data/study.json
- 스터디 기록 샘플 데이터

상세 화면 설계:

페이지 제목:
- ahnda

부제:
- 오늘의 일정, 작업 기록, 메모, 스터디를 한 곳에서 정리하는 개인 작업실

상단 헤더 구성:
- 왼쪽: ahnda
- 오른쪽: 현재 날짜 표시
- 작은 설명 문구:
  “내가 오늘 무엇을 하고, 무엇을 남겼는지 확인하는 공간”

Dashboard 영역:
제목:
- 오늘의 대시보드

카드 4개:
1. 오늘 일정
   - 오늘 날짜에 해당하는 일정 개수 표시
   - 가장 가까운 일정 1개 표시
2. 최근 작업
   - 최근 작업 로그 1개 표시
   - 상태 표시
3. 최근 메모
   - 최근 메모 1개 표시
   - 태그 표시
4. 최근 스터디
   - 최근 스터디 기록 1개 표시
   - 진행 상태 표시

Schedule 영역:
제목:
- 일정

표시 내용:
- 날짜
- 시간
- 제목
- 유형
- 상태
- 메모

Work Log 영역:
제목:
- 작업 로그

표시 내용:
- 작업 일시
- 프로젝트
- 작업 제목
- 상태
- 작업 요약
- 회고
- 관련 링크 또는 파일

Memo 영역:
제목:
- 메모

표시 내용:
- 제목
- 내용
- 태그
- 작성일
- 수정일

Study 영역:
제목:
- 스터디 기록

표시 내용:
- 공부 주제
- 자료명
- 진행 상태
- 정리 내용
- 다음에 볼 내용

JSON 데이터 구조:

schedule.json 예시 구조:
[
  {
    "id": "schedule-001",
    "date": "2026-05-03",
    "time": "09:00",
    "title": "Local AI Console 점검",
    "type": "개발",
    "status": "진행중",
    "memo": "qwen/gemma가 작업 결과를 생성하고 기록하는 흐름 확인"
  }
]

work_log.json 예시 구조:
[
  {
    "id": "work-001",
    "datetime": "2026-05-03 15:30",
    "project": "ai-hub",
    "title": "Local AI Web Console MVP 실행",
    "status": "완료",
    "summary": "Ollama 로컬 모델을 웹에서 호출하고 결과를 파일로 저장하는 콘솔을 실행했다.",
    "reflection": "이제 로컬 AI에게 실제 작업을 맡길 수 있는 첫 단계에 들어섰다.",
    "link": ""
  }
]

memo.json 예시 구조:
[
  {
    "id": "memo-001",
    "title": "AI 작업실 방향",
    "content": "Antigravity는 부트스트랩 도구이고, desktop-ai의 로컬 AI가 실제 개발자가 되는 구조로 간다.",
    "tags": ["AI", "desktop-ai", "작업실"],
    "created_at": "2026-05-03",
    "updated_at": "2026-05-03"
  }
]

study.json 예시 구조:
[
  {
    "id": "study-001",
    "topic": "Local AI Agent",
    "material": "Ollama + qwen2.5-coder",
    "status": "진행중",
    "summary": "로컬 모델을 웹 콘솔에서 호출하고 작업 결과를 저장하는 구조를 실험 중이다.",
    "next": "파일 변경 적용기와 승인 기반 patch 흐름을 설계한다."
  }
]

샘플 데이터는 각 파일마다 최소 3개씩 작성한다.
실제 IP, 계정명, 비밀번호, token, API key, secret은 포함하지 않는다.

index.html 구현 요구사항:
- semantic HTML 사용
- header, main, section 사용
- 각 영역에 id 부여
  - dashboard
  - schedule
  - work-log
  - memo
  - study
- app.js에서 데이터를 삽입할 container 제공
- 데이터 로딩 중 표시 문구 제공
- 데이터가 없을 때 표시할 문구 제공
- footer 포함
  - “ahnda personal workspace”
- 접근성 고려
  - button이나 link가 있으면 aria-label 고려
  - 색상 대비 신경쓰기

style.css 구현 요구사항:
- CSS variables 사용
예:
  --bg
  --panel
  --panel-soft
  --text
  --muted
  --accent
  --border
  --danger
  --success
  --warning
- 전체 배경은 차분한 다크 톤
- 카드 배경은 약간 밝은 톤
- border-radius 사용
- box-shadow는 과하지 않게
- 모바일 대응:
  @media (max-width: 768px)
- 긴 텍스트가 카드 밖으로 넘치지 않게 처리
- 상태 badge 스타일 작성
  - 완료
  - 진행중
  - 예정
  - 보류

app.js 구현 요구사항:
- DOMContentLoaded 후 실행
- fetch로 data/*.json 읽기
- Promise.all 사용 가능
- 실패 시 console.error와 화면 오류 표시
- 날짜 포맷 함수 작성
- 최근 항목 정렬 함수 작성
- 오늘 일정 필터 함수 작성
- 카드 HTML 생성 함수 작성
- XSS 방지를 위해 데이터 삽입 시 escapeHtml 함수 사용
- innerHTML 사용 시 반드시 escapeHtml 적용
- 상태별 badge class 생성 함수 작성

필수 JavaScript 함수 후보:
- escapeHtml(value)
- formatDate(value)
- getTodayDateString()
- sortByDateDesc(items, field)
- getStatusClass(status)
- renderDashboard(data)
- renderSchedule(items)
- renderWorkLogs(items)
- renderMemos(items)
- renderStudies(items)
- renderError(message)
- loadData()

보안 요구사항:
- JSON 데이터는 공개 가능한 샘플만 사용
- 개인 민감 정보는 data/*.json에 넣지 않는다
- 향후 비공개 데이터는 public web root 밖에 둘 수 있도록 README 또는 주석에 언급
- app.js에서 외부 스크립트/CDN 사용 금지
- HTML injection 방지를 위해 escapeHtml 사용
- API key/token/password 같은 단어와 실제 값이 샘플에 들어가지 않게 한다

검증 방법:
작업 후 아래를 수행해라.

1. 파일 목록 확인:
find /project/site/ahnda -maxdepth 3 -type f | sort

2. HTML/CSS/JS 파일 존재 확인:
test -f /project/site/ahnda/index.html
test -f /project/site/ahnda/assets/css/style.css
test -f /project/site/ahnda/assets/js/app.js
test -f /project/site/ahnda/data/schedule.json
test -f /project/site/ahnda/data/work_log.json
test -f /project/site/ahnda/data/memo.json
test -f /project/site/ahnda/data/study.json

3. JSON 문법 확인:
python -m json.tool /project/site/ahnda/data/schedule.json > /dev/null
python -m json.tool /project/site/ahnda/data/work_log.json > /dev/null
python -m json.tool /project/site/ahnda/data/memo.json > /dev/null
python -m json.tool /project/site/ahnda/data/study.json > /dev/null

4. 정적 파일 확인:
grep -RIn "api_key\|token\|secret\|password" /project/site/ahnda || true

5. 간단한 로컬 확인:
가능하면 /project/site/ahnda에서 아래 서버를 실행해 확인한다.
python -m http.server 18080

브라우저:
http://localhost:18080

단, 이미 서비스 서버가 있다면 별도 서버 실행은 생략하고 파일 생성까지만 보고한다.

작업 기록:
이번 작업 후 아래 기록을 생성해라.

1. session 기록:
/project/ai-hub/doc/history/session/YYYYMMDD_HHMMSS_site-ahnda_static_mvp_session.md

2. ahnda 작업 로그:
/project/ai-hub/doc/publish-source/ahnda/YYYYMMDD_HHMMSS_site_ahnda_static_mvp_log.md

3. bomts 기술 레퍼런스:
/project/ai-hub/doc/reference/bomts/YYYYMMDD_HHMMSS_site_ahnda_static_mvp_reference.md

4. bomts 게시 후보:
/project/ai-hub/doc/publish-source/bomts/YYYYMMDD_HHMMSS_site_ahnda_static_mvp_publish.md

각 기록에는 다음을 포함해라:
- 작업 목적
- 생성/수정한 파일
- 데이터 구조
- 검증 결과
- 보안 주의사항
- 다음 작업

완료 후 보고:
1. 현재 /project/site/ahnda 기존 상태
2. 백업한 파일 목록
3. 생성한 파일 목록
4. 수정한 파일 목록
5. 구현한 화면 영역
6. JSON 데이터 구조 요약
7. 보안 처리 내용
8. 검증 명령 실행 결과
9. 로컬 확인 URL
10. 생성된 작업 기록 경로
11. 남은 제한사항
12. 다음 작업 제안

중요:
이번 작업은 실제 ahnda.com MVP 정적 웹페이지를 만드는 작업이다.
설계만 하지 말고 반드시 파일을 생성/수정해라.
단, 허용된 범위 밖은 절대 수정하지 마라.
- Output: /project/ai-hub/out/local-ai-job/20260503_232910_site-ahnda_develop_qwen2_5-coder_7b_result.md

## Summary
Local AI Web Console executed the task successfully.

## Next Action
Review the output file and validate proposed code or commands.

## Security Notice
- Replaced IPs with <IP>
- Replaced ports with <PORT>
- Replaced users with <USER>
