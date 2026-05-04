# 작업 로그: /project 전체 Workspace 정책 정리

- Date: 2026-05-04
- Category: 인프라/개발환경

## 오늘 한 일

desktop-ai의 작업 폴더를 `/project/ai-hub`에서 `/project` 전체로 확장했다.
그에 맞게 workspace 정책, README, 매니페스트, Git 전략을 새로 정리했다.

## 왜 했는지

ai-hub만 바라보면 site 개발이나 bomts-ai 작업을 할 때마다 범위가 애매했다.
`/project` 전체를 열면서 "넓게 열고, 좁게 수정한다"는 원칙을 세우면
매번 작업 범위를 명확히 지정할 수 있다.

## 진행하면서 든 생각

- 구조 잡는 데 시간을 너무 쓰면 안 된다. 빨리 깔고 실제 개발로 넘어가자.
- site, lostway가 마운트 안 되어 있으면 Permission denied가 뜬다.
  다음에 작업할 때 마운트 상태 먼저 확인해야 한다.
- ai-hub 기존 지침은 폐기하지 않고 하위 실행 지침으로 두기로 했다.

## 결과

5개 파일 신규 생성:
- `/project/README.md` — workspace 개요
- `/project/workspace.yaml` — 프로젝트 매니페스트
- `/project/.gitignore` — git 제외 목록
- `/project/doc/workspace_policy.md` — 전체 정책
- `/project/doc/git_strategy.md` — Git 전략

## 남은 일

- site/ahnda 마운트 확인 후 ahnda 포털 MVP 개발
- Local AI Console 상태 확인
- git init/commit (사용자 승인 후)

## 나중에 돌아보면

이 시점이 ai-hub 단독 → /project 전체로 확장한 전환점이다.
여기서 깔아둔 정책이 향후 작업의 기준선이 된다.
