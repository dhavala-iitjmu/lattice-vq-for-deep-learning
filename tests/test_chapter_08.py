from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_08_lattice_quantization.py"


def load_module():
    if str(MODULE_PATH.parent) not in sys.path:
        sys.path.insert(0, str(MODULE_PATH.parent))
    spec = importlib.util.spec_from_file_location("chapter_08_lattice_quantization", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_scaled_quantization_matches_chapter_7_at_beta_1() -> None:
    module = load_module()
    example = module.build_example()
    beta_1 = example.results_by_beta[1.0]

    assert beta_1[0].lattice_point == (1, -2, 2, -1)
    assert beta_1[0].reconstruction == (1.0, -2.0, 2.0, -1.0)
    assert round(beta_1[0].distance, 4) == 0.6427
    assert beta_1[1].lattice_point == (1, 0, -2, 3)
    assert beta_1[1].reconstruction == (1.0, 0.0, -2.0, 3.0)
    assert round(beta_1[1].distance, 4) == 0.4780


def test_finer_scale_reduces_example_mse() -> None:
    module = load_module()
    example = module.build_example()

    assert round(example.mse_by_beta[0.5], 4) == 0.3135
    assert round(example.mse_by_beta[1.0], 4) == 0.1002
    assert round(example.mse_by_beta[2.0], 4) == 0.0302
    assert example.mse_by_beta[0.5] > example.mse_by_beta[1.0] > example.mse_by_beta[2.0]


def test_beta_2_running_weight_reconstruction() -> None:
    module = load_module()
    example = module.build_example()

    assert example.results_by_beta[2.0][0].lattice_point == (1, -4, 4, -1)
    assert example.results_by_beta[2.0][0].reconstruction == (0.5, -2.0, 2.0, -0.5)
    assert round(example.results_by_beta[2.0][0].squared_error, 4) == 0.0931
    assert example.running_weight_reconstruction_beta_2 == (
        0.5,
        -2.0,
        2.0,
        -0.5,
        1.5,
        0.0,
        -2.5,
        3.0,
    )


def test_scaled_lattice_ray_is_unbounded_prefix() -> None:
    module = load_module()

    assert module.scaled_d4_ray(beta=2.0, count=5) == (
        (0.0, 0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 0.0),
        (2.0, 0.0, 0.0, 0.0),
        (3.0, 0.0, 0.0, 0.0),
        (4.0, 0.0, 0.0, 0.0),
    )


def test_validation() -> None:
    module = load_module()

    try:
        module.scaled_nearest_d4_quantize((1.0, 2.0), beta=1.0)
    except ValueError as error:
        assert "length 4" in str(error)
    else:
        raise AssertionError("scaled_nearest_d4_quantize should reject non-4D vectors")

    try:
        module.scaled_nearest_d4_quantize((1.0, 2.0, 3.0, 4.0), beta=0.0)
    except ValueError as error:
        assert "positive" in str(error)
    else:
        raise AssertionError("scaled_nearest_d4_quantize should reject nonpositive beta")


if __name__ == "__main__":
    test_scaled_quantization_matches_chapter_7_at_beta_1()
    test_finer_scale_reduces_example_mse()
    test_beta_2_running_weight_reconstruction()
    test_scaled_lattice_ray_is_unbounded_prefix()
    test_validation()
