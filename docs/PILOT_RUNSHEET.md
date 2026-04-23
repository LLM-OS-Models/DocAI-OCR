# Pilot Run Sheet: DocAI-OCR

## Objective

- VLM 전환만으로 field extraction과 table parsing이 실제로 올라가는지 확인한다.
- 첫 실험에서는 vision layer를 고정한 상태로 language adapter만 본다.

## Run IDs

- `DOC-P0`: 문서 자산 복구 완료 여부 검증
- `DOC-P1`: `Qwen2.5-VL-7B-Instruct` vision-freeze pilot
- `DOC-P2`: visual budget 확대 ablation
- `DOC-P3`: `Gemma 4` comparator 설계 보류

## Dataset Gate

- train/eval document missing `0`
- 문서 유형 태그 완료
- 포맷 split 완료:
  - receipt
  - contract / invoice
  - form / HR
  - table-heavy

## Model Matrix

| Run ID | Model | Page Cap | Visual Budget | Vision Layer | Purpose |
|---|---|---:|---:|---|---|
| DOC-P1 | `Qwen2.5-VL-7B-Instruct` | 3 | 560 | freeze | primary pilot |
| DOC-P2 | `Qwen2.5-VL-7B-Instruct` | 3 | 1120 | freeze | small-text / table stress |
| DOC-P3 | `gemma-4-E4B-it` | 3 | default | freeze | comparator only if P1 wins |

## Fixed Decisions

- input ordering: image first
- page cap: max 3 pages
- first stage: language / attention / MLP only
- output format: field JSON or markdown table only

## Primary Metrics

- `field_extraction_accuracy`
- `table_parse_accuracy`
- `document_understanding_accuracy`

## Slice Metrics

- receipt split
- form split
- contract split
- table-heavy split
- small-font split

## Accept

- overall `document_understanding_accuracy >= 0.85`
- receipt/form `field_extraction_accuracy >= 0.90`
- table-heavy `table_parse_accuracy >= 0.75`

## Reject

- text-only prompt leakage와 같은 shortcut이 남아 있음
- receipt만 좋아지고 contract/form이 무너짐
- page cap / visual budget 변경이 성능보다 비용만 키움

## Review Questions

1. 실패가 OCR recognition인지 document reasoning인지 분리되는가
2. table split 이득이 visual budget 증가와 직접 연결되는가
3. Gemma comparator가 정말 필요한지, 아니면 Qwen 계열에서 끝낼 수 있는가
