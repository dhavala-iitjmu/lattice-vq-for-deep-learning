from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code" / "python"


def load(name: str):
    if str(CODE) not in sys.path:
        sys.path.insert(0, str(CODE))
    spec = importlib.util.spec_from_file_location(name, CODE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_digit_encoding_running_blocks() -> None:
    m = load("chapter_10_hnlq")
    ex = m.build_example()
    b1, b2 = ex.running_encodings

    assert b1.lattice_point == (1, -4, 4, -1)
    assert b1.coefficients == (1, -3, 1, 0)
    assert b1.indices == (14, 0, 4, 4)
    assert b1.reconstruction == (0.5, -2.0, 2.0, -0.5)
    assert round(b1.squared_error, 4) == 0.0931
    assert b1.overloaded is False

    assert b2.lattice_point == (3, 0, -5, 6)
    assert b2.coefficients == (3, 3, -4, 2)
    assert b2.indices == (12, 13, 2, 2)
    assert b2.reconstruction == (1.5, 0.0, -2.5, 3.0)
    assert round(b2.squared_error, 4) == 0.0985
    assert b2.overloaded is False


def test_decode_is_exact_within_range() -> None:
    m = load("chapter_10_hnlq")
    for z in ((0, 0, 0, 0), (1, -3, 1, 0), (3, 3, -4, 2), (-8, 7, -8, 7), (5, -1, 2, -6)):
        indices = m.coefficients_to_indices(z)
        assert m.indices_to_coefficients(indices) == z


def test_beta_sweep_shape_and_overload_demo() -> None:
    m = load("chapter_10_hnlq")
    ex = m.build_example()
    assert ex.effective_codebook_size == 65536
    sweep = {beta: (round(mse, 4), ov) for beta, mse, ov in ex.beta_sweep}
    assert sweep[0.5] == (0.2727, 0)
    assert sweep[1.0] == (0.0802, 0)
    assert sweep[2.0] == (0.0239, 0)
    assert sweep[4.0] == (0.0077, 1)
    assert sweep[8.0][1] == 2
    assert sweep[8.0][0] > sweep[4.0][0]
    demo = ex.overload_demo
    assert demo.coefficients == (10, 10, -17, 8)
    assert demo.clamped_coefficients == (7, 7, -8, 7)
    assert demo.overloaded is True


def test_minnorm_cycle() -> None:
    m = load("chapter_10_hnlq")
    ch9 = load("chapter_09_quotient_codebooks")
    codebook = {entry.index: entry.representative for entry in ch9.generate_a2_d4()}
    trace = m.minnorm_digit_attempt((0, -1, 1, 0), codebook, steps=4)
    assert trace[1] == (0, -1, 1, 0)
    assert trace[-1] == (0, -1, 1, 0)


if __name__ == "__main__":
    test_digit_encoding_running_blocks()
    test_decode_is_exact_within_range()
    test_beta_sweep_shape_and_overload_demo()
    test_minnorm_cycle()
