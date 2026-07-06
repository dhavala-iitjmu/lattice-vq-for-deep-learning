from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_17_bit_planes.py"


def load_module():
    spec = importlib.util.spec_from_file_location("chapter_17_bit_planes", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_running_bit_planes() -> None:
    module = load_module()
    example = module.build_example()

    assert example.encoded_columns == ("0001", "0000", "1110", "0011")
    assert example.planes == (
        (1, 0, 0, 1),
        (0, 0, 1, 1),
        (0, 0, 1, 0),
        (0, 0, 1, 0),
    )
    assert example.reconstructed == example.vector
    assert example.lsb_even_parity is True


def test_twos_complement_roundtrip() -> None:
    module = load_module()

    for value in range(-8, 8):
        bits = module.to_twos_complement_bits(value, 4)
        assert module.from_twos_complement_bits(bits) == value


def test_validation() -> None:
    module = load_module()

    try:
        module.to_twos_complement_bits(8, 4)
    except ValueError as error:
        assert "out of range" in str(error)
    else:
        raise AssertionError("to_twos_complement_bits should reject out-of-range values")


if __name__ == "__main__":
    test_running_bit_planes()
    test_twos_complement_roundtrip()
    test_validation()
