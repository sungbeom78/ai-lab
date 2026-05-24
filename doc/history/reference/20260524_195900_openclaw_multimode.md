# BomTS Technical Reference - OpenClaw Multi-Mode Alignment

본 문서는 OpenClaw의 다중 모드(Mode) 지원 기능 추가 및 지침(Prompt) 강화에 대한 아키텍처 및 구현 방법론적 기술 레퍼런스를 기술합니다. 

## 1. 아키텍처 및 데이터 흐름 (Data Flow)

```text
[VS Code Extension (Webview)]
        │  1) 다중 체크박스 선택 (#modeCheckboxes)
        │  2) 'sendMessage' 메시지 발송 (mode: "inspect,develop")
        ▼
[OpenClaw Bridge Server (main.py)]
        │  3) intent_router 분석 및 build_system_prompt 호출
        ▼
[instruction.py (build_system_prompt)]
        │  4) mode 쉼표 스플릿 분석 (["inspect", "develop"])
        │  5) _MODE_DIRECTIVES 기반으로 동적 지침 프롬프트 생성 및 조립
        ▼
[Local AI Model (Qwen/Gemma via Ollama)]
        │  6) 강제된 Proposed Files 룰에 맞춘 코딩 및 응답 생성
        ▼
[VS Code Extension (Webview)]
           렌더링 및 완성 코드 수령
```

---

## 2. 컴파일 및 배포 절차 (Build & Package Guide)

VS Code 확장 프로그램 소스(`OpenClawViewProvider.ts`) 변경 시에는 반드시 다음의 컴파일 및 빌드 프로세스를 수행해야 로컬 VS Code 에디터 환경에 변경 사항이 올바르게 반영됩니다.

### 2-1. 빌드 준비 및 종속성 확인
`/project/openclaw-vscode-extension` 폴더 내부로 이동한 후, `package.json`에 정의된 개발 종속성들이 설치되어 있는지 확인합니다.

### 2-2. 배포 패키지(.vsix) 컴파일 및 빌드 명령어
```bash
# 1) 타입스크립트 컴파일 및 VSIX 패키징 일괄 수행
npm run compile && npx -y @vscode/vsce package --no-git-tag-version --allow-missing-repository
```
* `prepublish` 스크립트에 의해 패키징 작업 전에 `npm run compile`이 자동 순차 실행됩니다.
* 빌드가 성공하면 루트 디렉토리에 `openclaw-vscode-0.0.1.vsix` 파일이 최종 갱신되어 최신 HTML 및 JS 연동 로직이 담기게 됩니다.

---

## 3. 프롬프트 세부 지침 설계 구조 (Prompt Directives Design)

`develop` 모드에서 AI가 코드를 요약하지 않고 동작 가능한 온전한 실소스를 뽑아내도록 만들기 위해 적용된 백엔드 `_MODE_DIRECTIVES["develop"]` 상세 내용입니다.

```python
_MODE_DIRECTIVES = {
    "develop": """[DEVELOP MODE DIRECTIVE - CRITICAL RULE]
- 당신은 현재 'develop(개발/수정)' 모드로 동작 중입니다.
- **[요약 금지 법칙] 절대로 변경 사항이나 해결책을 대략적인 개념 설명이나 말로 요약만 하고 응답을 끝마치지 마십시오.**
- **반드시 '## Proposed Files' 또는 이에 준하는 수정 대상 코드 섹션에 카피하여 즉시 파일에 반영할 수 있는 완전하고 완성도 높은 소스 코드(또는 완벽한 패치형 diff)를 한 줄도 생략 없이 구체적으로 작성해야 합니다.**
- 코드 중간을 주석으로 날려버리거나 채워 넣기를 미루는 중략 행위를 극도로 금지합니다. 동작 가능한 완전한 형태로 구현하십시오."""
}
```

이 강력한 지침은 LLM으로 하여금 'Response Format' 내의 'Proposed Files' 파트를 필수적으로 가득 메우게 만드는 심리적 강제력을 지니며, 로컬 환경에서 지시하는 코드 개발 작업의 실패율을 대폭 낮춥니다.
