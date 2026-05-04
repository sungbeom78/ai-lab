AI Hub 첫 작업을 시작한다.

목표:
- /project/ai-hub를 공통 AI 작업 허브로 정리한다.
- history / publish-source 구조를 생성한다.
- 자동 실행 중심의 공통 작업 지침을 정리한다.
- 모든 결과를 작업 이력과 게시 원천 글감으로 남긴다.

주의:
- /project/bomts-ai 실제 소스는 수정하지 않는다.
- /project/lostway 실제 소스는 수정하지 않는다.
- /project/site 실제 서비스 소스는 수정하지 않는다.
- systemd, firewall, portproxy, Cloudflare, SSH 보안 설정은 수정하지 않는다.
- git commit/push 하지 않는다.
- .env, secret, API key는 건드리지 않는다.

자동 실행:
- /project 구조 점검
- /project/ai-hub 하위 디렉토리 생성
- prompt/system, prompt/project, prompt/task 구조 확인 및 정리
- doc/history, doc/publish-source 구조 생성
- 템플릿 문서 생성
- 작업 결과 기록

완료 후 보고:
1. 생성/수정한 파일 목록
2. 실행한 명령
3. 확인된 현재 상태
4. 승인 필요로 남겨둔 항목
5. 다음 작업 제안
6. publish-source에 남긴 게시 글감 요약



작업 이력은 **하나로 통합해서 남기는 게 아니라, 목적이 다른 두 종류로 분리**해야 한다.

```text
1. ahnda.com
   → “내가 언제 무엇을 했는지”를 남기는 개인 작업 로그 / 회고 / 일정 기록

2. bomts.net
   → “같은 작업을 다시 재현할 수 있을 정도”의 기술 작업 레퍼런스 / 절차서 / 운영 기록
```

첨부 파일은 `bomts.net` 쪽 레퍼런스에 가까워. WSL 설치, 디렉토리 구성, SSHFS 마운트, Ollama 설치, SSH 서버, 포트포워딩, Antigravity SSH 설정까지 실제 재현 가능한 명령과 순서가 포함되어 있고, 민감 정보는 `<PORT>`, `<IP>`, `<계정명>` 같은 형태로 치환하는 방향이 이미 들어가 있어. 

---

# 작업 이력 정책 v1.1

## 1. ahnda.com용 작업 이력

### 목적

`ahnda.com`에는 기술 절차서가 아니라, 범이가 **언제 무엇을 했는지** 남기면 된다.

느낌은 이거야.

```text
오늘은 AI Hub 작업 환경을 정리했다.
WSL2 Ubuntu에 프로젝트 디렉토리를 잡고,
NUC-main의 lostway/site 경로를 SSHFS로 마운트했다.

아직 GPU 연동과 SSH 보안 설정은 더 확인해야 하지만,
일단 AI가 작업할 수 있는 기본 작업실은 만들어졌다.

나중에 돌아보면 “아, 이때부터 AI 개발 허브를 만들기 시작했지”라고 기억할 수 있을 것 같다.
```

즉, `ahnda.com`은 **내가 뭘 했지? / 그때 무슨 생각이었지? / 어디까지 왔지?** 를 남기는 공간이다.

### ahnda 기록 성격

```text
- 개인 작업 로그
- 작업 일정 기록
- 회고
- 진행 상황 요약
- 감정/판단/맥락 포함 가능
- 명령어 전체를 자세히 남길 필요 없음
- 민감 정보는 당연히 제외
- 너무 기술적으로 빡빡하지 않아도 됨
```

### ahnda용 파일 위치

```text
/project/ai-hub/doc/publish-source/ahnda
```

### ahnda 파일명 예시

```text
20260503_ai_hub_start_log.md
20260503_wsl_ai_workspace_log.md
20260503_antigravity_remote_work_log.md
```

### ahnda 템플릿

