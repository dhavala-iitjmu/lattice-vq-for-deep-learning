"""Reference implementation for Chapter 5: lattice generation."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import sqrt


Matrix = tuple[tuple[float, ...], ...]
Vector = tuple[float, ...]
IntVector = tuple[int, ...]

Z2_GENERATOR: Matrix = ((1.0, 0.0), (0.0, 1.0))
HEX_GENERATOR: Matrix = ((1.0, 0.5), (0.0, sqrt(3.0) / 2.0))
VISIBLE_TARGET: Vector = (0.73, -1.84)


@dataclass(frozen=True)
class NearestGeneratedPoint:
    coefficients: IntVector
    point: Vector
    distance: float


@dataclass(frozen=True)
class LatticeExample:
    z2_nearest: NearestGeneratedPoint
    hex_nearest: NearestGeneratedPoint
    z2_area: float
    hex_area: float
    d4_preview_membership: tuple[bool, bool]


def matrix_vector_multiply(matrix: Matrix, vector: IntVector | Vector) -> Vector:
    """Multiply a matrix by a vector."""

    if not matrix:
        raise ValueError("matrix must not be empty")
    if len(matrix[0]) != len(vector):
        raise ValueError("matrix column count must match vector length")
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def determinant_2x2(matrix: Matrix) -> float:
    """Compute the determinant of a 2x2 matrix."""

    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("determinant_2x2 requires a 2x2 matrix")
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def fundamental_area_2d(generator: Matrix) -> float:
    """Return the area of the two-dimensional fundamental parallelogram."""

    return abs(determinant_2x2(generator))


def squared_distance(left: Vector, right: Vector) -> float:
    """Compute squared Euclidean distance."""

    if len(left) != len(right):
        raise ValueError("distance requires vectors of equal length")
    return sum((a - b) ** 2 for a, b in zip(left, right))


def generate_lattice_points(generator: Matrix, radius: int) -> tuple[tuple[IntVector, Vector], ...]:
    """Generate lattice points for coefficient vectors in [-radius, radius]^d."""

    if radius < 0:
        raise ValueError("radius must be nonnegative")
    dimension = len(generator[0])
    points = []
    for coefficients in product(range(-radius, radius + 1), repeat=dimension):
        point = matrix_vector_multiply(generator, coefficients)
        points.append((coefficients, point))
    return tuple(points)


def bounded_nearest_generated_point(
    target: Vector,
    generator: Matrix,
    radius: int,
) -> NearestGeneratedPoint:
    """Return the nearest generated lattice point in a bounded coefficient box."""

    candidates = generate_lattice_points(generator, radius)
    if not candidates:
        raise ValueError("candidate set must not be empty")
    best_coefficients, best_point = candidates[0]
    best_squared_distance = squared_distance(target, best_point)
    for coefficients, point in candidates[1:]:
        current_squared_distance = squared_distance(target, point)
        if current_squared_distance < best_squared_distance:
            best_coefficients = coefficients
            best_point = point
            best_squared_distance = current_squared_distance
    return NearestGeneratedPoint(
        coefficients=best_coefficients,
        point=best_point,
        distance=sqrt(best_squared_distance),
    )


def d4_parity_preview(vector: tuple[int, int, int, int]) -> bool:
    """Preview Chapter 6: D4 contains integer vectors with even coordinate sum."""

    return sum(vector) % 2 == 0


def build_example() -> LatticeExample:
    """Build the numerical example used in Chapter 5."""

    return LatticeExample(
        z2_nearest=bounded_nearest_generated_point(VISIBLE_TARGET, Z2_GENERATOR, radius=3),
        hex_nearest=bounded_nearest_generated_point(VISIBLE_TARGET, HEX_GENERATOR, radius=3),
        z2_area=fundamental_area_2d(Z2_GENERATOR),
        hex_area=fundamental_area_2d(HEX_GENERATOR),
        d4_preview_membership=(
            d4_parity_preview((1, -2, 2, 0)),
            d4_parity_preview((1, 0, -2, 3)),
        ),
    )


def main() -> None:
    example = build_example()
    print(f"Z2 nearest coefficients  = {example.z2_nearest.coefficients}")
    print(f"Z2 nearest point         = {tuple(round(v, 4) for v in example.z2_nearest.point)}")
    print(f"Z2 nearest distance      = {example.z2_nearest.distance:.4f}")
    print(f"hex nearest coefficients = {example.hex_nearest.coefficients}")
    print(f"hex nearest point        = {tuple(round(v, 4) for v in example.hex_nearest.point)}")
    print(f"hex nearest distance     = {example.hex_nearest.distance:.4f}")
    print(f"Z2 fundamental area      = {example.z2_area:.4f}")
    print(f"hex fundamental area     = {example.hex_area:.4f}")
    print(f"D4 preview membership    = {example.d4_preview_membership}")


if __name__ == "__main__":
    main()

