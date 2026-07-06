"""Reference implementation for Chapter 13: HNLQ in practice.

Three measured experiments, all deterministic:

  1. Calibrate beta on a small fixed layer and evaluate weight/output MSE.
  2. Compare HNLQ against a scale-swept scalar INT4 baseline at 4 bits/weight.
  3. A Gaussian study separating the D4 geometry gain (matched point density)
     from the digit-range shaping loss (matched bits per weight).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from chapter_07_nearest_lattice import nearest_dn
from chapter_10_hnlq import DEFAULT_Q, hnlq_encode


Vector = tuple[float, ...]
Matrix = tuple[Vector, ...]

WEIGHT_MATRIX: Matrix = (
    (0.73, -1.84, 2.11, -0.45, 1.27, 0.08, -2.36, 3.14),
    (0.38, -0.62, 1.49, -1.11, -0.54, 1.72, -1.06, 0.44),
    (-1.25, 0.91, 0.33, -2.07, 2.44, -0.18, 1.36, -0.75),
    (1.88, -1.52, 0.06, 0.97, -0.82, 2.15, -1.94, 0.28),
)

ACTIVATION_BATCH: Matrix = (
    (2.0, 1.0, -1.0, 3.0, -2.0, 0.5, 1.0, -1.5),
    (0.5, -1.0, 2.0, 0.25, 1.5, -0.5, 0.75, 1.0),
    (-1.0, 0.25, 0.5, -0.75, 2.0, 1.0, -0.5, 0.25),
)

BETA_CANDIDATES = (0.5, 1.0, 2.0, 4.0)
INT4_DELTA_CANDIDATES = tuple(k / 100 for k in range(5, 101))


@dataclass(frozen=True)
class CalibrationResult:
    beta: float
    quantized_weights: Matrix
    weight_mse: float
    output_mse: float
    overloaded_blocks: int


@dataclass(frozen=True)
class ScalarBaseline:
    delta: float
    weight_mse: float
    output_mse: float


@dataclass(frozen=True)
class GaussianStudy:
    hnlq_best_beta: float
    hnlq_best_mse: float
    int4_best_delta: float
    int4_best_mse: float
    matched_rate_ratio: float
    granular_d4_mse: float
    granular_scalar_mse: float
    matched_density_ratio: float


@dataclass(frozen=True)
class Chapter13Example:
    sweep: tuple[CalibrationResult, ...]
    best_by_weight_mse: CalibrationResult
    best_by_output_mse: CalibrationResult
    scalar_baseline: ScalarBaseline
    bits_per_weight: float
    gaussian: GaussianStudy


def split_blocks(row: Vector, block_size: int = 4) -> tuple[Vector, ...]:
    """Split a row into fixed-size blocks."""

    return tuple(
        tuple(row[index : index + block_size]) for index in range(0, len(row), block_size)
    )


def mean_squared_error(left: Matrix, right: Matrix) -> float:
    """Elementwise mean squared error between two matrices."""

    total = 0.0
    count = 0
    for left_row, right_row in zip(left, right):
        for a, b in zip(left_row, right_row):
            total += (a - b) ** 2
            count += 1
    return total / count


def matmul_activations_weights(activations: Matrix, weights: Matrix) -> Matrix:
    """Compute X W^T for calibration activations X and weight matrix W."""

    return tuple(
        tuple(sum(a * w for a, w in zip(sample, row)) for row in weights)
        for sample in activations
    )


def quantize_hnlq_matrix(weights: Matrix, beta: float) -> tuple[Matrix, int]:
    """HNLQ-quantize a matrix row by row with the digit encoder."""

    rows = []
    overloaded_blocks = 0
    for row in weights:
        reconstructed: Vector = ()
        for block in split_blocks(row):
            encoding = hnlq_encode(block, beta=beta)
            reconstructed += encoding.reconstruction
            overloaded_blocks += int(encoding.overloaded)
        rows.append(reconstructed)
    return tuple(rows), overloaded_blocks


def evaluate_hnlq_beta(beta: float) -> CalibrationResult:
    quantized, overloaded_blocks = quantize_hnlq_matrix(WEIGHT_MATRIX, beta)
    original_outputs = matmul_activations_weights(ACTIVATION_BATCH, WEIGHT_MATRIX)
    quantized_outputs = matmul_activations_weights(ACTIVATION_BATCH, quantized)
    return CalibrationResult(
        beta=beta,
        quantized_weights=quantized,
        weight_mse=mean_squared_error(WEIGHT_MATRIX, quantized),
        output_mse=mean_squared_error(original_outputs, quantized_outputs),
        overloaded_blocks=overloaded_blocks,
    )


def quantize_int4(weights: Matrix, delta: float) -> Matrix:
    """Symmetric scalar INT4 with levels -8..7 and step delta."""

    return tuple(
        tuple(max(-8, min(7, round(value / delta))) * delta for value in row)
        for row in weights
    )


def scalar_int4_baseline() -> ScalarBaseline:
    """Scale-swept scalar INT4 baseline, best step by output MSE."""

    original_outputs = matmul_activations_weights(ACTIVATION_BATCH, WEIGHT_MATRIX)
    best: ScalarBaseline | None = None
    for delta in INT4_DELTA_CANDIDATES:
        quantized = quantize_int4(WEIGHT_MATRIX, delta)
        quantized_outputs = matmul_activations_weights(ACTIVATION_BATCH, quantized)
        candidate = ScalarBaseline(
            delta=delta,
            weight_mse=mean_squared_error(WEIGHT_MATRIX, quantized),
            output_mse=mean_squared_error(original_outputs, quantized_outputs),
        )
        if best is None or candidate.output_mse < best.output_mse:
            best = candidate
    assert best is not None
    return best


def bits_per_weight(M: int = 4, q: int = DEFAULT_Q, d: int = 4) -> float:
    """Return HNLQ bits per weight for q=2 digit indices."""

    return M * d * math.log2(q) / d


def deterministic_gaussians(count: int, seed: int = 12345) -> tuple[float, ...]:
    """Deterministic standard Gaussian samples (LCG + Box-Muller)."""

    state = seed
    values: list[float] = []
    while len(values) < count:
        state = (1103515245 * state + 12345) % (2**31)
        u1 = state / (2**31)
        state = (1103515245 * state + 12345) % (2**31)
        u2 = state / (2**31)
        if u1 <= 1e-12:
            continue
        radius = math.sqrt(-2.0 * math.log(u1))
        values.append(radius * math.cos(2.0 * math.pi * u2))
        values.append(radius * math.sin(2.0 * math.pi * u2))
    return tuple(values[:count])


def gaussian_study(count: int = 256, seed: int = 12345) -> GaussianStudy:
    """Measure the D4 geometry gain and the digit-range shaping loss."""

    samples = deterministic_gaussians(count, seed)
    blocks = split_blocks(samples)

    def hnlq_weight_mse(beta: float) -> float:
        return sum(hnlq_encode(block, beta=beta).squared_error for block in blocks) / count

    def int4_weight_mse(delta: float) -> float:
        return sum(
            (value - max(-8, min(7, round(value / delta))) * delta) ** 2 for value in samples
        ) / count

    hnlq_best_mse, hnlq_best_beta = min(
        (hnlq_weight_mse(k / 4), k / 4) for k in range(2, 33)
    )
    int4_best_mse, int4_best_delta = min(
        (int4_weight_mse(delta), delta) for delta in INT4_DELTA_CANDIDATES
    )

    # Matched point density, granular regime only: D4 at spacing 1/beta has
    # 0.5 * beta^4 points per unit volume; the scalar grid matches it with
    # step delta = 2^(1/4) / beta.
    beta = 4.0
    delta_matched = 2 ** 0.25 / beta
    granular_d4 = 0.0
    for block in blocks:
        scaled = tuple(beta * value for value in block)
        decoded = nearest_dn(scaled).decoded
        granular_d4 += sum(
            (value - point / beta) ** 2 for value, point in zip(block, decoded)
        )
    granular_d4 /= count
    granular_scalar = (
        sum((value - round(value / delta_matched) * delta_matched) ** 2 for value in samples)
        / count
    )

    return GaussianStudy(
        hnlq_best_beta=hnlq_best_beta,
        hnlq_best_mse=hnlq_best_mse,
        int4_best_delta=int4_best_delta,
        int4_best_mse=int4_best_mse,
        matched_rate_ratio=hnlq_best_mse / int4_best_mse,
        granular_d4_mse=granular_d4,
        granular_scalar_mse=granular_scalar,
        matched_density_ratio=granular_d4 / granular_scalar,
    )


def build_example() -> Chapter13Example:
    sweep = tuple(evaluate_hnlq_beta(beta) for beta in BETA_CANDIDATES)
    best_by_weight = min(sweep, key=lambda result: result.weight_mse)
    best_by_output = min(sweep, key=lambda result: result.output_mse)
    return Chapter13Example(
        sweep=sweep,
        best_by_weight_mse=best_by_weight,
        best_by_output_mse=best_by_output,
        scalar_baseline=scalar_int4_baseline(),
        bits_per_weight=bits_per_weight(),
        gaussian=gaussian_study(),
    )


def main() -> None:
    example = build_example()
    print("beta sweep (beta, weight MSE, output MSE, overloaded blocks):")
    for result in example.sweep:
        print(
            f"  {result.beta:>4} {result.weight_mse:.4f} {result.output_mse:.4f} {result.overloaded_blocks}"
        )
    print(f"bits per weight = {example.bits_per_weight}")
    baseline = example.scalar_baseline
    print(
        f"scalar INT4 (swept): delta={baseline.delta}, weight MSE={baseline.weight_mse:.4f}, output MSE={baseline.output_mse:.4f}"
    )
    g = example.gaussian
    print("gaussian study:")
    print(f"  HNLQ best:  mse={g.hnlq_best_mse:.5f} at beta={g.hnlq_best_beta}")
    print(f"  INT4 best:  mse={g.int4_best_mse:.5f} at delta={g.int4_best_delta}")
    print(f"  matched-rate ratio HNLQ/INT4 = {g.matched_rate_ratio:.3f}")
    print(
        f"  matched-density granular: D4={g.granular_d4_mse:.6f}, scalar={g.granular_scalar_mse:.6f}, ratio={g.matched_density_ratio:.3f}"
    )


if __name__ == "__main__":
    main()
