# [2026-05-05] OpenClaw Bridge Server 및 VS Code 확장 MVP 개발 완료

## 진행한 작업
- 데스크탑 AI 환경을 내 VS Code 조종석으로 만들기 위해 **OpenClaw Bridge Server**와 **VS Code 확장(Extension)**을 동시에 개발했습니다.
- 기존 AI Hub 포트(11004)를 피해 `11006`번 포트로 새로운 FastAPI 서버를 띄웠고, `gemma3:4b`와 `qwen2.5-coder:7b` 모델을 자동으로 분기하여 처리하도록 라우터를 구성했습니다.
- Windows VS Code 측에서는 TypeScript로 웹뷰를 가진 Extension을 만들었고, 현재 파일, 워크스페이스 정보 등을 로컬 서버(11006)로 전송할 수 있도록 통신 모듈(`api.ts`)을 구성했습니다.

## 주요 고려사항 및 결과
- "코드 작성해줘" 같은 요청이 들어가면 자동으로 Qwen 모델로 빠지도록 했는데, Qwen 7B 모델을 처음 메모리에 올릴 때 리소스(RAM 등) 문제로 상당히 오래 걸리거나 응답이 멈추는 현상이 관찰되었습니다. 데스크탑 모델 최적화가 필요할지도 모르겠습니다.
- 일단 백엔드(Python FastAPI)와 프론트엔드(VS Code Extension) 구조는 완전히 뼈대가 잡혔고, 이제 VS Code 안에서 `vsce package` 명령으로 확장을 설치해서 테스트해 볼 수 있습니다.

## 다음 단계
1. Windows 호스트의 VS Code에서 직접 확장을 빌드하고 설치(`Install from VSIX`)
2. 우측 사이드바에 나타난 OpenClaw 패널에서 실제 코딩 관련 대화가 부드럽게 이어지는지 테스트
3. Qwen 모델의 타임아웃 문제를 해결하기 위해 시스템 모니터링 및 프롬프트 최적화 점검
