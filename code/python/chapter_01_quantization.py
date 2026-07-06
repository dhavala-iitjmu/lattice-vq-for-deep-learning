"""Numerical example for Chapter 1.

The values here are the canonical Chapter 1 running example. Keep this file
small and explicit so readers can verify the arithmetic by inspection.
"""

from __future__ import annotations

from dataclasses import dataclass


WEIGHTS = (0.73, -1.84, 2.11, -0.45, 1.27, 0.08, -2.36, 3.14)
ACTIVATIONS = (2.0, 1.0, -1.0, 3.0, -2.0, 0.5, 1.0, -1.5)


@dataclass(frozen=True)
class QuantizationExample:
    weights: tuple[float, ...]
    activations: tuple[float, ...]
    quantized_weights: tuple[int, ...]
    original_dot: float
    quantized_dot: float
    dot_error: float
    fp16_bits: int
    int4_bits: int


def scalar_quantize(values: tuple[float, ...]) -> tuple[int, ...]:
    """Round each coordinate independently to the nearest integer."""

    return tuple(round(value) for value in values)


def dot(left: tuple[float, ...] | tuple[int, ...], right: tuple[float, ...]) -> float:
    """Compute a dot product using ordinary Python arithmetic."""

    if len(left) != len(right):
        raise ValueError("dot product requires vectors of equal length")
    return sum(a * b for a, b in zip(left, right))


def build_example() -> QuantizationExample:
    quantized_weights = scalar_quantize(WEIGHTS)
    original_dot = dot(WEIGHTS, ACTIVATIONS)
    quantized_dot = dot(quantized_weights, ACTIVATIONS)
    return QuantizationExample(
        weights=WEIGHTS,
        activations=ACTIVATIONS,
        quantized_weights=quantized_weights,
        original_dot=original_dot,
        quantized_dot=quantized_dot,
        dot_error=quantized_dot - original_dot,
        fp16_bits=len(WEIGHTS) * 16,
        int4_bits=len(WEIGHTS) * 4,
    )


def main() -> None:
    example = build_example()
    print(f"w                 = {example.weights}")
    print(f"x                 = {example.activations}")
    print(f"hat(w)            = {example.quantized_weights}")
    print(f"w^T x             = {example.original_dot:.2f}")
    print(f"hat(w)^T x        = {example.quantized_dot:.2f}")
    print(f"dot-product error = {example.dot_error:.2f}")
    print(f"FP16 bits         = {example.fp16_bits}")
    print(f"int4 bits         = {example.int4_bits}")


if __name__ == "__main__":
    main()

