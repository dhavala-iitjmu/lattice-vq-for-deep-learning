from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_02_modulo.py"


def load_module():
    spec = importlib.util.spec_from_file_location("chapter_02_modulo", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_integer_mod_examples() -> None:
    module = load_module()

    assert module.quotient_and_remainder(17, 4) == (4, 1)
    assert module.quotient_and_remainder(-7, 4) == (-2, 1)
    assert module.integer_mod(17, 4) == 1
    assert module.integer_mod(-7, 4) == 1


def test_group_by_remainder() -> None:
    module = load_module()

    buckets = module.group_by_remainder(range(-8, 10), 4)
    assert set(buckets) == {0, 1, 2, 3}
    assert -8 in buckets[0]
    assert -7 in buckets[1]
    assert -6 in buckets[2]
    assert -5 in buckets[3]
    assert 9 in buckets[1]


def test_vector_mod_running_blocks() -> None:
    module = load_module()

    assert module.vector_mod((1, -2, 2, 0), 2) == (1, 0, 0, 0)
    assert module.vector_mod((1, 0, -2, 3), 2) == (1, 0, 0, 1)
    assert module.running_block_signatures() == ((1, 0, 0, 0), (1, 0, 0, 1))


def test_binary_patterns() -> None:
    module = load_module()

    patterns = module.binary_patterns(4)
    assert len(patterns) == 16
    assert (0, 0, 0, 0) in patterns
    assert (1, 1, 1, 1) in patterns


if __name__ == "__main__":
    test_integer_mod_examples()
    test_group_by_remainder()
    test_vector_mod_running_blocks()
    test_binary_patterns()

