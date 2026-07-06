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


def test_beta_sweep() -> None:
    m = load("chapter_13_hnlq_practice")
    ex = m.build_example()
    table = {r.beta: (round(r.weight_mse, 4), round(r.output_mse, 4), r.overloaded_blocks) for r in ex.sweep}
    assert table[0.5] == (0.3087, 5.9559, 0)
    assert table[1.0] == (0.0987, 0.8513, 0)
    assert table[2.0] == (0.0300, 0.2610, 0)
    assert table[4.0] == (0.0334, 0.3494, 3)
    assert ex.best_by_weight_mse.beta == 2.0
    assert ex.best_by_output_mse.beta == 2.0
    assert ex.bits_per_weight == 4.0


def test_scalar_baseline_and_gaussian() -> None:
    m = load("chapter_13_hnlq_practice")
    ex = m.build_example()
    assert round(ex.scalar_baseline.weight_mse, 4) == 0.0278
    assert round(ex.scalar_baseline.output_mse, 4) == 0.0810
    g = ex.gaussian
    assert round(g.matched_density_ratio, 3) == 0.892
    assert round(g.matched_rate_ratio, 3) == 1.798
    assert g.matched_density_ratio < 1.0
    assert g.matched_rate_ratio > 1.0


if __name__ == "__main__":
    test_beta_sweep()
    test_scalar_baseline_and_gaussian()
