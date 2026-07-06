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


def test_lut_matvec_matches_reconstruction() -> None:
    m = load("chapter_12_hnlq_matmul")
    ex = m.build_example()
    assert ex.output_from_lut == ex.output_from_reconstruction
    assert round(ex.output_from_lut[0], 4) == -14.5
    assert ex.activation_table_count == 2
    assert ex.traffic.hnlq_indices == 64
    assert ex.traffic.reconstructed_weight_values == 64
    assert ex.traffic.lut_entries == 32


if __name__ == "__main__":
    test_lut_matvec_matches_reconstruction()
