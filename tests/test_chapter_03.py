from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_03_geometry.py"


def load_module():
    spec = importlib.util.spec_from_file_location("chapter_03_geometry", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_norms_distances_and_dot_products() -> None:
    module = load_module()
    example = module.build_example()

    assert round(example.weight_norm, 2) == 5.06
    assert round(example.activation_norm, 2) == 4.74
    assert round(example.quantized_weight_norm, 2) == 4.80
    assert round(example.quantization_error_norm, 2) == 0.74
    assert tuple(round(value, 2) for value in example.block_distances) == (0.56, 0.48)
    assert round(example.original_dot, 2) == -13.41
    assert round(example.quantized_dot, 2) == -10.50
    assert round(example.dot_error, 2) == 2.91


def test_cosine_and_angle() -> None:
    module = load_module()
    example = module.build_example()

    assert round(example.cosine_similarity, 3) == -0.559
    assert round(example.angle_degrees, 2) == 123.95


def test_nearest_neighbor() -> None:
    module = load_module()

    block_1 = module.WEIGHTS[:4]
    block_2 = module.WEIGHTS[4:]
    nearest_1 = module.nearest_neighbor(block_1, module.CODEBOOK)
    nearest_2 = module.nearest_neighbor(block_2, module.CODEBOOK)

    assert nearest_1[0] == 1
    assert round(nearest_1[1], 2) == 0.56
    assert nearest_2[0] == 2
    assert round(nearest_2[1], 2) == 0.48


def test_dimension_checks() -> None:
    module = load_module()

    try:
        module.euclidean_distance((1.0, 2.0), (1.0,))
    except ValueError as error:
        assert "equal length" in str(error)
    else:
        raise AssertionError("expected euclidean_distance to reject mismatched dimensions")


if __name__ == "__main__":
    test_norms_distances_and_dot_products()
    test_cosine_and_angle()
    test_nearest_neighbor()
    test_dimension_checks()

