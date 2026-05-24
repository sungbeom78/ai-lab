# OpenClaw 원격 접속 가능 여부 확인

## Goal
동일 공유기 내 다른 리눅스 환경에서 OpenClaw Bridge Server(포트 11005)를 통해 Gemma 3 및 Qwen 모델을 사용할 수 있는지 확인 및 연동 방법 안내

## Actions
- `openclaw-bridge.service` 및 `start_openclaw.sh` 분석: 서버가 `0.0.0.0:11005`로 바인딩됨을 확인 (외부 접속 가능).
- `app/openclaw/main.py` 분석: `POST /api/chat` 등의 REST API 엔드포인트 지원 및 모델 선택(`model` 파라미터) 구조 확인.
- `openclaw-vscode-extension/package.json` 분석: VS Code 확장에서 `openclaw.apiUrl` 설정을 통해 원격 서버 주소 지정이 가능함을 확인.
- `script/refresh_wsl_ssh_portproxy.ps1` 분석: Windows 호스트(`192.168.50.242`)의 `11005` 포트가 이미 WSL로 포트포워딩 되도록 스크립트가 구성되어 있음을 확인.

## Result
- 원격 리눅스 PC에서 `http://192.168.50.242:11005` 주소로 VS Code 확장 설정 또는 REST API 직접 호출을 통해 정상적으로 이용 가능함을 확인하고 사용자에게 안내함.

## Next Action
- 사용자가 원격 연결 시 방화벽 문제 등 추가적인 트러블슈팅을 요청할 경우 지원.
