"""Reference implementation for Chapter 4: classical vector quantization."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import ceil, log2, sqrt


BLOCKS = (
    (0.73, -1.84, 2.11, -0.45),
    (1.27, 0.08, -2.36, 3.14),
)

LEVELS = (
    (-2, 0, 1, 3),
    (-2, 0, 1, 3),
    (-2, 0, 2, 3),
    (-2, 0, 1, 3),
)


@dataclass(frozen=True)
class VectorQuantizationExample:
    codebook_size: int
    dimension: int
    bits_per_block: int
    bits_per_weight: float
    indices: tuple[int, ...]
    reconstructions: tuple[tuple[int, ...], ...]
    squared_errors: tuple[float, ...]
    distances: tuple[float, ...]
    mean_squared_error: float


def build_codebook() -> tuple[tuple[int, ...], ...]:
    """Build the deterministic 256-entry Chapter 4 codebook."""

    return tuple(product(*LEVELS))


def squared_euclidean_distance(
    left: tuple[float, ...] | tuple[int, ...],
    right: tuple[float, ...] | tuple[int, ...],
) -> float:
    """Compute squared Euclidean distance."""

    if len(left) != len(right):
        raise ValueError("distance requires vectors of equal length")
    return sum((a - b) ** 2 for a, b in zip(left, right))


def encode_nearest(
    vector: tuple[float, ...],
    codebook: tuple[tuple[int, ...], ...],
) -> int:
    """Return the index of the nearest codeword."""

    if not codebook:
        raise ValueError("codebook must not be empty")
    best_index = 0
    best_distance = squared_euclidean_distance(vector, codebook[0])
    for index, codeword in enumerate(codebook[1:], start=1):
        distance = squared_euclidean_distance(vector, codeword)
        if distance < best_distance:
            best_index = index
            best_distance = distance
    return best_index


def decode_index(index: int, codebook: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    """Decode one codebook index."""

    if index < 0 or index >= len(codebook):
        raise IndexError("codebook index out of range")
    return codebook[index]


def encode_blocks(
    blocks: tuple[tuple[float, ...], ...],
    codebook: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    """Encode all blocks using nearest-codeword search."""

    return tuple(encode_nearest(block, codebook) for block in blocks)


def decode_indices(
    indices: tuple[int, ...],
    codebook: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """Decode a sequence of codebook indices."""

    return tuple(decode_index(index, codebook) for index in indices)


def bits_per_block(codebook_size: int) -> int:
    """Return the number of bits required to store one codebook index."""

    if codebook_size <= 1:
        return 0
    return ceil(log2(codebook_size))


def build_example() -> VectorQuantizationExample:
    codebook = build_codebook()
    dimension = len(codebook[0])
    indices = encode_blocks(BLOCKS, codebook)
    reconstructions = decode_indices(indices, codebook)
    squared_errors = tuple(
        squared_euclidean_distance(block, reconstruction)
        for block, reconstruction in zip(BLOCKS, reconstructions)
    )
    distances = tuple(sqrt(error) for error in squared_errors)
    total_coordinates = len(BLOCKS) * dimension
    index_bits = bits_per_block(len(codebook))
    return VectorQuantizationExample(
        codebook_size=len(codebook),
        dimension=dimension,
        bits_per_block=index_bits,
        bits_per_weight=index_bits / dimension,
        indices=indices,
        reconstructions=reconstructions,
        squared_errors=squared_errors,
        distances=distances,
        mean_squared_error=sum(squared_errors) / total_coordinates,
    )


def top_k_nearest(
    vector: tuple[float, ...],
    codebook: tuple[tuple[int, ...], ...],
    k: int,
) -> tuple[tuple[int, tuple[int, ...], float], ...]:
    """Return the k nearest codewords as index, codeword, distance triples."""

    if k <= 0:
        raise ValueError("k must be positive")
    distances = sorted(
        (
            (index, codeword, sqrt(squared_euclidean_distance(vector, codeword)))
            for index, codeword in enumerate(codebook)
        ),
        key=lambda item: item[2],
    )
    return tuple(distances[:k])


def main() -> None:
    codebook = build_codebook()
    example = build_example()
    print(f"codebook size       = {example.codebook_size}")
    print(f"dimension           = {example.dimension}")
    print(f"bits per block      = {example.bits_per_block}")
    print(f"bits per weight     = {example.bits_per_weight:.2f}")
    print(f"encoded indices     = {example.indices}")
    print(f"reconstructions     = {example.reconstructions}")
    print(f"distances           = {[round(value, 2) for value in example.distances]}")
    print(f"squared errors      = {[round(value, 4) for value in example.squared_errors]}")
    print(f"mean squared error  = {example.mean_squared_error:.4f}")
    print("nearest codewords for block 1:")
    for index, codeword, distance in top_k_nearest(BLOCKS[0], codebook, 3):
        print(f"  {index:3d}: {codeword}, distance={distance:.2f}")


if __name__ == "__main__":
    main()

