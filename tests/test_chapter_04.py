from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "code" / "python" / "chapter_04_vector_quantization.py"


def load_module():
    spec = importlib.util.spec_from_file_location("chapter_04_vector_quantization", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_codebook_shape_and_rate() -> None:
    module = load_module()
    codebook = module.build_codebook()
    example = module.build_example()

    assert len(codebook) == 256
    assert len(codebook[0]) == 4
    assert example.bits_per_block == 8
    assert example.bits_per_weight == 2.0


def test_encoding_and_decoding_running_blocks() -> None:
    module = load_module()
    codebook = module.build_codebook()
    example = module.build_example()

    assert example.indices == (137, 147)
    assert module.decode_index(137, codebook) == (1, -2, 2, 0)
    assert module.decode_index(147, codebook) == (1, 0, -2, 3)
    assert example.reconstructions == ((1, -2, 2, 0), (1, 0, -2, 3))


def test_distortion_values() -> None:
    module = load_module()
    example = module.build_example()

    assert tuple(round(value, 4) for value in example.squared_errors) == (0.3131, 0.2285)
    assert tuple(round(value, 2) for value in example.distances) == (0.56, 0.48)
    assert round(example.mean_squared_error, 4) == 0.0677


def test_top_k_nearest() -> None:
    module = load_module()
    codebook = module.build_codebook()
    top_three = module.top_k_nearest(module.BLOCKS[0], codebook, 3)

    assert [entry[0] for entry in top_three] == [137, 73, 141]
    assert top_three[0][1] == (1, -2, 2, 0)
    assert round(top_three[0][2], 2) == 0.56


if __name__ == "__main__":
    test_codebook_shape_and_rate()
    test_encoding_and_decoding_running_blocks()
    test_distortion_values()
    test_top_k_nearest()

