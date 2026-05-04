# Publish Source: AI 에이전트 작업의 효율을 높이는 "자동 실행 중심" 정책 도입기

- Target:
  - [ ] ahnda.com
  - [x] bomts.com / bomts.net

## Draft Summary
AI Hub 환경 구축 과정에서 매 단계별 승인을 요구하던 기존 방식의 병목을 해결하기 위해, 파괴적이거나 위험한 작업을 제외한 모든 문서 작업, 점검, 환경 셋업 등을 "자동 실행"하도록 허용하는 정책을 도입했습니다. 이와 함께 모든 과정을 마크다운(Markdown) 기반의 이력으로 남기는 체계를 구축했습니다.

## Background
보안과 안전을 위해 AI 에이전트의 모든 액션을 사용자에게 묻도록 설계했으나, 개발/문서화 극초기 단계에서는 단순한 파일 구조 변경이나 `pwd`, `ls`, `python --version` 같은 읽기 전용 작업에서도 승인을 기다려야 해 전반적인 작업 속도가 크게 저하되었습니다. 

## What was built or decided
1. **Tier 분리**: 작업을 `Auto-allowed`(자동 승인), `Approval-required`(승인 필요), `Forbidden`(금지) 등급으로 나누었습니다.
2. **History Accumulation**: 단순히 작업을 빠르게 처리하는 데 그치지 않고, `Session`, `Event`, `Decision`, `Error` 4개의 분류로 작업 로그를 남기도록 했습니다.
3. **Publish Source 연계**: 가치 있는 의사결정과 구축 내역은 향후 블로그 글로 퍼블리싱할 수 있도록 자동으로 초안을 작성하는 룰을 추가했습니다.

## Why it matters
이 변화는 AI 기반 워크플로우(Autonomous Work Loop)가 인간의 개입을 최소화하면서도, 투명성(작업 이력)을 확보하는 핵심적인 밸런스를 맞춘 사례입니다. 더 적은 커뮤니케이션으로 더 많은 문서를 작성하면서도, 위험 요소를 격리할 수 있게 되었습니다.

## Technical details
- `tool_permission.yaml` 파일에 안전 명령어(`ls`, `cat`, `grep`, `ollama` 등) 화이트리스트 명시
- 프롬프트에 "묻지 말고 실행하라"는 명확한 `Auto-Run Tier` 정책 주입
- 모든 실패는 1회 분석 후 재시도하며, 2회 실패 시 파이프라인 중단 없이 해당 항목만 Pending 처리

## Next step
이제 이 체계를 바탕으로 거래 시스템(BomTS)과 상담 서비스(Lostway)의 본격적인 코드 점검 및 마이그레이션을 빠른 속도로, 이력을 축적하며 진행할 수 있습니다.
