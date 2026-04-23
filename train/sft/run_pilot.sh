#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

python3 "$ROOT/scripts/train_unsloth_vision_sft.py" \
  --config "$ROOT/DocAI-OCR/train/sft/qwen2_5_vl_7b_qlora.json" \
  "$@"