```markdown
# 작업 로그: <제목>

- Date:
- Project:
- Category:
- Status:

## 오늘 한 일

## 왜 이 작업을 했나

## 작업하면서 정리된 생각

## 진행 결과

## 남은 일

## 나중에 돌아보면

## 공개 시 주의할 내용
- [ ] IP 제거
- [ ] 계정명 제거
- [ ] 포트 제거
- [ ] 내부 경로 공개 가능 여부 확인
- [ ] 민감 정보 없음 확인
```

---

## 2. bomts.net용 작업 레퍼런스

### 목적

`bomts.net`에는 다시 같은 작업을 할 수 있을 정도의 **작업 레퍼런스**를 남겨야 한다.

첨부 파일 같은 형태가 맞다.

즉, 이런 내용이 들어가야 한다.

```text
- 목적
- 환경
- 사전 조건
- 실제 명령어
- 설정 파일 내용
- 확인 명령
- 정상 결과 예시
- 실패 시 확인할 것
- 보안 주의사항
- 민감 정보 치환 규칙
```

이건 그냥 “오늘 뭐 했다”가 아니라, 나중에 범이나 AI가 다시 보고 **작업을 재현할 수 있는 문서**여야 한다.

### bomts 기록 성격

```text
- 기술 절차서
- 운영 레퍼런스
- 재현 가능한 작업 기록
- 명령어 포함
- 설정 파일 예시 포함
- 검증 방법 포함
- 에러/해결 기록 포함
- 민감 정보는 반드시 placeholder 처리
```

### bomts용 파일 위치

```text
/project/ai-hub/doc/publish-source/bomts
```

또는 레퍼런스 성격이 강하면 별도 보관도 가능하다.

```text
/project/ai-hub/doc/reference/bomts
```

나는 둘을 이렇게 나누는 걸 추천한다.

```text
/project/ai-hub/doc/reference/bomts
  → 실제 작업 레퍼런스 원본

/project/ai-hub/doc/publish-source/bomts
  → bomts.net 게시용으로 다듬은 초안
```

즉,

```text
reference/bomts = 실무 원본
publish-source/bomts = 공개 게시 후보
```

---

# 3. 민감 정보 치환 규칙

bomts.net에 남기는 작업 레퍼런스는 자세해야 하지만, 민감 정보는 절대 그대로 남기면 안 된다.

## 치환 규칙

```text
실제 IP              → <IP>
데스크탑 LAN IP      → <DESKTOP_LAN_IP>
WSL IP              → <WSL_IP>
NUC 서버 IP          → <NUC_IP>
포트                 → <PORT>
계정명               → <USER>
서버 계정명           → <SERVER_USER>
WSL 계정명            → <WSL_USER>
호스트명              → <HOSTNAME>
도메인               → <DOMAIN>
API Key              → <API_KEY>
Token                → <TOKEN>
Password             → <PASSWORD>
Secret               → <SECRET>
SSH key name         → <SSH_KEY_NAME>
이메일               → <EMAIL>
내부 절대경로 중 민감한 것 → <PATH>
```

예시는 이렇게 남긴다.

```bash
ssh -p <PORT> <USER>@<HOSTNAME>
```

```bash
sshfs -p <PORT> <SERVER_USER>@<NUC_HOST>:/project/site /project/site \
  -o reconnect \
  -o ServerAliveInterval=15 \
  -o ServerAliveCountMax=3
```

```powershell
netsh interface portproxy add v4tov4 `
  listenaddress=<DESKTOP_LAN_IP> `
  listenport=<PORT> `
  connectaddress=<WSL_IP> `
  connectport=<PORT>
```

---

# 4. 최종 구조 제안

이제 작업 이력 구조는 이렇게 가면 좋다.

```text
/project/ai-hub/doc/history
  ├─ session
  │   └─ 작업 세션 전체 기록
  ├─ event
  │   └─ 주요 실행 이벤트
  ├─ decision
  │   └─ 구조/정책/설계 결정
  └─ error
      └─ 실패/중단/보류/승인 필요 항목

/project/ai-hub/doc/reference
  └─ bomts
      └─ 재현 가능한 기술 작업 레퍼런스 원본

/project/ai-hub/doc/publish-source
  ├─ ahnda
  │   └─ 개인 작업 로그 / 회고 / 일정형 기록
  └─ bomts
      └─ bomts.net 게시용 기술 레퍼런스 초안
```

