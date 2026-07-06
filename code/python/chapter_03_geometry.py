"""Reference geometry examples for Chapter 3."""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, degrees, sqrt


WEIGHTS = (0.73, -1.84, 2.11, -0.45, 1.27, 0.08, -2.36, 3.14)
ACTIVATIONS = (2.0, 1.0, -1.0, 3.0, -2.0, 0.5, 1.0, -1.5)
QUANTIZED_WEIGHTS = (1, -2, 2, 0, 1, 0, -2, 3)
CODEBOOK = (
    (0, 0, 0, 0),
    (1, -2, 2, 0),
    (1, 0, -2, 3),
    (1, -1, 2, -1),
)


@dataclass(frozen=True)
class GeometryExample:
    weight_norm: float
    activation_norm: float
    quantized_weight_norm: float
    quantization_error_norm: float
    block_distances: tuple[float, float]
    original_dot: float
    quantized_dot: float
    dot_error: float
    cosine_similarity: float
    angle_degrees: float
    nearest_indices: tuple[int, int]


def dot(left: tuple[float, ...] | tuple[int, ...], right: tuple[float, ...] | tuple[int, ...]) -> float:
    """Compute a dot product."""

    if len(left) != len(right):
        raise ValueError("dot product requires vectors of equal length")
    return sum(a * b for a, b in zip(left, right))


def squared_norm(vector: tuple[float, ...] | tuple[int, ...]) -> float:
    """Compute squared Euclidean norm."""

    return dot(vector, vector)


def l2_norm(vector: tuple[float, ...] | tuple[int, ...]) -> float:
    """Compute Euclidean norm."""

    return sqrt(squared_norm(vector))


def squared_euclidean_distance(
    left: tuple[float, ...] | tuple[int, ...],
    right: tuple[float, ...] | tuple[int, ...],
) -> float:
    """Compute squared Euclidean distance."""

    if len(left) != len(right):
        raise ValueError("distance requires vectors of equal length")
    return sum((a - b) ** 2 for a, b in zip(left, right))


def euclidean_distance(
    left: tuple[float, ...] | tuple[int, ...],
    right: tuple[float, ...] | tuple[int, ...],
) -> float:
    """Compute Euclidean distance."""

    return sqrt(squared_euclidean_distance(left, right))


def cosine_similarity(
    left: tuple[float, ...] | tuple[int, ...],
    right: tuple[float, ...] | tuple[int, ...],
) -> float:
    """Compute cosine similarity."""

    denominator = l2_norm(left) * l2_norm(right)
    if denominator == 0:
        raise ValueError("cosine similarity is undefined for zero vectors")
    return dot(left, right) / denominator


def angle_degrees(
    left: tuple[float, ...] | tuple[int, ...],
    right: tuple[float, ...] | tuple[int, ...],
) -> float:
    """Return the angle between two vectors in degrees."""

    cosine = max(-1.0, min(1.0, cosine_similarity(left, right)))
    return degrees(acos(cosine))


def nearest_neighbor(
    target: tuple[float, ...],
    candidates: tuple[tuple[int, ...], ...],
) -> tuple[int, float]:
    """Return the index and distance of the nearest candidate."""

    if not candidates:
        raise ValueError("nearest_neighbor requires at least one candidate")

    best_index = 0
    best_squared_distance = squared_euclidean_distance(target, candidates[0])
    for index, candidate in enumerate(candidates[1:], start=1):
        squared_distance = squared_euclidean_distance(target, candidate)
        if squared_distance < best_squared_distance:
            best_index = index
            best_squared_distance = squared_distance
    return best_index, sqrt(best_squared_distance)


def build_example() -> GeometryExample:
    block_1 = WEIGHTS[:4]
    block_2 = WEIGHTS[4:]
    quantized_block_1 = QUANTIZED_WEIGHTS[:4]
    quantized_block_2 = QUANTIZED_WEIGHTS[4:]
    original_dot = dot(WEIGHTS, ACTIVATIONS)
    quantized_dot = dot(QUANTIZED_WEIGHTS, ACTIVATIONS)
    nearest_1, _ = nearest_neighbor(block_1, CODEBOOK)
    nearest_2, _ = nearest_neighbor(block_2, CODEBOOK)

    return GeometryExample(
        weight_norm=l2_norm(WEIGHTS),
        activation_norm=l2_norm(ACTIVATIONS),
        quantized_weight_norm=l2_norm(QUANTIZED_WEIGHTS),
        quantization_error_norm=euclidean_distance(WEIGHTS, QUANTIZED_WEIGHTS),
        block_distances=(
            euclidean_distance(block_1, quantized_block_1),
            euclidean_distance(block_2, quantized_block_2),
        ),
        original_dot=original_dot,
        quantized_dot=quantized_dot,
        dot_error=quantized_dot - original_dot,
        cosine_similarity=cosine_similarity(WEIGHTS, ACTIVATIONS),
        angle_degrees=angle_degrees(WEIGHTS, ACTIVATIONS),
        nearest_indices=(nearest_1, nearest_2),
    )


def main() -> None:
    example = build_example()
    print(f"||w||_2                 = {example.weight_norm:.2f}")
    print(f"||x||_2                 = {example.activation_norm:.2f}")
    print(f"||hat(w)||_2            = {example.quantized_weight_norm:.2f}")
    print(f"||hat(w) - w||_2        = {example.quantization_error_norm:.2f}")
    print(f"block distances         = {[round(value, 2) for value in example.block_distances]}")
    print(f"w^T x                   = {example.original_dot:.2f}")
    print(f"hat(w)^T x              = {example.quantized_dot:.2f}")
    print(f"dot-product error       = {example.dot_error:.2f}")
    print(f"cosine similarity       = {example.cosine_similarity:.3f}")
    print(f"angle between w and x   = {example.angle_degrees:.2f} degrees")
    print(f"nearest codeword indices = {example.nearest_indices}")


if __name__ == "__main__":
    main()

