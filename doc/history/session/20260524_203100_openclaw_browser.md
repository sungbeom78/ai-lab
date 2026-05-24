# AI Hub Work Session Log - 2026-05-24 (File Picker & Absolute Prompt)

- **세션 ID**: `20260524_203100_openclaw_browser`
- **목표**: Instruction File Path를 수동 오타 기입 없이 마우스 클릭으로 간편하게 선택할 수 있게 VS Code 네이티브 파일 다이얼로그(`showOpenDialog`)를 연동하고, 해당 기획 파일의 내용을 AI가 1순위로 엄수하여 구현하도록 프롬프트 권위를 극대화한다.
- **수행 유형**: Develop, Native Dialog API, Prompt Tuning

## 1. 구현 완료 내역 (Detailed Changes)

### 1-1. VS Code 네이티브 탐색기 연동
- **파일**: `/project/openclaw-vscode-extension/src/OpenClawViewProvider.ts`
  - HTML 웹뷰 내에 `Instruction File Path` 텍스트 상자와 **"파일 선택 🔍"** 버튼이 가로 flex 정렬로 배치되도록 레이아웃 고도화.
  - 버튼 클릭 시 `browseFile` 이벤트를 확장 프로그램 TS 백엔드로 postMessage 전송.
  - 백엔드에서 `vscode.window.showOpenDialog`를 호출하여 기획 문서(`.md`, `.json`, `.txt` 등)를 선택할 수 있게 연동.
  - 사용자가 선택한 절대경로를 `selectedFile` 이벤트를 통해 웹뷰로 복귀 전송하여 텍스트 상자에 자동 바인딩 완료.

### 1-2. 기획 지침 '절대 복종 규칙' 프롬프트 장착
- **파일**: `/project/ai-hub/app/openclaw/instruction.py`
  - 기획서가 주입되는 헤더 명을 **`## Instruction File [CRITICAL / ABSOLUTE RULE]`**로 규정.
  - 모델(Qwen)에게 **"이 기획 지침서는 귀하가 이번 개발에서 준수해야 할 최상위 절대 복종 지침(Absolute Directive)이므로, 관성적 설계를 버리고 1순위 상위 원칙으로 100% 한 치의 오차도 없이 무조건 엄수하여 개발하라"**는 명확한 이탈 차단 프롬프트 주입.

---

## 2. 배포 패키지 빌드 성공
- `/project/openclaw-vscode-extension` 폴더에서 `npm run compile && npx -y @vscode/vsce package ...` 명령어를 완수하여 `openclaw-vscode-0.0.1.vsix` 최신 배포 패키지를 갱신함.

---

## 3. 향후 계획 (Next Steps)
- 실제 VSIX 재설치 후, 돋보기 버튼 클릭으로 기획 문서를 선택하여 Qwen2.5-coder가 기획 지침의 세부적인 기능 및 레이아웃 설계를 한 치의 오차도 없이 기가 막히게 파일 시스템에 반영하는지 실전 모니터링 수행.
