from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_06_d4.py"


def load_module():
    spec = importlib.util.spec_from_file_location("chapter_06_d4", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_membership_examples() -> None:
    module = load_module()

    assert module.is_in_d4((1, -2, 2, 0)) is False
    assert module.is_in_d4((1, 0, -2, 3)) is True
    assert module.is_in_d4((2, -2, 2, 0)) is True
    assert module.is_in_d4((0, 0, 0, 0)) is True
    assert module.is_in_d4((1.0, 0, 0, 1)) is True
    assert module.is_in_d4((1.5, 0.5, 0, 0)) is False
    assert module.is_in_d4((0.73, -1.84, 2.11, -0.45)) is False


def test_generator_representation() -> None:
    module = load_module()

    coefficients = module.coefficients_for_d4_vector((1, 0, -2, 3))
    assert coefficients == (1, 1, -2, 1)
    assert module.generate_d4_point(coefficients) == (1, 0, -2, 3)

    coefficients = module.coefficients_for_d4_vector((2, -2, 2, 0))
    assert coefficients == (2, 0, 1, 1)
    assert module.generate_d4_point(coefficients) == (2, -2, 2, 0)


def test_parity_signatures_and_cosets() -> None:
    module = load_module()
    patterns = module.even_parity_patterns()

    assert len(patterns) == 8
    assert (0, 0, 0, 0) in patterns
    assert (1, 1, 1, 1) in patterns
    assert (1, 0, 0, 0) not in patterns
    assert module.parity_signature((1, 0, -2, 3)) == (1, 0, 0, 1)
    assert module.coset_representative_mod_2z4((1, 0, -2, 3)) == (1, 0, 0, 1)


def test_build_example() -> None:
    module = load_module()
    example = module.build_example()

    assert example.membership == (False, True)
    assert example.generated_running_coefficients == (1, 1, -2, 1)
    assert example.generated_running_block == (1, 0, -2, 3)
    assert example.parity_signatures == ((1, 0, 0, 0), (1, 0, 0, 1))


if __name__ == "__main__":
    test_membership_examples()
    test_generator_representation()
    test_parity_signatures_and_cosets()
    test_build_example()

