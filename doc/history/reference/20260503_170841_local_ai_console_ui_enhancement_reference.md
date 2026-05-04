# 작업 레퍼런스: Local AI Web Console UI 개선 및 Markdown 렌더링 도입

- Date: 2026-05-03
- Project: ai-hub

## 1. 주요 변경사항 및 구현 과정 설명
- **한국어 응답 강화**: `job_context.py`에 Output Requirements를 수정하여 어떤 지시를 하더라도 결과물이 한국어로 생성되도록 프롬프트를 보강했습니다.
- **결과 복사 기능**: `app.js`에 `navigator.clipboard.writeText`를 활용해 "결과 복사" 및 "Markdown 복사" 버튼을 연동했습니다.
- **Markdown 모달 렌더링**: `index.html`에 CDN으로 `marked.js`를 가져와, Recent Jobs 목록을 클릭할 때 `/api/jobs/{job_id}/result` API에서 원본 MD를 받아와 즉석에서 HTML로 렌더링하도록 `app.js`를 수정했습니다.

## 2. 테스트 결과 및 확인 사항
- Python syntax check 통과 완료
- Health API 및 Models API 정상 통신 확인
- Qwen 모델에게 한국어 강제 테스트 지시 후, 정상적으로 한국어 마크다운 포맷팅 결과 수신 확인
- 브라우저 상에서 Recent Jobs 클릭 시 모달창이 열리고 `marked.js`가 정상 작동하는 것 확인

## 3. 보안 관련 리뷰 및 수정 내용
- **Path Traversal 방지**: `main.py`의 결과 파일 반환 API(`/api/jobs/{job_id}/result`)에서 `job_id`에 정규식 `^[a-zA-Z0-9_\-]+$` 검증을 적용하여, 폴더 밖의 파일(`../`)을 탈취하려는 시도를 원천 차단했습니다.

## 4. 다음 작업 제안
이제 결과물이 웹 상에서 시각적으로 보기 좋게 렌더링되므로, 이 결과물 내의 코드 블록이나 제안된 파일 수정안을 긁어서 사용자가 손수 적용하지 않아도 되게끔 **"프로젝트에 코드 자동 적용 (Apply Patch)" 기능**을 콘솔에 탑재하는 것을 제안합니다.
