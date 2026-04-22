# Experiment Card: DocAI-OCR

## task_type
`docai_ocr`

## 목적
이미지/PDF 문서를 텍스트, 레이아웃, 표, 도표 단위로 구조화하고 downstream task에 연결한다.

## 핵심 지표
- field_extraction_accuracy — 타겟 필드 추출 정확도 (0~1)
- table_parse_accuracy — 테이블 헤더 적중률 (0~1)
- document_understanding_accuracy — 종합 점수 (0.6 * field + 0.4 * table)

## 평가 실행
```bash
bash eval/run_phase1.sh
bash eval/run_phase2.sh
```

## 평가 모델
- Phase 1: 8개 모델
- Phase 2: Qwen3.6-27B + LFM 모델
