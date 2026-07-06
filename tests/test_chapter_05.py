from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_05_lattices.py"


def load_module():
    spec = importlib.util.spec_from_file_location("chapter_05_lattices", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_matrix_vector_multiply_and_area() -> None:
    module = load_module()

    assert module.matrix_vector_multiply(module.Z2_GENERATOR, (2, -3)) == (2.0, -3.0)
    hex_point = module.matrix_vector_multiply(module.HEX_GENERATOR, (2, -2))
    assert tuple(round(value, 4) for value in hex_point) == (1.0, -1.7321)
    assert module.fundamental_area_2d(module.Z2_GENERATOR) == 1.0
    assert round(module.fundamental_area_2d(module.HEX_GENERATOR), 4) == 0.866


def test_generate_lattice_points_count() -> None:
    module = load_module()

    points = module.generate_lattice_points(module.Z2_GENERATOR, radius=2)
    assert len(points) == 25
    assert ((0, 0), (0.0, 0.0)) in points
    assert ((2, -2), (2.0, -2.0)) in points


def test_nearest_generated_points() -> None:
    module = load_module()
    example = module.build_example()

    assert example.z2_nearest.coefficients == (1, -2)
    assert example.z2_nearest.point == (1.0, -2.0)
    assert round(example.z2_nearest.distance, 4) == 0.3138
    assert example.hex_nearest.coefficients == (2, -2)
    assert tuple(round(value, 4) for value in example.hex_nearest.point) == (1.0, -1.7321)
    assert round(example.hex_nearest.distance, 4) == 0.2908


def test_d4_preview_membership() -> None:
    module = load_module()
    example = module.build_example()

    assert example.d4_preview_membership == (False, True)
    assert module.d4_parity_preview((0, 0, 0, 0)) is True
    assert module.d4_parity_preview((1, 0, 0, 0)) is False


if __name__ == "__main__":
    test_matrix_vector_multiply_and_area()
    test_generate_lattice_points_count()
    test_nearest_generated_points()
    test_d4_preview_membership()

