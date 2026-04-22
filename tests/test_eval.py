from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock
from llm_os_eval.schemas.sample import EvalSample
from llm_os_eval.schemas.result import EvalResult
from llm_os_eval.graders.docai_ocr import DocAIOCREvaluator

SAMPLES_PATH = Path(__file__).parent.parent / "eval" / "internal" / "v0.jsonl"


def _load_samples():
    samples = []
    with open(SAMPLES_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                samples.append(EvalSample.model_validate_json(line))
    return samples


def _make_runner_mock(response_text=""):
    runner = MagicMock()
    runner.generate.return_value = {
        "text": response_text,
        "tool_calls": [],
        "latency_ms": 100,
        "input_tokens": 10,
        "output_tokens": 20,
    }
    return runner


class TestSchemaValidation:
    def test_jsonl_schema_valid(self):
        samples = _load_samples()
        assert len(samples) >= 2
        for s in samples:
            assert s.task_type == "docai_ocr"
            assert s.difficulty in ("easy", "medium", "hard")
            assert s.user_query


class TestGraderIntegration:
    def setup_method(self):
        self.samples = _load_samples()
        self.runner = _make_runner_mock()
        self.evaluator = DocAIOCREvaluator(
            runner=self.runner, model_name="test", checkpoint_name="base"
        )

    def test_build_prompt(self):
        for sample in self.samples:
            sys_prompt, user_prompt = self.evaluator.build_prompt(sample)
            assert sample.user_query in user_prompt

    def test_grade_returns_metrics(self):
        mock_output = "계약금: ₩120,000,000\n계약일: 2026-03-12"
        first_graded = None
        for sample in self.samples:
            result = EvalResult(
                run_id="test",
                sample_id=sample.sample_id,
                task_type=sample.task_type,
                model_name="test",
                checkpoint_name="base",
                prompt_version="v1",
                raw_output=mock_output,
            )
            graded = self.evaluator.grade(sample, result)
            assert len(graded.metric_values) > 0
            # Verify key metrics are present
            assert "field_extraction_accuracy" in graded.metric_values
            assert "table_parse_accuracy" in graded.metric_values
            assert "document_understanding_accuracy" in graded.metric_values
            if first_graded is None:
                first_graded = graded

        # The mock output matches doc_0001 gold fields (₩120,000,000, 2026-03-12),
        # so first sample should have non-zero field_extraction_accuracy.
        assert first_graded.metric_values["field_extraction_accuracy"] > 0
        assert first_graded.metric_values["document_understanding_accuracy"] > 0
