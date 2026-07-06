from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_07_nearest_lattice.py"


def load_module():
    spec = importlib.util.spec_from_file_location("chapter_07_nearest_lattice", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_running_block_decoding() -> None:
    module = load_module()
    example = module.build_example()

    assert example.decoded_blocks == ((1, -2, 2, -1), (1, 0, -2, 3))
    assert example.reconstructed_weight == (1, -2, 2, -1, 1, 0, -2, 3)
    assert example.results[0].rounded == (1, -2, 2, 0)
    assert example.results[0].repaired_coordinate == 3
    assert round(example.results[0].distance, 4) == 0.6427
    assert example.results[1].rounded == (1, 0, -2, 3)
    assert example.results[1].repaired_coordinate is None
    assert round(example.results[1].distance, 4) == 0.4780


def test_decoder_matches_bounded_brute_force() -> None:
    module = load_module()

    for block in module.RUNNING_BLOCKS:
        decoded = module.nearest_d4(block)
        brute_point, brute_distance = module.brute_force_nearest_d4(block, radius=5)
        assert decoded.decoded == brute_point
        assert round(decoded.distance, 8) == round(brute_distance, 8)


def test_general_dn_decoder() -> None:
    module = load_module()

    result = module.nearest_dn((0.6, 0.6, 0.6))
    assert result.rounded == (1, 1, 1)
    assert result.repaired_coordinate == 0
    assert result.decoded == (0, 1, 1)
    assert module.is_in_dn(result.decoded)


def test_validation() -> None:
    module = load_module()

    try:
        module.nearest_d4((1.0, 2.0))
    except ValueError as error:
        assert "length 4" in str(error)
    else:
        raise AssertionError("nearest_d4 should reject non-4D vectors")


if __name__ == "__main__":
    test_running_block_decoding()
    test_decoder_matches_bounded_brute_force()
    test_general_dn_decoder()
    test_validation()

