"""Reference implementation for Chapter 14: higher-dimensional lattices."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from chapter_01_quantization import WEIGHTS
from chapter_07_nearest_lattice import nearest_dn, squared_distance


Vector = tuple[float, ...]


@dataclass(frozen=True)
class E8DecodeResult:
    target: Vector
    d8_candidate: Vector
    shifted_candidate: Vector
    decoded: Vector
    d8_squared_error: float
    shifted_squared_error: float
    squared_error: float
    distance: float


@dataclass(frozen=True)
class Chapter14Example:
    d4_product_decoded: Vector
    d4_product_squared_error: float
    e8_result: E8DecodeResult


def nearest_e8(vector: Vector) -> E8DecodeResult:
    """Decode an eight-dimensional vector to E8 via two D8 decodes."""

    if len(vector) != 8:
        raise ValueError("nearest_e8 requires a vector of length 8")
    half = tuple(0.5 for _ in vector)
    d8_candidate = tuple(float(value) for value in nearest_dn(vector).decoded)
    shifted_target = tuple(value - 0.5 for value in vector)
    shifted_base = nearest_dn(shifted_target).decoded
    shifted_candidate = tuple(value + 0.5 for value in shifted_base)
    d8_error = squared_distance(vector, d8_candidate)
    shifted_error = squared_distance(vector, shifted_candidate)
    if d8_error <= shifted_error:
        decoded = d8_candidate
        error = d8_error
    else:
        decoded = shifted_candidate
        error = shifted_error
    return E8DecodeResult(
        target=vector,
        d8_candidate=d8_candidate,
        shifted_candidate=shifted_candidate,
        decoded=decoded,
        d8_squared_error=d8_error,
        shifted_squared_error=shifted_error,
        squared_error=error,
        distance=sqrt(error),
    )


def nearest_d4_product(vector: Vector) -> Vector:
    """Decode an eight-dimensional vector as two independent D4 blocks."""

    if len(vector) != 8:
        raise ValueError("nearest_d4_product requires a vector of length 8")
    return tuple(float(value) for value in nearest_dn(vector[:4]).decoded + nearest_dn(vector[4:]).decoded)


def build_example() -> Chapter14Example:
    vector = tuple(float(value) for value in WEIGHTS)
    d4_product = nearest_d4_product(vector)
    e8 = nearest_e8(vector)
    return Chapter14Example(
        d4_product_decoded=d4_product,
        d4_product_squared_error=squared_distance(vector, d4_product),
        e8_result=e8,
    )


def main() -> None:
    example = build_example()
    print(f"D4 x D4 decoded       = {example.d4_product_decoded}")
    print(f"D4 x D4 squared error = {example.d4_product_squared_error:.4f}")
    print(f"E8 D8 candidate       = {example.e8_result.d8_candidate}")
    print(f"E8 shifted candidate  = {example.e8_result.shifted_candidate}")
    print(f"E8 decoded            = {example.e8_result.decoded}")
    print(f"E8 squared error      = {example.e8_result.squared_error:.4f}")


if __name__ == "__main__":
    main()
