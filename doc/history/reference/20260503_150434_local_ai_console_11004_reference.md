# 작업 레퍼런스: Local AI Web Console 11004 포트 및 VENV 고도화

- Date: 2026-05-03
- Project: ai-hub

## 1. 개요
WSL 로컬 환경에서 구동하는 AI 웹 콘솔의 기본 포트를 11004로 이전하고, python `venv`를 도입하여 시스템 패키지와 독립적인 구동 환경을 구축했습니다.

## 2. VENV 적용 방식
```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```
시스템 python이 아닌 가상환경의 파이썬 인터프리터를 사용하여 패키지 의존성을 격리합니다. `run_local_ai_console.sh` 실행 시 `.venv` 여부를 자동 탐지합니다.

## 3. 외부 접속 준비 (Windows Portproxy)
외부 기기(노트북)에서 WSL2(11004)로 접속하기 위해 `local_ai_console_external_access_approval.md`를 작성했습니다. Windows 호스트에서 `netsh interface portproxy` 명령어와 `New-NetFirewallRule` 명령어를 통해 포워딩이 이루어집니다.