이렇게 나누면 깔끔하다.

---

# 5. 작업 후 항상 남길 기록 3종

앞으로 AI가 작업을 하면 항상 3개 관점으로 남기면 된다.

## 1) session 기록

위치:

```text
/project/ai-hub/doc/history/session
```

목적:

```text
이번 작업 전체 기록
```

내용:

```text
- 목표
- 수행한 작업
- 수정한 파일
- 실행한 명령
- 결과
- 보류 사항
- 다음 작업
```

## 2) ahnda용 로그

위치:

```text
/project/ai-hub/doc/publish-source/ahnda
```

목적:

```text
내가 언제 무엇을 했는지 기억하기 위한 글감
```

내용:

```text
- 오늘 한 일
- 왜 했는지
- 어디까지 되었는지
- 느낀 점
- 다음에 할 일
```

## 3) bomts용 레퍼런스

위치:

```text
/project/ai-hub/doc/reference/bomts
/project/ai-hub/doc/publish-source/bomts
```

목적:

```text
다시 같은 작업을 할 수 있는 기술 레퍼런스
```

내용:

```text
- 작업 목적
- 환경
- 명령어
- 설정 파일
- 확인 방법
- 에러 대응
- 민감 정보 치환
```

---

# 6. Antigravity 지침에 추가할 내용

아래 내용을 기존 지침에 추가하면 된다.

```text
작업 이력은 목적에 따라 ahnda용 로그와 bomts용 레퍼런스로 분리한다.

1. ahnda.com용 기록

ahnda.com에는 “내가 언제 무엇을 했는지”를 남기는 개인 작업 로그를 작성한다.
기술 절차를 완전히 재현할 수 있을 정도로 자세할 필요는 없다.
작업 일정, 진행 상황, 판단, 회고, 당시 생각을 남기는 것이 목적이다.

저장 위치:
/project/ai-hub/doc/publish-source/ahnda

작성 기준:
- 오늘 무엇을 했는지
- 왜 했는지
- 어디까지 진행됐는지
- 어떤 판단을 했는지
- 다음에 무엇을 할지
- 나중에 돌아봤을 때 기억할 만한 내용

2. bomts.net용 기록

bomts.net에는 같은 작업을 다시 재현할 수 있을 정도의 작업 레퍼런스를 작성한다.
명령어, 설정 파일, 확인 방법, 정상 결과, 실패 대응을 포함한다.
단, IP, 계정명, 비밀번호, 포트, 토큰, API key, 내부 민감 정보는 반드시 placeholder로 치환한다.

저장 위치:
원본 레퍼런스:
/project/ai-hub/doc/reference/bomts

게시 후보:
/project/ai-hub/doc/publish-source/bomts

작성 기준:
- 작업 목적
- 대상 환경
- 사전 조건
- 실제 명령어
- 설정 파일 예시
- 확인 명령
- 정상 결과 예시
- 오류 발생 시 확인할 것
- 보안 주의사항
- 민감 정보 치환 여부

민감 정보 치환 규칙:
- 실제 IP → <IP>
- 데스크탑 LAN IP → <DESKTOP_LAN_IP>
- WSL IP → <WSL_IP>
- NUC 서버 IP → <NUC_IP>
- 포트 → <PORT>
- 계정명 → <USER>
- 서버 계정명 → <SERVER_USER>
- WSL 계정명 → <WSL_USER>
- 비밀번호 → <PASSWORD>
- API Key → <API_KEY>
- Token → <TOKEN>
- Secret → <SECRET>
- 이메일 → <EMAIL>
- 민감한 내부 경로 → <PATH>

작업 완료 시 최소 3개 기록을 남긴다.
1. history/session: 작업 세션 전체 기록
2. publish-source/ahnda: 개인 작업 로그 초안
3. reference/bomts 또는 publish-source/bomts: 재현 가능한 기술 레퍼런스
```

