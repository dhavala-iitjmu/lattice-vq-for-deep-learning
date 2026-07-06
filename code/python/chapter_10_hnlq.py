"""Reference implementation for Chapter 10: Hierarchical Nested Lattice Quantization.

The scheme is exact digit decomposition:

  1. Decode the scaled target once: y = Q_D4(beta * v).
  2. Write the generator coefficients z (y = G z) in M-digit two's complement.
  3. Emit one 4-bit coset index per digit plane.

Decoding recombines digit representatives with weights (1, q, ..., q^(M-2),
-q^(M-1)). Within coefficient range the reconstruction equals y / beta exactly,
so the only error is the single nearest-lattice-point step. Overload happens
exactly when a coefficient falls outside the M-digit two's-complement range,
and is handled by deterministic coefficient clamping (saturation).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from chapter_06_d4 import D4_GENERATOR, coefficients_for_d4_vector, matrix_vector_multiply
from chapter_07_nearest_lattice import nearest_dn


Vector = tuple[float, ...]
IntVector = tuple[int, ...]
IndexSequence = tuple[int, ...]

RUNNING_BLOCKS: tuple[Vector, Vector] = (
    (0.73, -1.84, 2.11, -0.45),
    (1.27, 0.08, -2.36, 3.14),
)

DEFAULT_Q = 2
DEFAULT_M = 4
DEFAULT_BETA = 2.0


def digit_bits(index: int) -> IntVector:
    """Return the four coefficient bits of a digit index (z1 is the MSB)."""

    if index < 0 or index > 15:
        raise ValueError("digit index must be in 0..15")
    return ((index >> 3) & 1, (index >> 2) & 1, (index >> 1) & 1, index & 1)


def digit_index(bits: IntVector) -> int:
    """Return the digit index for four coefficient bits (z1 is the MSB)."""

    return bits[0] * 8 + bits[1] * 4 + bits[2] * 2 + bits[3]


def digit_representative(index: int) -> IntVector:
    """Return the digit representative G * bits(index)."""

    return matrix_vector_multiply(D4_GENERATOR, digit_bits(index))


DIGIT_REPRESENTATIVES: tuple[IntVector, ...] = tuple(
    digit_representative(index) for index in range(16)
)


def digit_weights(M: int = DEFAULT_M, q: int = DEFAULT_Q) -> tuple[int, ...]:
    """Return two's-complement digit weights (1, q, ..., q^(M-2), -q^(M-1))."""

    if M < 1:
        raise ValueError("M must be positive")
    weights = [q**m for m in range(M - 1)]
    weights.append(-(q ** (M - 1)))
    return tuple(weights)


def coefficient_range(M: int = DEFAULT_M, q: int = DEFAULT_Q) -> tuple[int, int]:
    """Return the closed two's-complement coefficient range for M digits."""

    return (-(q ** (M - 1)), q ** (M - 1) - 1)


