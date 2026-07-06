from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_15_barnes_wall.py"


def load_module():
    if str(MODULE_PATH.parent) not in sys.path:
        sys.path.insert(0, str(MODULE_PATH.parent))
    spec = importlib.util.spec_from_file_location("chapter_15_barnes_wall", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_running_example() -> None:
    module = load_module()
    example = module.build_example()

    assert example.parity_membership is True
    assert example.generator_coefficients == (1, 1, -2, 1)
    assert example.regenerated == example.vector
    assert example.pairwise_r == (1, 1, 1, -5)


def test_pairwise_r_roundtrip() -> None:
    module = load_module()
    vector = (1, 0, -2, 3, 4, -1, 2, 2)
    transformed = module.pairwise_r_transform(vector)
    assert module.inverse_pairwise_r_transform(transformed) == tuple(float(value) for value in vector)


def test_hierarchy_and_validation() -> None:
    module = load_module()

    assert module.barnes_wall_hierarchy()[2] == (4, "D4-like parity structure")
    try:
        module.pairwise_r_transform((1, 2, 3))
    except ValueError as error:
        assert "even length" in str(error)
    else:
        raise AssertionError("pairwise_r_transform should reject odd length")


if __name__ == "__main__":
    test_running_example()
    test_pairwise_r_roundtrip()
    test_hierarchy_and_validation()
