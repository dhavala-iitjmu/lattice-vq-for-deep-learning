from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_01_quantization.py"


def load_module():
    spec = importlib.util.spec_from_file_location("chapter_01_quantization", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_chapter_01_numbers() -> None:
    module = load_module()
    example = module.build_example()

    assert example.quantized_weights == (1, -2, 2, 0, 1, 0, -2, 3)
    assert round(example.original_dot, 2) == -13.41
    assert round(example.quantized_dot, 2) == -10.50
    assert round(example.dot_error, 2) == 2.91
    assert example.fp16_bits == 128
    assert example.int4_bits == 32


if __name__ == "__main__":
    test_chapter_01_numbers()