def coefficients_to_indices(z: IntVector, M: int = DEFAULT_M, q: int = DEFAULT_Q) -> IndexSequence:
    """Write coefficients in M-digit base-q two's complement, one index per plane."""

    low, high = coefficient_range(M, q)
    for value in z:
        if value < low or value > high:
            raise ValueError("coefficient out of range; clamp before extracting digits")
    wrapped = [value % (q**M) for value in z]
    indices = []
    for m in range(M):
        plane = tuple((value // (q**m)) % q for value in wrapped)
        indices.append(digit_index(plane))
    return tuple(indices)


def indices_to_coefficients(indices: IndexSequence, q: int = DEFAULT_Q) -> IntVector:
    """Recombine digit planes into signed coefficients (two's complement)."""

    M = len(indices)
    weights = digit_weights(M, q)
    z = [0, 0, 0, 0]
    for weight, index in zip(weights, indices):
        bits = digit_bits(index)
        for i in range(4):
            z[i] += weight * bits[i]
    return tuple(z)


def squared_distance(left: Vector, right: Vector) -> float:
    """Compute squared Euclidean distance."""

    if len(left) != len(right):
        raise ValueError("distance requires vectors of equal length")
    return sum((a - b) ** 2 for a, b in zip(left, right))


@dataclass(frozen=True)
class HNLQEncoding:
    target: Vector
    beta: float
    q: int
    M: int
    lattice_point: IntVector
    coefficients: IntVector
    clamped_coefficients: IntVector
    overloaded: bool
    indices: IndexSequence
    reconstruction: Vector
    squared_error: float


@dataclass(frozen=True)
class Chapter10Example:
    effective_codebook_size: int
    running_encodings: tuple[HNLQEncoding, HNLQEncoding]
    running_weight_reconstruction: Vector
    beta_sweep: tuple[tuple[float, float, int], ...]
    overload_demo: HNLQEncoding


def hnlq_encode(
    target: Vector,
    beta: float = DEFAULT_BETA,
    q: int = DEFAULT_Q,
    M: int = DEFAULT_M,
) -> HNLQEncoding:
    """Encode one block: one nearest-D4 decode, then M digit planes."""

    if beta <= 0:
        raise ValueError("beta must be positive")
    scaled = tuple(beta * value for value in target)
    lattice_point = nearest_dn(scaled).decoded
    z = coefficients_for_d4_vector(lattice_point)
    low, high = coefficient_range(M, q)
    clamped = tuple(max(low, min(high, value)) for value in z)
    overloaded = clamped != z
    indices = coefficients_to_indices(clamped, M, q)
    reconstruction = decode_indices(indices, beta, q)
    return HNLQEncoding(
        target=target,
        beta=beta,
        q=q,
        M=M,
        lattice_point=lattice_point,
        coefficients=z,
        clamped_coefficients=clamped,
        overloaded=overloaded,
        indices=indices,
        reconstruction=reconstruction,
        squared_error=squared_distance(target, reconstruction),
    )


def decode_indices(
    indices: IndexSequence,
    beta: float = DEFAULT_BETA,
    q: int = DEFAULT_Q,
) -> Vector:
    """Decode digit indices to a reconstruction in weight units."""

    if beta <= 0:
        raise ValueError("beta must be positive")
    weights = digit_weights(len(indices), q)
    accumulator = [0, 0, 0, 0]
    for weight, index in zip(weights, indices):
        representative = DIGIT_REPRESENTATIVES[index]
        for i in range(4):
            accumulator[i] += weight * representative[i]
    return tuple(value / beta for value in accumulator)


def effective_codebook_size(codebook_size: int, M: int) -> int:
    """Return the number of index sequences in an M-level hierarchy."""

    if codebook_size <= 0:
        raise ValueError("codebook_size must be positive")
    if M <= 0:
        raise ValueError("M must be positive")
    return codebook_size**M


def minnorm_digit_attempt(start: IntVector, codebook: dict[int, IntVector], steps: int = 6) -> tuple[IntVector, ...]:
    """Demonstrate why min-norm representatives cannot serve as exact digits.

    Runs y -> (y - c(y)) / 2 with c(y) the min-norm coset representative and
    returns the visited quotients. Points such as (0, -1, 1, 0) cycle forever.
    """

    trace = [start]
    y = start
    for _ in range(steps):
        z = coefficients_for_d4_vector(y)
        index = digit_index(tuple(value % 2 for value in z))
        c = codebook[index]
        y = tuple((a - b) // 2 for a, b in zip(y, c))
        trace.append(y)
    return tuple(trace)


def build_example() -> Chapter10Example:
    """Build the numerical example used in Chapter 10."""

    running = tuple(hnlq_encode(block) for block in RUNNING_BLOCKS)
    reconstruction = running[0].reconstruction + running[1].reconstruction
    sweep = []
    for beta in (0.5, 1.0, 2.0, 4.0, 8.0):
        encodings = [hnlq_encode(block, beta=beta) for block in RUNNING_BLOCKS]
        mse = sum(e.squared_error for e in encodings) / 8
        overloads = sum(int(e.overloaded) for e in encodings)
        sweep.append((beta, mse, overloads))
    return Chapter10Example(
        effective_codebook_size=effective_codebook_size(16, DEFAULT_M),
        running_encodings=running,
        running_weight_reconstruction=reconstruction,
        beta_sweep=tuple(sweep),
        overload_demo=hnlq_encode(RUNNING_BLOCKS[1], beta=8.0),
    )


def main() -> None:
    example = build_example()
    print(f"effective codebook size = {example.effective_codebook_size}")
    for name, enc in zip(("block 1", "block 2"), example.running_encodings):
        print(f"{name}: beta={enc.beta}")
        print(f"  lattice point   = {enc.lattice_point}")
        print(f"  coefficients    = {enc.coefficients}")
        print(f"  digit indices   = {enc.indices}")
        print(f"  reconstruction  = {enc.reconstruction}")
        print(f"  squared error   = {enc.squared_error:.4f}")
        print(f"  overloaded      = {enc.overloaded}")
    print(f"running reconstruction = {example.running_weight_reconstruction}")
    print("beta sweep (beta, mse, overloaded blocks):")
    for row in example.beta_sweep:
        print(f"  {row[0]:>4} {row[1]:.4f} {row[2]}")
    demo = example.overload_demo
    print(f"overload demo at beta={demo.beta}: z={demo.coefficients} -> {demo.clamped_coefficients}, sqerr={demo.squared_error:.4f}")


if __name__ == "__main__":
    main()