---

# 7. bomts.net 작업 레퍼런스 템플릿

````markdown
# 작업 레퍼런스: <작업 제목>

- Date:
- Project:
- Area:
- Environment:
- Status:
- Visibility:
  - [ ] Internal
  - [ ] Publish Candidate
  - [ ] Published

## 1. 목적

이 작업을 수행한 목적을 적는다.

## 2. 대상 환경

```text
OS:
Host:
WSL:
Server:
Local Path:
Remote Path:
Related Domain:
````

민감 정보는 반드시 placeholder로 작성한다.

## 3. 사전 조건

```text
- 필요한 패키지
- 필요한 권한
- 필요한 디렉토리
- 필요한 SSH 접속
- 필요한 서비스 상태
```

## 4. 작업 순서

### 4.1 <단계 제목>

```bash
명령어
```

설명:

```text
이 명령이 하는 일
```

확인:

```bash
확인 명령어
```

정상 결과 예시:

```text
정상 출력 예시
```

## 5. 설정 파일

파일:

```text
<설정 파일 경로>
```

내용:

```bash
설정 내용
```

## 6. 검증 방법

```bash
검증 명령어
```

정상 기준:

```text
어떤 결과가 나오면 정상인지
```

## 7. 오류와 대응

| 증상 | 원인 | 대응 |
| -- | -- | -- |
|    |    |    |

## 8. 보안 주의사항

```text
- IP는 <IP>로 치환
- 계정명은 <USER>로 치환
- 포트는 <PORT>로 치환
- 비밀번호/API key/token은 절대 기록하지 않음
```

## 9. 재작업 체크리스트

* [ ] 사전 조건 확인
* [ ] 디렉토리 생성
* [ ] 설정 파일 작성
* [ ] 명령 실행
* [ ] 상태 확인
* [ ] 보안 정보 치환 확인
* [ ] 게시 전 민감 정보 검토

## 10. 관련 기록

```text
history/session:
publish-source/ahnda:
publish-source/bomts:
```

````

---

# 8. ahnda.com 작업 로그 템플릿

```markdown
# 작업 로그: <작업 제목>

- Date:
- Project:
- Type:
- Status:

## 오늘 한 일

## 왜 이 작업을 했나

## 진행하면서 든 생각

## 결과

## 아쉬운 점 / 남은 문제

## 다음에 할 일

## 나중에 돌아보면

## 게시 전 확인

- [ ] IP 없음
- [ ] 계정명 없음
- [ ] 포트 없음
- [ ] 비밀번호/API key/token 없음
- [ ] 공개해도 되는 내용만 포함
````

---

# 9. 정리하면

이제 방향은 이렇게 확정하면 된다.

```text
ahnda.com
= 범이의 작업 일지
= “내가 뭘 했지?”
= 일정, 회고, 진행 상황, 기억용 기록

bomts.net
= 기술 작업 레퍼런스
= “이 작업을 다시 하려면 어떻게 해야 하지?”
= 명령어, 설정, 검증, 오류 대응, 보안 치환 포함
```

그리고 아주 중요하게:

```text
history/session은 내부 작업 원장
publish-source/ahnda는 개인 작업 로그 초안
reference/bomts는 기술 레퍼런스 원본
publish-source/bomts는 공개용 기술 글 초안
```

이렇게 가면 된다.

이제 Antigravity 지침은 기존보다 훨씬 좋아진다.
“모든 작업 이력을 남겨라”가 아니라,

> **개인 회고용 로그와 기술 재현용 레퍼런스를 분리해서 남겨라.**

이렇게 명확해졌어.


**************** 이하는 참고사항 ****************

이 프로젝트는 On-Premise AI Hub 구축 프로젝트다.

