# Labeling Guide: DocAI-OCR

## Goal

- 문서 필드 추출과 table parsing을 평가 가능한 구조로 저장한다.
- 문서 종류별 실패 모드를 태그로 남긴다.

## Required Fields

- `document_path`
- `document_type`
- `document_format`
- `page_count`
- `answer_format`
- `target_fields`

## Document Type Tags

- `receipt`
- `contract`
- `form`
- `table_heavy`

필요하면 보조 태그를 추가한다.

- `small_font`
- `handwriting`
- `low_quality_scan`
- `multi_page`

## Answer Format Rules

- `field_json`: 키와 값이 안정적인 필드 추출
- `markdown_table`: 표 구조 복원이 주목적일 때만 사용

한 샘플에 두 포맷을 동시에 gold로 두지 않는다.

## Verification

1. 문서가 열리는지 확인
2. 페이지 수 기록
3. 핵심 필드 위치 확인
4. 표가 있으면 헤더/행 구조 검증
5. answer_format 일치 여부 확인

## Common Mistakes

- OCR raw text를 그대로 정답으로 저장
- field extraction과 table parse를 한 문자열에 섞음
- 이미지와 PDF를 같은 난이도로 취급
