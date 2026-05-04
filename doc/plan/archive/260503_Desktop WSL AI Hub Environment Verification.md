목표:
데스크탑 Windows WSL2 Ubuntu 환경에 구성된 On-Premise AI Hub 개발 환경을 점검하고, 노트북 Antigravity에서 안정적으로 접속하여 작업할 수 있도록 기본 연결/검증 구조를 완성한다.

중요 원칙:
- 기존 BomTS 소스는 수정하지 않는다.
- lostway 서비스 서버의 파일도 아직 수정하지 않는다.
- API key, secret, 계정 정보는 생성/수정/노출하지 않는다.
- 자동 commit, push, deploy는 금지한다.
- Windows 방화벽 전체 개방은 금지한다.
- Ollama 11434 포트를 외부 또는 LAN에 직접 공개하지 않는다.
- 모든 작업 결과는 문서로 남긴다.
- 디렉토리명은 단수형/원형을 우선한다.
  예: doc, log, model, script, publish

현재 전제:
- /project 는 WSL 내부 실제 디렉토리다.
- /project/ai-hub 는 Windows SSD 경로에 연결되어 있다.
- /project/bomts-ai 는 Windows SSD 경로에 연결되어 있다.
- /project/doc 는 Windows SSD 경로에 연결되어 있다.
- /project/publish 는 Windows SSD 경로에 연결되어 있다.
- /project/log 는 Windows SSD 경로에 연결되어 있다.
- /project/script 는 Windows SSD 경로에 연결되어 있다.
- /project/lostway 는 서비스 서버 Linux의 /project/lostway 를 SSHFS로 마운트한다.
- /project/model 은 WSL 내부 ~/ai-local/model 에 연결되어 있다.
- /project/rag-index 는 WSL 내부 ~/ai-local/rag-index 에 연결되어 있다.
- /project/runtime 은 WSL 내부 ~/ai-local/runtime 에 연결되어 있다.
- /project/site 는 NUC-main Linux의 /project/site 를 SSHFS로 마운트한다.
- /project/site/ahnda 는 www.ahnda.com 실제 사이트 루트다.
- /project/site/bomts 는 www.bomts.net 또는 www.bomts.com 실제 사이트 루트다.
- /project/publish 는 게시 후보 산출물이며, 실제 서비스 루트가 아니다.

수행 작업:
1. WSL 상태 확인
   - wsl -l -v 결과 확인
   - Ubuntu-24.04가 WSL2인지 확인

2. /project 구조 확인
   - ls -al /project
   - readlink -f /project/*
   - /project 자체가 Windows 경로 symlink가 아닌지 확인
   - 각 하위 경로가 의도한 위치를 가리키는지 확인

3. lostway 마운트 확인
   - mountpoint -q /project/lostway
   - /project/script/check_lostway_mount.sh 실행
   - mount_lostway.sh, unmount_lostway.sh, check_lostway_mount.sh 내부 경로가 /project/script 기준으로 맞는지 확인
   - 오타가 있으면 수정안을 제시하되, 수정 전 diff를 보여준다

4. site 마운트 확인
   - mountpoint -q /project/site
   - /project/script/check_site_mount.sh 실행
   - mount_site.sh, unmount_site.sh, check_site_mount.sh 존재 여부 확인

5. GPU/Ollama 확인 (자동 실행)
   - nvidia-smi
   - ollama --version
   - curl http://localhost:11434/api/tags
   - gemma3:4b 설치 여부 확인
   - qwen2.5-coder:7b 설치 여부 확인
   - qwen2.5-coder:7b가 없으면 설치 명령만 제안하고, 실제 설치는 사용자 승인 후 진행한다. (대형 모델 설치는 승인 요청)

6. Python 환경 확인 (자동 실행):
   - python3 --version
   - python --version
   - pip --version
   - python 명령이 없으면 설치 명령만 제안하고 사용자 승인 후 진행한다. (설치는 승인 요청)
     sudo apt update
     sudo apt install -y python3 python-is-python3 python3-pip python3-venv
   - .sh 파일은 python으로 실행하지 않는다.
   - check_lostway_mount.sh 실행은 bash /project/script/check_lostway_mount.sh 또는 /project/script/check_lostway_mount.sh 로 수행한다.

7. 노트북 Antigravity 접속 준비 (조회 및 초안 생성은 자동 실행)
   - WSL sshd 설치 여부 확인
   - sshd_config 확인
   - Port 2222 사용 권장
   - PasswordAuthentication no 권장
   - PubkeyAuthentication yes 권장
   - PermitRootLogin no 권장
   - 데스크탑 Windows portproxy 설정 스크립트 초안 작성 (실제 등록은 승인 요청)
   - Windows 방화벽 규칙 생성 명령 초안 작성 (실제 추가는 승인 요청)
   - 노트북 ~/.ssh/config 예시 작성

8. AI Hub 공통/프로젝트별 지침 분리 확인
   - /project/ai-hub/prompt/system/ai_hub_work_start.md 존재 확인
   - /project/ai-hub/prompt/project/bomts_work_start.md 존재 확인
   - /project/ai-hub/prompt/project/lostway_work_start.md 존재 확인
   - BomTS 거래 시스템 지침이 AI Hub 공통 지침으로 사용되지 않는지 확인한다.
   - BomTS reference root는 /project/ai-hub/doc/reference/bomts 로 통일되어야 한다.

9. 결과 문서 작성
   - /project/ai-hub/doc/result/setup_report.md
   - /project/ai-hub/doc/result/remote_access_guide.md
   - /project/ai-hub/doc/result/project_path_policy.md

산출물:
- /project/ai-hub/doc/result/setup_report.md
- /project/ai-hub/doc/result/remote_access_guide.md
- /project/ai-hub/doc/result/project_path_policy.md
- 수정이 필요한 script diff