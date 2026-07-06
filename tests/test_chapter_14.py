from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_14_higher_lattices.py"


def load_module():
    if str(MODULE_PATH.parent) not in sys.path:
        sys.path.insert(0, str(MODULE_PATH.parent))
    spec = importlib.util.spec_from_file_location("chapter_14_higher_lattices", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_running_vector_e8_comparison() -> None:
    module = load_module()
    example = module.build_example()

    assert example.d4_product_decoded == (1.0, -2.0, 2.0, -1.0, 1.0, 0.0, -2.0, 3.0)
    assert round(example.d4_product_squared_error, 4) == 0.6416
    assert example.e8_result.decoded == example.d4_product_decoded
    assert round(example.e8_result.d8_squared_error, 4) == 0.6416
    assert round(example.e8_result.shifted_squared_error, 4) == 0.7016


def test_shifted_shell_can_win() -> None:
    module = load_module()

    result = module.nearest_e8((0.49, 0.51, 0.48, 0.52, 0.5, 0.5, 0.49, 0.51))
    assert result.decoded == result.shifted_candidate
    assert result.shifted_squared_error < result.d8_squared_error


def test_validation() -> None:
    module = load_module()

    try:
        module.nearest_e8((1.0, 2.0))
    except ValueError as error:
        assert "length 8" in str(error)
    else:
        raise AssertionError("nearest_e8 should reject non-8D input")


if __name__ == "__main__":
    test_running_vector_e8_comparison()
    test_shifted_shell_can_win()
    test_validation()
