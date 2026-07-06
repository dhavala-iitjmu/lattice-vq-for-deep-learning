"""Reference implementation for Chapter 11: one-sided lookup tables."""

from __future__ import annotations

from dataclasses import dataclass

from chapter_01_quantization import ACTIVATIONS, WEIGHTS, dot
from chapter_10_hnlq import (
    DEFAULT_BETA,
    DEFAULT_Q,
    DIGIT_REPRESENTATIVES,
    RUNNING_BLOCKS,
    build_example as build_chapter_10_example,
    decode_indices,
    digit_weights,
)


Vector = tuple[float, ...]
IndexSequence = tuple[int, ...]


@dataclass(frozen=True)
class BlockLookupResult:
    activation_block: Vector
    indices: IndexSequence
    table: tuple[float, ...]
    lookup_dot: float
    reconstruct_dot: float


@dataclass(frozen=True)
class Chapter11Example:
    block_results: tuple[BlockLookupResult, BlockLookupResult]
    hnlq_dot: float
    reconstruct_dot: float
    original_dot: float
    dot_error: float


def split_blocks(vector: Vector, block_size: int = 4) -> tuple[Vector, ...]:
    """Split a vector into fixed-size blocks."""

    if block_size <= 0:
        raise ValueError("block_size must be positive")
    if len(vector) % block_size != 0:
        raise ValueError("vector length must be divisible by block_size")
    return tuple(
        tuple(vector[index : index + block_size])
        for index in range(0, len(vector), block_size)
    )


def build_lut(
    activation_block: Vector,
    representatives: tuple[tuple[int, ...], ...] = DIGIT_REPRESENTATIVES,
) -> tuple[float, ...]:
    """Build T_x(b) = x^T c~_b over the 16 digit representatives."""

    if len(activation_block) != 4:
        raise ValueError("activation_block must have length 4")
    return tuple(dot(activation_block, representative) for representative in representatives)


def hnlq_dot_from_lut(
    indices: IndexSequence,
    table: tuple[float, ...],
    beta: float = DEFAULT_BETA,
    q: int = DEFAULT_Q,
) -> float:
    """Compute one HNLQ block dot product from a one-sided LUT."""

    if beta <= 0:
        raise ValueError("beta must be positive")
    if q <= 1:
        raise ValueError("q must be greater than 1")
    if not indices:
        raise ValueError("indices must not be empty")
    weights = digit_weights(len(indices), q)
    total = 0.0
    for weight, index in zip(weights, indices):
        if index < 0 or index >= len(table):
            raise IndexError("lookup index out of range")
        total += weight * table[index]
    return total / beta


def reconstruct_then_dot(
    activation_block: Vector,
    indices: IndexSequence,
    beta: float = DEFAULT_BETA,
    q: int = DEFAULT_Q,
) -> float:
    """Decode a block and then compute its dot product."""

    reconstruction = decode_indices(indices, beta, q)
    return dot(activation_block, reconstruction)


def build_example() -> Chapter11Example:
    """Build the numerical example used in Chapter 11."""

    hnlq_example = build_chapter_10_example()
    activation_blocks = split_blocks(ACTIVATIONS)
    block_results = []
    for activation_block, encoding in zip(activation_blocks, hnlq_example.running_encodings):
        table = build_lut(activation_block)
        lookup_dot = hnlq_dot_from_lut(encoding.indices, table, encoding.beta, encoding.q)
        reconstruct_dot = reconstruct_then_dot(
            activation_block,
            encoding.indices,
            encoding.beta,
            encoding.q,
        )
        block_results.append(
            BlockLookupResult(
                activation_block=activation_block,
                indices=encoding.indices,
                table=table,
                lookup_dot=lookup_dot,
                reconstruct_dot=reconstruct_dot,
            )
        )

    hnlq_dot = sum(result.lookup_dot for result in block_results)
    reconstructed_dot = sum(result.reconstruct_dot for result in block_results)
    original_dot = dot(WEIGHTS, ACTIVATIONS)
    return Chapter11Example(
        block_results=tuple(block_results),  # type: ignore[arg-type]
        hnlq_dot=hnlq_dot,
        reconstruct_dot=reconstructed_dot,
        original_dot=original_dot,
        dot_error=hnlq_dot - original_dot,
    )


def build_example_from_chapter_10():
    """Isolate the Chapter 10 import so the public build_example name stays local."""

    return build_chapter_10_example()


def main() -> None:
    example = build_example()
    for index, result in enumerate(example.block_results, start=1):
        selected = [(entry, result.table[entry]) for entry in result.indices]
        print(f"block {index}")
        print(f"  indices          = {result.indices}")
        print(f"  selected entries = {selected}")
        print(f"  lookup dot       = {result.lookup_dot:.4f}")
        print(f"  reconstruct dot  = {result.reconstruct_dot:.4f}")
    print(f"HNLQ dot      = {example.hnlq_dot:.4f}")
    print(f"original dot  = {example.original_dot:.4f}")
    print(f"dot error     = {example.dot_error:.4f}")


if __name__ == "__main__":
    main()
