# Publish Source Policy

## 1. 목적
AI Hub에서 발생한 작업 이력(`doc/history`) 중 가치 있는 내용을 외부(웹사이트)에 게시할 수 있도록 가공, 보관합니다.

## 2. 타겟별 성격
- **`ahnda.com`**: 사용자 경험, 서비스 방향성, 철학, 일반적인 개발 이야기 중심
- **`bomts.com` / `bomts.net`**: 기술 스택 깊은 이야기, 개발 아키텍처, 자동화 로직, 운영 트러블슈팅 중심

## 3. 원칙
- **선별 기준**: 단순 반복 작업이 아닌, 의사결정, 문제 해결, 새로운 자동화 환경 구축 등 지식 공유 가치가 있는 내용을 기반으로 합니다.
- **검토 필수**: 모든 초안은 게시 전에 반드시 검토를 거쳐야 합니다.
- **보안 및 민감 정보 제거**: 
  - 실제 내부 경로 (예: Windows 드라이브 경로, NUC 사용자명 등)
  - API Key, Secret Token
  - DB Schema 세부사항 등 민감 데이터는 절대 포함되지 않도록 마스킹 처리합니다.

## 4. 템플릿 포맷
각 글감은 아래 항목을 포함하는 마크다운 초안으로 작성합니다:
- 대상 타겟 (`ahnda.com` 또는 `bomts.com`)
- 요약 (Draft Summary)
- 배경 (Background)
- 주요 내용 및 결정 사항 (What was built or decided)
- 중요성 (Why it matters)
- 기술적 디테일 (Technical details)
- 향후 과제 (Next step)
