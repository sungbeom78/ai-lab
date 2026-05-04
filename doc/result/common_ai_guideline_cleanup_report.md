# Common AI Guideline Cleanup Report

## 변경 파일 목록 (Changed Files)

### 새로 생성됨 (Created)
- `/project/ai-hub/prompt/system/ai_hub_work_start.md`
- `/project/ai-hub/prompt/project/bomts_work_start.md`
- `/project/ai-hub/prompt/project/lostway_work_start.md`
- `/project/ai-hub/prompt/task/common_task_start_template.md`
- `/project/ai-hub/prompt/task/lostway_task_start_template.md`

### 삭제/이동됨 (Deleted/Moved)
- `/project/ai-hub/prompt/system/bomts_work_start.md` (project 디렉토리로 이동 및 수정)

### 점검됨 (Verified)
- `/project/ai-hub/prompt/task/bomts_task_start_template.md` (이미 BomTS 전용으로 잘 설정되어 있음)

## 수행 작업 내역 (Actions Performed)

1. **Python 기본 환경 확인**
   - 시스템에 `Python 3.12.3`, `pip 24.0`이 정상적으로 설치되어 있음을 확인했습니다.

2. **Shell script 실행 방식 점검**
   - 검색 결과, `python ./script/check_lostway_mount.sh`를 지시하는 문서가 계획서(instructions) 외에는 존재하지 않음을 확인했습니다. 수정이 필요한 대상 문서가 없었습니다.

3. **지침 구조 정리 및 파일 이동**
   - 지침에 명시된 디렉토리 구조(`system`, `project`, `task`)에 맞춰 파일들을 재배치하고 내용을 갱신했습니다.

4. **경로 참조 정리**
   - `ai-hub/reference/bomts`와 같은 구 경로가 사용된 곳이 있는지 전체 검색했으나, 계획서를 제외하고는 발견되지 않았습니다.
   - BomTS 관련 지침이 `ai_hub_work_start.md`의 `BomTS` 영역 하위로 적절히 격리되었음을 확인했습니다.

## 남은 확인사항과 권장 다음 작업 (Remaining Checks & Next Steps)

- **lostway 환경 검증**: `/project/lostway` 경로가 실제로 마운트되어 있는지, 그리고 `script/check_lostway_mount.sh`가 문제 없이 동작하는지 테스트가 필요할 수 있습니다.
- **각 프로젝트별 실제 Task 진행**: 새로운 공통 지침(`ai_hub_work_start.md`) 및 Task Start 템플릿들을 사용하여 실제 작업을 테스트해 보는 것을 권장합니다.
