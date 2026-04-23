# Finetuning Plan: DocAI-OCR

## Current State

- `v0`는 `document_content`가 직접 프롬프트에 들어가므로 텍스트 모델도 일부 통과한다.
- 실제 `v1` 평가 문서 자산은 30/30 누락이다.
- 현재 train 문서 자산도 27/27 누락이다.
- 이 프로젝트는 텍스트 LLM 미세조정보다 멀티모달 모델 전환이 핵심이다.

## Priority

- 우선순위: 상
- 이유: 자산만 복구되면 멀티모달 LoRA 실험으로 바로 개선 폭을 확인할 수 있다.

## Base Models

- Primary: `Qwen/Qwen2.5-VL-7B-Instruct`
- Secondary: `google/gemma-4-E4B-it`
- Lightweight fallback: `google/gemma-4-E2B-it`

## Phase 0

1. `documents/` 자산을 train/eval 모두 복구한다.
2. 문서 유형을 아래 4개로 태깅한다.
   - receipt
   - invoice / contract
   - form / hr record
   - table-heavy document
3. 출력 포맷을 `JSON field extraction`과 `markdown table parse` 두 가지로 고정한다.
4. image/PDF와 inline text sample을 섞지 말고 별도 split으로 관리한다.

## Phase 1

- 목표: language-only LoRA로 document QA / extraction 안정화
- 권장 시작점
  - `max_seq_length=4096`
  - `per_device_train_batch_size=1`
  - `gradient_accumulation_steps=8`
  - `learning_rate=1e-4`
  - `lora_r=16`
- 첫 실험에서는
  - `finetune_vision_layers = False`
  - language / attention / MLP만 학습

## Phase 2

- hard OCR / table-heavy split에서만 vision layer unfreeze 실험을 추가한다.
- `Gemma 4` 계열은 멀티모달 입력을 항상 image first로 넣는다.
- OCR / 문서 파싱은 visual token budget을 높게 잡는다.
  - `560`: 일반 문서
  - `1120`: 작은 글씨, 표, handwriting

## Model Notes

- `Qwen2.5-VL`은 OCR, DocVQA, form/table extraction 쪽이 강점이다.
- `Gemma 4` E2B/E4B는 multimodal FT를 지원하지만 처음엔 vision layer를 고정하는 편이 안전하다.

## Exit Criteria

- `document_understanding_accuracy >= 0.85`
- receipt / form split에서 `field_extraction_accuracy >= 0.9`
- table-heavy split에서 `table_parse_accuracy >= 0.75`
