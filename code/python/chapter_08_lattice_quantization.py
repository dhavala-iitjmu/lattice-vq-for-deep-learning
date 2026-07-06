"""Reference implementation for Chapter 8: lattice vector quantization."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from chapter_07_nearest_lattice import RUNNING_BLOCKS, nearest_d4, squared_distance


Vector = tuple[float, ...]
IntVector = tuple[int, ...]

DIAGNOSTIC_BLOCK: Vector = (0.38, -0.62, 1.49, -1.11)
EXAMPLE_BLOCKS: tuple[Vector, ...] = (
    RUNNING_BLOCKS[0],
    RUNNING_BLOCKS[1],
    DIAGNOSTIC_BLOCK,
)
SCALES: tuple[float, ...] = (0.5, 1.0, 2.0)


@dataclass(frozen=True)
class LatticeQuantizationResult:
    target: Vector
    beta: float
    scaled_target: Vector
    lattice_point: IntVector
    reconstruction: Vector
    squared_error: float
    distance: float


@dataclass(frozen=True)
class Chapter8Example:
    blocks: tuple[Vector, ...]
    betas: tuple[float, ...]
    results_by_beta: dict[float, tuple[LatticeQuantizationResult, ...]]
    mse_by_beta: dict[float, float]
    running_weight_reconstruction_beta_2: Vector


def scale_vector(vector: Vector, beta: float) -> Vector:
    """Scale a vector coordinate-wise."""

    return tuple(beta * value for value in vector)


def inverse_scale_vector(vector: IntVector, beta: float) -> Vector:
    """Return a lattice point to the original weight scale."""

    return tuple(value / beta for value in vector)


def scaled_nearest_d4_quantize(vector: Vector, beta: float) -> LatticeQuantizationResult:
    """Quantize one four-dimensional vector with the scaled D4 quantizer."""

    if len(vector) != 4:
        raise ValueError("scaled_nearest_d4_quantize requires a vector of length 4")
    if beta <= 0:
        raise ValueError("beta must be positive")

    scaled_target = scale_vector(vector, beta)
    decoded = nearest_d4(scaled_target)
    reconstruction = inverse_scale_vector(decoded.decoded, beta)
    squared_error = squared_distance(vector, reconstruction)
    return LatticeQuantizationResult(
        target=vector,
        beta=beta,
        scaled_target=scaled_target,
        lattice_point=decoded.decoded,
        reconstruction=reconstruction,
        squared_error=squared_error,
        distance=sqrt(squared_error),
    )


def quantize_blocks(
    blocks: tuple[Vector, ...],
    beta: float,
) -> tuple[LatticeQuantizationResult, ...]:
    """Quantize a sequence of D4 blocks with one shared scale."""

    return tuple(scaled_nearest_d4_quantize(block, beta) for block in blocks)


def mean_squared_error(results: tuple[LatticeQuantizationResult, ...]) -> float:
    """Return mean squared error per coordinate for quantized blocks."""

    if not results:
        raise ValueError("mean_squared_error requires at least one result")
    total_coordinates = sum(len(result.target) for result in results)
    return sum(result.squared_error for result in results) / total_coordinates


def scaled_d4_ray(beta: float, count: int) -> tuple[Vector, ...]:
    """Generate points showing that a scaled D4 lattice is still infinite."""

    if beta <= 0:
        raise ValueError("beta must be positive")
    if count < 0:
        raise ValueError("count must be nonnegative")
    return tuple((2 * index / beta, 0.0, 0.0, 0.0) for index in range(count))


def build_example() -> Chapter8Example:
    """Build the numerical example used in Chapter 8."""

    results_by_beta = {beta: quantize_blocks(EXAMPLE_BLOCKS, beta) for beta in SCALES}
    mse_by_beta = {
        beta: mean_squared_error(results)
        for beta, results in results_by_beta.items()
    }
    beta_2_results = results_by_beta[2.0]
    running_weight_reconstruction = beta_2_results[0].reconstruction + beta_2_results[1].reconstruction
    return Chapter8Example(
        blocks=EXAMPLE_BLOCKS,
        betas=SCALES,
        results_by_beta=results_by_beta,
        mse_by_beta=mse_by_beta,
        running_weight_reconstruction_beta_2=running_weight_reconstruction,
    )


def main() -> None:
    example = build_example()
    for beta in example.betas:
        print(f"beta = {beta}")
        for index, result in enumerate(example.results_by_beta[beta], start=1):
            rounded_reconstruction = tuple(round(value, 4) for value in result.reconstruction)
            print(
                f"  block {index}: lattice={result.lattice_point}, "
                f"reconstruction={rounded_reconstruction}, "
                f"squared_error={result.squared_error:.4f}"
            )
        print(f"  mean_squared_error={example.mse_by_beta[beta]:.4f}")
    print(
        "running weight reconstruction at beta=2 = "
        f"{tuple(round(value, 4) for value in example.running_weight_reconstruction_beta_2)}"
    )
    print(f"scaled D4 ray at beta=2 = {scaled_d4_ray(beta=2.0, count=5)}")


if __name__ == "__main__":
    main()
