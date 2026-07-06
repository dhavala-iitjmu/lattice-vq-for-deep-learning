from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_18_binary_domain.py"


def load_module():
    if str(MODULE_PATH.parent) not in sys.path:
        sys.path.insert(0, str(MODULE_PATH.parent))
    spec = importlib.util.spec_from_file_location("chapter_18_binary_domain", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_bitplane_dot_matches_ordinary_dot() -> None:
    module = load_module()
    example = module.build_example()

    assert example.ordinary_dot == 13.0
    assert example.bitplane_dot == 13.0
    assert [c.contribution for c in example.contributions] == [5.0, 4.0, -4.0, 8.0]


def test_evidence_labels() -> None:
    module = load_module()
    example = module.build_example()

    assert example.evidence_labels["bitplane_dot_identity"] == "established"
    assert example.evidence_labels["hnlq_lut_dot_identity"] == "established"
    assert example.evidence_labels["structured_bitplane_kernel"] == "experimental"
    assert example.evidence_labels["binary_domain_gemm"] == "speculative"


def test_validation() -> None:
    module = load_module()

    try:
        module.label_claim("unknown")
    except ValueError as error:
        assert "unknown claim" in str(error)
    else:
        raise AssertionError("label_claim should reject unknown claims")


if __name__ == "__main__":
    test_bitplane_dot_matches_ordinary_dot()
    test_evidence_labels()
    test_validation()
