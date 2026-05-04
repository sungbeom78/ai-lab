# 기술 블로그 초안: AI Hub의 작업 이력, 어떻게 설계해야 효율적일까?

- Target:
  - [ ] ahnda.com
  - [x] bomts.com / bomts.net

## Draft Summary
AI Hub 자동화 파이프라인에서 '기술 레퍼런스 원본(reference)'과 '퍼블리싱용 초안(publish-source)'의 역할을 엄격히 분리하여, 지식의 유실을 막고 외부 공개의 안정성을 높인 구조 개선 사례입니다.

## Background
이전 작업에서 AI의 모든 작업을 자동으로 기록하는 체계를 구축했습니다. 하지만 기술적인 상세 내용(명령어, 설정 파일 등)을 바로 퍼블리싱용 폴더에 담다 보니 보안 검토가 어렵고, 실제 기술 원본으로써의 깊이가 얕아질 우려가 있었습니다.

## What was built or decided
작업 이력을 크게 3가지 계층으로 분리했습니다.
1. **내부 원장 (`history/session`)**: AI와 사용자가 협업한 세션 자체의 순수한 기록
2. **기술 원본 (`reference/bomts`)**: 작업을 100% 재현할 수 있는 무결성 있는 기술 절차서. IP나 포트 등 민감 정보는 모두 `<IP>`, `<PORT>` 등의 Placeholder로 치환.
3. **게시 초안 (`publish-source/bomts`)**: 원본 레퍼런스를 기반으로 대중에게 공개 가능한 수준으로 다듬은 블로그용 마크다운.

## Why it matters
이러한 데이터 계층 분리는 AI에게 "어디에 무엇을 어떤 톤앤매너로 저장해야 하는지"를 명확히 지시하게 해 줍니다. 결과적으로 **"자동 실행 - 원장 보존 - 안전한 공유"** 라는 완벽한 사이클을 구축하게 됩니다. 인간 개발자의 개입은 오직 마지막 '게시 초안'의 컨펌에만 머무를 수 있게 됩니다.

## Technical details
- `/project/ai-hub/doc/reference/bomts` 디렉토리 신규 생성
- `ai_hub_work_start.md` 시스템 프롬프트 업데이트 (각 폴더의 R&R 명시)
- 마크다운 파일 템플릿화 (`bomts_reference_template.md` 등) 적용 완료

## Next step
이 견고해진 이력 파이프라인을 바탕으로, 실제 서비스 로직(BomTS-AI) 연동 및 검증 작업을 자동화된 방식으로 전개할 예정입니다.
