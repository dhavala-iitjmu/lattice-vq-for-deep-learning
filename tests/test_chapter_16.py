from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_16_reed_muller.py"


def load_module():
    if str(MODULE_PATH.parent) not in sys.path:
        sys.path.insert(0, str(MODULE_PATH.parent))
    spec = importlib.util.spec_from_file_location("chapter_16_reed_muller", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_rm_1_2_codewords_are_even_parity() -> None:
    module = load_module()
    codewords = module.generate_binary_code(module.RM_1_2_GENERATOR)

    assert len(codewords) == 8
    assert all(module.is_even_parity(word) for word in codewords)
    assert (1, 0, 0, 1) in codewords
    assert (1, 0, 0, 0) not in codewords


def test_running_decomposition_and_encoding() -> None:
    module = load_module()
    example = module.build_example()

    assert example.running_signature == (1, 0, 0, 1)
    assert example.running_even_part == (0, 0, -2, 2)
    assert example.generated_from_101 == (1, 0, 1, 0)


def test_validation() -> None:
    module = load_module()

    try:
        module.xor_vectors((1, 0), (1,))
    except ValueError as error:
        assert "equal lengths" in str(error)
    else:
        raise AssertionError("xor_vectors should reject unequal lengths")


if __name__ == "__main__":
    test_rm_1_2_codewords_are_even_parity()
    test_running_decomposition_and_encoding()
    test_validation()