목표는 AI가 여러 프로젝트를 스스로 개발, 관리, 검증, 개선할 수 있는 작업 허브를 만드는 것이다.
단, AI가 임의로 위험한 작업을 수행해서는 안 된다.
기본 원칙은 “안전한 작업은 자동 실행, 위험한 작업은 승인 요청, 모든 작업은 이력으로 남김”이다.

현재 작업 환경은 다음과 같다.

/project
  ├─ ai-hub      # 모든 프로젝트 공통 AI 작업 허브
  ├─ bomts-ai    # BomTS 관련 작업 영역
  ├─ doc
  ├─ publish     # 게시 후보 산출물 저장소. 실제 서비스 루트 아님
  ├─ log
  ├─ script
  ├─ lostway     # NUC-main:/project/lostway SSHFS 마운트
  ├─ site        # NUC-main:/project/site SSHFS 마운트
  ├─ model
  ├─ rag-index
  └─ runtime

/project/site
  ├─ ahnda       # www.ahnda.com 실제 서비스 루트
  └─ bomts       # www.bomts.com 또는 www.bomts.net 실제 서비스 루트

중요 경로 원칙:
- /project/ai-hub는 공통 AI 작업 허브다.
- /project/publish는 게시 후보 산출물 저장소이며 실제 서비스 루트가 아니다.
- /project/site/ahnda와 /project/site/bomts는 실제 서비스 루트다.
- /project/lostway와 /project/site는 원격 마운트 경로이므로 실제 소스 수정 전 승인 필요하다.
- BomTS는 거래 시스템이므로 실제 소스, 설정, API key, 주문 관련 작업은 반드시 승인 필요하다.

AI Hub 지침 구조는 다음을 사용한다.

/project/ai-hub/prompt
  ├─ system
  │   └─ ai_hub_work_start.md
  ├─ project
  │   ├─ bomts_work_start.md
  │   └─ lostway_work_start.md
  └─ task
      ├─ common_task_start_template.md
      ├─ bomts_task_start_template.md
      └─ lostway_task_start_template.md

디렉토리 명명 원칙:
- AI Hub 자체 디렉토리는 단수형/원형을 사용한다.
- 예: doc, log, model, script, prompt, task, system, project, config, out, plan, history, event, decision, error

기본 실행 정책:
- 가능한 작업은 사용자의 추가 확인 없이 자동 실행한다.
- 단, 위험 작업은 반드시 사전 승인 요청한다.
- 승인 요청 시에는 “왜 위험한지”, “무엇을 바꾸는지”, “되돌릴 수 있는지”를 짧게 설명한다.
- 애매하면 먼저 읽기/점검/mock 검증까지만 자동 실행하고, 실제 변경 직전에 승인 요청한다.

자동 실행 허용:
- pwd, ls, find, tree, readlink, mountpoint, df, lsblk, hostname, ip addr
- grep, sed, cat, head, tail
- python3 --version, python --version, pip --version
- git --version, ssh -V
- ollama --version
- curl http://localhost:11434/api/tags
- /project/script/check_lostway_mount.sh
- /project/script/check_site_mount.sh
- /project/ai-hub 하위 문서, 지침, config, prompt 생성 및 수정
- /project/ai-hub 하위 history, publish-source 구조 생성
- 경로 오타 수정
- reference root 경로 통일
- 공통 지침과 프로젝트별 지침 분리
- Python syntax check
- import check
- mock test
- Ollama local API test
- model routing mock test
- search policy mock test
- 작업 결과 요약 문서 생성
- 게시 후보 원천 글감 생성

