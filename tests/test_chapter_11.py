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


def test_lookup_matches_reconstruction() -> None:
    m = load("chapter_11_one_sided_lut")
    ex = m.build_example()
    b1, b2 = ex.block_results
    assert b1.indices == (14, 0, 4, 4)
    assert round(b1.lookup_dot, 4) == -4.5
    assert round(b1.reconstruct_dot, 4) == -4.5
    assert b2.indices == (12, 13, 2, 2)
    assert round(b2.lookup_dot, 4) == -10.0
    assert round(b2.reconstruct_dot, 4) == -10.0
    assert round(ex.hnlq_dot, 4) == -14.5
    assert round(ex.original_dot, 2) == -13.41
    assert round(ex.dot_error, 4) == -1.09


def test_selected_table_entries() -> None:
    m = load("chapter_11_one_sided_lut")
    t1 = m.build_lut((2, 1, -1, 3))
    assert t1[14] == -1.0
    assert t1[0] == 0.0
    assert t1[4] == 2.0
    t2 = m.build_lut((-2, 0.5, 1, -1.5))
    assert t2[12] == -3.0
    assert t2[13] == -3.5
    assert t2[2] == 2.5


if __name__ == "__main__":
    test_lookup_matches_reconstruction()
    test_selected_table_entries()
