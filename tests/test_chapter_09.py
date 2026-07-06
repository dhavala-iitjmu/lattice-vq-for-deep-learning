from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_09_quotient_codebooks.py"


def load_module():
    if str(MODULE_PATH.parent) not in sys.path:
        sys.path.insert(0, str(MODULE_PATH.parent))
    spec = importlib.util.spec_from_file_location("chapter_09_quotient_codebooks", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_a2_codebook_shape_and_entries() -> None:
    module = load_module()
    codebook = module.generate_a2_d4()

    assert len(codebook) == 16
    assert tuple(entry.index for entry in codebook) == tuple(range(16))
    assert codebook[0].bits == (0, 0, 0, 0)
    assert codebook[0].representative == (0, 0, 0, 0)
    assert codebook[13].bits == (1, 1, 0, 1)
    assert codebook[13].representative == (1, 0, 0, 1)
    assert codebook[14].bits == (1, 1, 1, 0)
    assert codebook[14].representative == (1, 0, 0, -1)


def test_representatives_are_valid_unique_cosets() -> None:
    module = load_module()
    codebook = module.generate_a2_d4()

    assert all(module.is_in_scaled_d4(entry.representative, q=1) for entry in codebook)
    assert all(module.in_closed_scaled_voronoi(entry.representative) for entry in codebook)
    assert len({entry.bits for entry in codebook}) == 16
    assert len({entry.representative for entry in codebook}) == 16
    assert not module.same_coset_mod_qd4(codebook[13].representative, codebook[14].representative)


def test_running_lattice_point_reductions() -> None:
    module = load_module()
    example = module.build_example()
    first, second = example.reductions

    assert first.lattice_point == (1, -2, 2, -1)
    assert first.coefficients == (1, -1, 1, 0)
    assert first.bits == (1, 1, 1, 0)
    assert first.index == 14
    assert first.representative == (1, 0, 0, -1)
    assert first.coarse_difference == (0, -2, 2, 0)
    assert module.is_in_scaled_d4(first.coarse_difference, q=2)

    assert second.lattice_point == (1, 0, -2, 3)
    assert second.coefficients == (1, 1, -2, 1)
    assert second.bits == (1, 1, 0, 1)
    assert second.index == 13
    assert second.representative == (1, 0, 0, 1)
    assert second.coarse_difference == (0, 0, -2, 2)
    assert module.is_in_scaled_d4(second.coarse_difference, q=2)


def test_nearest_representative_search() -> None:
    module = load_module()
    codebook = module.generate_a2_d4()

    first = module.nearest_representative((0.73, -1.84, 2.11, -0.45), codebook)
    second = module.nearest_representative((1.27, 0.08, -2.36, 3.14), codebook)

    assert first.index == 15
    assert first.representative == (1, 0, 1, 0)
    assert round(first.distance, 4) == 2.2120
    assert second.index == 13
    assert second.representative == (1, 0, 0, 1)
    assert round(second.distance, 4) == 3.1982


def test_bit_index_roundtrip_and_validation() -> None:
    module = load_module()

    for index in range(16):
        assert module.bits_to_index(module.index_to_bits(index)) == index

    try:
        module.index_to_bits(16)
    except ValueError as error:
        assert "[0, 15]" in str(error)
    else:
        raise AssertionError("index_to_bits should reject out-of-range indices")

    try:
        module.bits_to_index((0, 1, 2, 0))
    except ValueError as error:
        assert "0 and 1" in str(error)
    else:
        raise AssertionError("bits_to_index should reject non-bits")


if __name__ == "__main__":
    test_a2_codebook_shape_and_entries()
    test_representatives_are_valid_unique_cosets()
    test_running_lattice_point_reductions()
    test_nearest_representative_search()
    test_bit_index_roundtrip_and_validation()
