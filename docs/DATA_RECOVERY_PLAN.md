# Data Recovery Plan: DocAI-OCR

## Objective

- 누락 문서를 복구하고 field extraction / table parse gold를 evaluator contract에 맞게 고정한다.

## Current Blockers

- train/eval 문서 자산 누락
- 문서 타입 태깅 부족
- answer format 혼합 가능성

## Recovery Sequence

1. 누락 문서 인벤토리 확정
2. 파일 포맷별 자산 복구
3. 문서 타입 / 보조 태그 기입
4. page count 기록
5. field JSON 또는 markdown table gold 작성
6. QA 검수

## Required Outputs

- restored `documents/`
- updated metadata with type/format/page count
- normalized answer files
- QA completion sheet

## Acceptance

- missing document `0`
- type/format tags completion `100%`
- mixed answer format sample `0`
- verified sample ratio `100%`
