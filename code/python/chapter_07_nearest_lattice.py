"""Reference implementation for Chapter 7: nearest Dn/D4 decoding."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import floor, sqrt


Vector = tuple[float, ...]
IntVector = tuple[int, ...]

RUNNING_BLOCKS: tuple[Vector, Vector] = (
    (0.73, -1.84, 2.11, -0.45),
    (1.27, 0.08, -2.36, 3.14),
)


@dataclass(frozen=True)
class DecodeResult:
    target: Vector
    rounded: IntVector
    rounding_errors: Vector
    repaired_coordinate: int | None
    decoded: IntVector
    distance: float


@dataclass(frozen=True)
class Chapter7Example:
    decoded_blocks: tuple[IntVector, IntVector]
    results: tuple[DecodeResult, DecodeResult]
    reconstructed_weight: IntVector


def round_nearest_integer(value: float) -> int:
    """Round to the nearest integer with ties resolved toward +infinity."""

    return floor(value + 0.5)


def squared_distance(left: Vector | IntVector, right: Vector | IntVector) -> float:
    """Compute squared Euclidean distance."""

    if len(left) != len(right):
        raise ValueError("distance requires vectors of equal length")
    return sum((a - b) ** 2 for a, b in zip(left, right))


def is_in_dn(vector: IntVector) -> bool:
    """Return whether an integer vector is in D_n."""

    return sum(vector) % 2 == 0


def nearest_dn(vector: Vector) -> DecodeResult:
    """Decode a real-valued vector to the nearest D_n lattice point."""

    if not vector:
        raise ValueError("nearest_dn requires a nonempty vector")

    rounded = tuple(round_nearest_integer(value) for value in vector)
    errors = tuple(value - rounded_value for value, rounded_value in zip(vector, rounded))
    decoded = list(rounded)
    repaired_coordinate: int | None = None

    if not is_in_dn(rounded):
        repaired_coordinate = max(range(len(vector)), key=lambda index: abs(errors[index]))
        if errors[repaired_coordinate] >= 0:
            decoded[repaired_coordinate] += 1
        else:
            decoded[repaired_coordinate] -= 1

    decoded_tuple = tuple(decoded)
    return DecodeResult(
        target=vector,
        rounded=rounded,
        rounding_errors=errors,
        repaired_coordinate=repaired_coordinate,
        decoded=decoded_tuple,
        distance=sqrt(squared_distance(vector, decoded_tuple)),
    )


def nearest_d4(vector: Vector) -> DecodeResult:
    """Decode a real-valued vector to the nearest D4 lattice point."""

    if len(vector) != 4:
        raise ValueError("nearest_d4 requires a vector of length 4")
    return nearest_dn(vector)


def brute_force_nearest_d4(vector: Vector, radius: int = 5) -> tuple[IntVector, float]:
    """Verify nearest D4 decoding by bounded brute force."""

    if len(vector) != 4:
        raise ValueError("brute_force_nearest_d4 requires a vector of length 4")
    best: IntVector | None = None
    best_squared_distance = float("inf")
    for candidate in product(range(-radius, radius + 1), repeat=4):
        if sum(candidate) % 2 != 0:
            continue
        current = squared_distance(vector, candidate)
        if current < best_squared_distance:
            best = candidate
            best_squared_distance = current
    if best is None:
        raise ValueError("no D4 candidate found")
    return best, sqrt(best_squared_distance)


def build_example() -> Chapter7Example:
    """Build the running Chapter 7 example."""

    results = tuple(nearest_d4(block) for block in RUNNING_BLOCKS)
    decoded_blocks = tuple(result.decoded for result in results)
    reconstructed_weight = decoded_blocks[0] + decoded_blocks[1]
    return Chapter7Example(
        decoded_blocks=decoded_blocks,  # type: ignore[arg-type]
        results=results,  # type: ignore[arg-type]
        reconstructed_weight=reconstructed_weight,
    )


def main() -> None:
    example = build_example()
    for index, result in enumerate(example.results, start=1):
        print(f"block {index}")
        print(f"  target              = {result.target}")
        print(f"  rounded             = {result.rounded}")
        print(f"  rounding errors     = {tuple(round(value, 2) for value in result.rounding_errors)}")
        print(f"  repaired coordinate = {result.repaired_coordinate}")
        print(f"  decoded             = {result.decoded}")
        print(f"  distance            = {result.distance:.4f}")
    print(f"decoded weight = {example.reconstructed_weight}")


if __name__ == "__main__":
    main()

