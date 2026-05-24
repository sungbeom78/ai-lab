# BomTS Technical Reference - OpenClaw Native File Browser Integration

본 문서는 OpenClaw VS Code Extension의 웹뷰 설정 UI에서 로컬 기획 파일의 절대 경로를 안전하게 획득하기 위한 VS Code 네이티브 파일 열기 API(`showOpenDialog`) 바인딩 아키텍처 및 기획 지침 절대성 프롬프트 튜닝에 대한 기술 레퍼런스입니다.

---

## 1. 네이티브 파일 브라우징 아키텍처 (Native File Browser Data Flow)

```text
[Webview UI (Options Panel)]
       │
       ▼ (1) 'browseBtn' 돋보기 버튼 클릭
   vscode.postMessage({ type: 'browseFile' })
       │
       ▼ (2) Extension TS Backend (onDidReceiveMessage)
   vscode.window.showOpenDialog(filters: Markdown/JSON/Text)
       │
       ▼ (3) 사용자가 파일 선택 성공 (fsPath 획득)
   webviewView.webview.postMessage({ type: 'selectedFile', path: fsPath })
       │
       ▼ (4) Webview UI (selectedFile 리스너)
   instructionPath.value = msg.path (자동 바인딩 완료)
```

---

## 2. VS Code Extension API 구현 코드 (TypeScript)

`OpenClawViewProvider.ts` 에 이식된 네이티브 파일 브라우징 핵심 백엔드 구문입니다.
```typescript
case 'browseFile': {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    const defaultUri = workspaceFolders ? workspaceFolders[0].uri : undefined;
    
    const fileUris = await vscode.window.showOpenDialog({
        canSelectFolders: false,
        canSelectMany: false,
        defaultUri: defaultUri,
        openLabel: '기획 파일 선택',
        filters: {
            'Markdown/Text/JSON': ['md', 'txt', 'json', 'yaml', 'yml']
        }
    });
    
    if (fileUris && fileUris.length > 0) {
        webviewView.webview.postMessage({
            type: 'selectedFile',
            path: fileUris[0].fsPath
        });
    }
    break;
}
```

---

## 3. 기획 지침 절대 복종 프롬프트 명세 (Prompt Directive Spec)

기획 지침의 최상위 1순위 상위 원칙 보장을 위해 `instruction.py`에 적용된 절대성 튜닝 코드입니다.
```python
parts.append("## Instruction File [CRITICAL / ABSOLUTE RULE]")
parts.append("아래에 로드된 기획 지침 파일(Instruction / Specification File)은 귀하가 이번 개발 작업에서 따라야 할 **최상위 절대 지침(Absolute Directive)**입니다.")
parts.append("귀하의 기존 구현 방식이나 관성적인 아키텍처 설계를 고집하지 말고, **반드시 이 지침 파일에 기재된 기획 목표, 레이아웃 가이드, 기능 스펙 및 파일 생성/수정 요구사항을 100% 한 치의 오차도 없이 최우선 1순위로 엄수하여 개발을 진행하십시오.**")
parts.append("이 절대 지침 문서의 개발 스펙을 자의적으로 누락하거나 변경하여 구현하는 행위는 엄격히 금지됩니다. 이 스펙 문서는 귀하의 소스코드 작성을 구제하는 절대 복종 명령서입니다.")
```

이 고도화된 프롬프트 주입은 모델의 관성적 코딩 이탈 행위를 단숨에 무력화하며, 기획 문서를 정교하게 반영하여 코드를 생성하게 만듭니다.
