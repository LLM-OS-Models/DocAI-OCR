# DocAI-OCR

문서 AI / OCR 평가 트랙.

문서 경로와 질문이 주어지면, 모델이 문서에서 필드 값을 추출하고 표 구조를 파싱하는 능력을 평가한다. 필드 추출 정확도와 표 파싱 정확도를 가중 평균하여 종합 점수를 계산한다.

## 평가 메트릭

| 메트릭 | 설명 |
|--------|------|
| `field_extraction_accuracy` | gold 필드 값이 모델 응답에 포함된 비율 (0~1). 완전 일치=1.0, 숫자 포함=0.8, 단어 겹침=비율 |
| `table_parse_accuracy` | gold 테이블 헤더가 모델 응답에 포함된 비율 (0~1) |
| `document_understanding_accuracy` | `0.6 × field_accuracy + 0.4 × table_accuracy` |

**성공 조건**: `document_understanding_accuracy > 0.5`

## 필드 매칭 로직

`_field_match(gold_value, pred_text)`:
1. 대소문자 무시 부분문자열 포함 → 1.0
2. 숫자만 추출하여 포함 → 0.8
3. 단어 단위 겹침 비율 → 0~1
4. 매칭 없음 → 0.0

## 샘플 데이터 형식

### 문서 필드 추출 (doc_0001)

```json
{
  "sample_id": "doc_0001",
  "user_query": "이 문서에서 계약 금액과 계약일을 추출해라.",
  "artifacts": {"document_path": "documents/contracts/contract_001.pdf", "document_content": "계약금액: ₩120,000,000\n계약일: 2026-03-12\n..."},
  "gold": {
    "fields": {"contract_amount": "₩120,000,000", "contract_date": "2026-03-12"}
  }
}
```

### 표 파싱 (doc_0002)

```json
{
  "sample_id": "doc_0002",
  "user_query": "이 재무 문서에서 표를 파싱하고 총자산 항목을 찾아라.",
  "artifacts": {"document_path": "documents/finance/balance_sheet_01.png", "document_content": "항목 | 금액\n---|---\n총자산 | 1,240,000,000\n..."},
  "gold": {
    "fields": {"총자산": "1,240,000,000"},
    "table_headers": ["항목", "금액"]
  }
}
```

> **참고**: document_content가 제공되면 프롬프트에 문서 텍스트를 직접 포함

## 프로젝트 구조

```
DocAI-OCR/
├── README.md
├── pyproject.toml
├── eval/
│   ├── internal/
│   │   └── v0.jsonl        # 평가 데이터셋 (2샘플)
│   └── results/
├── tests/
└── data/
```

## 실행

```bash
uv sync

llm-os-eval run docai_ocr \
  --model Qwen/Qwen3-4B \
  --samples eval/internal/v0.jsonl \
  --output eval/results/Qwen3-4B_v0.jsonl \
  --base-url http://localhost:8001/v1
```

## 벤치마크 결과 (2026-04-23, Round 3)

| 모델 | Size | field_accuracy | table_accuracy | overall | 성공률 |
|------|------|---------------|----------------|---------|--------|
| Qwen3-8B | 8B | 0% | **50%** | 20% | 0% |
| gemma-4-31B-it | 31B | 0% | **50%** | 20% | 0% |
| 나머지 전체 | — | 0% | 25% | 10% | 0% |

텍스트 전용 모델은 PDF/이미지 문서를 직접 볼 수 없어 field_extraction_accuracy가 0%이다. 테이블 헤더는 질문 프롬프트에서 유추하여 일부 모델이 50%를 달성한다. 비전 기반 모델(Qwen2-VL 등)을 사용하면 결과가 크게 개선될 것이다.