승인 필요:
- rm -rf
- 기존 디렉토리 삭제
- 대량 파일 삭제
- git reset --hard
- git clean
- apt install
- curl | sh
- systemd/service 변경
- Windows 방화벽 변경
- portproxy 실제 등록/삭제
- SSH 보안 완화
- Cloudflare Tunnel 설정 변경
- Ollama 11434 LAN/인터넷 공개
- secret/token/API key 저장 또는 출력
- .env 생성/수정
- 외부 API 실제 호출 키 설정
- /project/bomts-ai 실제 소스 수정
- /project/lostway 실제 소스 수정
- /project/site 실제 사이트 소스 수정
- NUC-main 서비스 파일 수정
- commit, push, merge, rebase, tag, release
- 대형 모델 pull
- 새 DB/벡터DB 설치
- 장시간 실행 작업
- 대량 파일 인덱싱
- 실거래, 실주문, 계좌, 투자 판단에 영향을 줄 수 있는 작업

작업 이력 저장 정책:
모든 작업은 나중에 www.ahnda.com, www.bomts.com 또는 www.bomts.net에 게시할 수 있는 글감으로 재사용 가능해야 한다.

다음 디렉토리를 생성하고 유지한다.

/project/ai-hub/doc/history
/project/ai-hub/doc/history/session
/project/ai-hub/doc/history/event
/project/ai-hub/doc/history/decision
/project/ai-hub/doc/history/error
/project/ai-hub/doc/publish-source
/project/ai-hub/doc/publish-source/ahnda
/project/ai-hub/doc/publish-source/bomts

각 디렉토리 의미:
- history/session: 작업 세션별 전체 진행 기록
- history/event: 주요 실행 이벤트, 명령, 결과 기록
- history/decision: 구조, 정책, 설계 결정 기록
- history/error: 실패, 중단, 보류, 승인 필요 항목 기록
- publish-source/ahnda: ahnda.com 게시용 원천 글감
- publish-source/bomts: bomts.com 또는 bomts.net 게시용 원천 글감

작업을 시작할 때마다 세션 기록을 생성하거나 갱신한다.
파일명은 가능하면 다음 형식을 사용한다.

YYYYMMDD_HHMM_<project>_<task_name>_session.md

작업 세션 기록 포맷:

# Work Session: <task name>

## 1. Summary
- Date:
- Project:
- Task:
- Actor:
- Mode:
- Status:

## 2. Goal

## 3. Context

## 4. Actions
| Step | Command / Action | Result | Note |
|---|---|---|---|

## 5. Files Created / Updated
| File | Change |
|---|---|

## 6. Decision
| Decision | Reason |
|---|---|

## 7. Error / Pending
| Item | Reason | Next |
|---|---|---|

## 8. Publish Source

### For ahnda.com

### For bomts.com / bomts.net

## 9. Next Action

게시용 원천 글감 포맷:

# Publish Source: <title>

- Target:
  - [ ] ahnda.com
  - [ ] bomts.com / bomts.net

## Draft Summary

## Background

## What was built or decided

## Why it matters

## Technical details

## Next step

작업 방식:
1. 먼저 현재 상태를 읽고 정리한다.
2. 안전한 점검 명령은 자동 실행한다.
3. 필요한 디렉토리와 템플릿은 /project/ai-hub 하위에 자동 생성한다.
4. 실제 서비스, 거래, 보안, 네트워크, 삭제, 배포 관련 작업은 승인 요청한다.
5. 각 작업 후 syntax/import/mock 수준의 검증을 수행한다.
6. 검증 결과를 history에 남긴다.
7. 게시 가능한 요약을 publish-source에 남긴다.
8. 다음 작업을 명확히 제안한다.

첫 번째로 수행할 작업:
1. /project 구조를 점검한다.
2. /project/ai-hub/prompt 구조가 있는지 확인한다.
3. /project/ai-hub/doc/history 및 publish-source 구조를 생성한다.
4. 작업 세션 템플릿과 게시 원천 글감 템플릿을 생성한다.
5. ai_hub_work_start.md 내용을 자동 실행 중심으로 정리한다.
6. 실제 서비스 경로나 BomTS 실제 소스는 수정하지 않는다.
7. 수행 결과를 history/session에 기록한다.
8. ahnda.com 게시용 원천 글감 초안을 publish-source/ahnda에 남긴다.