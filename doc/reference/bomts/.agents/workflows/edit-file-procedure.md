---
description: File editing procedure to prevent encoding errors and ensure compliance
---

# 파일 수정 절차

## 규칙 위치 (Source of Truth)
이 절차는 아래 문서의 규칙을 수행하기 위한 것이다:
- doc/README_AI_GUIDELINE.md § RULE A (설정 파일 수정 필수 동반 작업)
- doc/guidelines/02_config.md (설정 파일 역할 분리)

## 관련 워크플로우
- 명령 실행 시 자동 승인 여부 → /safe-command-policy
- 코드 수정 후 검증 → /change-code-procedure

---

## 0. 인코딩 표준 — 절대 준수 (ENCODING STANDARD — ABSOLUTE)

> **이 규칙은 모든 파일 생성/수정에 예외 없이 적용된다.**

### 표준
| 항목 | 표준값 |
|------|--------|
| 인코딩 | **UTF-8, No BOM** (BOM 있으면 QA CRITICAL 오류) |
| 줄바꿈 | **LF** (`\n` 만, CRLF 금지) |
| 최종 줄 | 파일 끝에 빈 줄 1개 (`\n`) |

### 위반 시 영향
- QA `encoding_bom::*` → CRITICAL 실패
- QA `encoding_eol::*` → CRITICAL 실패
- 한글이 포함된 파일이 cp949로 저장되면 `c2 80` 오류 바이트 삽입됨

### 준수 방법 (우선순위 순)

1. **`write_to_file` / `replace_file_content` 도구 사용** — 도구가 UTF-8 LF를 보장
2. **Python 스크립트로 쓰기** (도구가 실패하거나 바이너리 조작이 필요한 경우)
   ```python
   # 반드시 이 패턴만 사용
   content = "...내용..."
   with open(path, 'wb') as f:
       f.write(content.encode('utf-8'))   # NoBOM, LF 유지
   ```
3. **절대 금지 패턴**
   - `Set-Content` / `Add-Content` (PowerShell) → cp949, CRLF 삽입
   - `Out-File` 기본값 (PowerShell) → UTF-16/BOM 삽입
   - `open(path, 'w')` (Python, Windows) → cp949로 열릴 수 있음
   - `open(path, 'w', encoding='utf-8-sig')` → BOM 삽입됨

### 수정 후 검증 (필수)
```bash
python tool/check_encoding.py
```
- `All encoding checks passed` 가 아니면 수정 완료로 보고하지 않는다.

---

## 1. 일반 파일 수정 — 도구 선택 규칙

| 상황 | 사용할 도구 |
|------|-----------|
| 파일 내용 확인 | `view_file` (grep_search가 실패하면 이것으로 대체) |
| 단일 연속 블록 수정 | `replace_file_content` |
| 여러 비연속 블록 수정 | `multi_replace_file_content` |
| 새 파일 생성 | `write_to_file` |
| .env 수정 | `view_file` → `replace_file_content` (grep_search 금지) |

### 금지 패턴
- PowerShell `Set-Content` / `Add-Content`로 소스 파일 생성/수정 → cp949 인코딩 손상
- PowerShell heredoc (@'...'@)으로 Python 파일 생성 → `write_to_file` 사용
- .env 파일 전체 재생성 → 민감정보 유실 위험. 반드시 백업 파일에서 복구 절차 사용

### 도구 실패 시 대응
- `grep_search` 취소/실패 → `view_file`로 대체
- `replace_file_content` 실패 → `view_file`로 현재 상태 재확인 후 재시도
- 동일 도구 2회 연속 실패 → 다른 도구로 전환, 전환 불가 시 작업 중단 후 사용자 보고

---

## 2. 설정 파일(.env, settings.yaml) 수정 절차

> 규칙 근거: doc/README_AI_GUIDELINE.md § RULE A

// turbo-all
수행 순서:
1. `view_file`로 수정 대상 파일 현재 상태 확인
2. 수정 **전** 백업 생성
   - PowerShell: `New-Item -ItemType Directory -Force -Path tmp\backup\config\{YYYYMMDD_HHmmss}`
   - PowerShell: `Copy-Item <대상파일> tmp\backup\config\{YYYYMMDD_HHmmss}\`
3. `replace_file_content` 또는 `multi_replace_file_content`로 수정
4. example 파일 동기화
   - `.env` 수정 시 → `.env.example` 구조 반영 (값은 비움)
   - `settings.yaml` 수정 시 → `settings.example.yaml` 구조 반영
5. `doc/change_log.md` 최상단에 변경 기록 추가
6. `python tool/check_encoding.py` 실행 → All passed 확인

---

## 3. .env 인코딩 손상 복구 절차

`.env`의 한글이 깨진 경우(c2 80 삽입, ? 대체 등) 아래 순서를 따른다:

1. `tmp/backup/config/` 에서 한글이 정상인 최신 백업을 찾는다
   ```bash
   python -c "
   import os,glob
   for d in sorted(glob.glob('tmp/backup/config/*'), reverse=True):
       for f in os.listdir(d):
           if '.env' in f:
               raw = open(os.path.join(d,f),'rb').read()
               kor = sum(1 for c in raw.decode('utf-8','replace') if '\uac00'<=c<='\ud7a3')
               print(d, f, 'korean:', kor)
   "
   ```
2. 한글 29자 이상인 백업을 정상 파일로 확인
3. 현재 `.env`에서 KEY=VALUE 값을 추출
4. 백업 구조(주석 포함) + 현재 값으로 재조립
5. `open(path, 'wb').write(content.encode('utf-8'))` 로 저장
6. `python tool/check_encoding.py` 로 검증
