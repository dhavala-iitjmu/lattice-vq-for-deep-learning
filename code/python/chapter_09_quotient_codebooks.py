"""Reference implementation for Chapter 9: quotient codebooks."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import sqrt

from chapter_06_d4 import coefficients_for_d4_vector, is_in_d4
from chapter_07_nearest_lattice import nearest_d4, squared_distance


IntVector = tuple[int, int, int, int]
Vector = tuple[float, ...]

RUNNING_DECODED_LATTICE_POINTS: tuple[IntVector, IntVector] = (
    (1, -2, 2, -1),
    (1, 0, -2, 3),
)


@dataclass(frozen=True)
class CodebookEntry:
    index: int
    bits: tuple[int, int, int, int]
    representative: IntVector
    norm_squared: int


@dataclass(frozen=True)
class QuotientReduction:
    lattice_point: IntVector
    coefficients: IntVector
    bits: tuple[int, int, int, int]
    index: int
    representative: IntVector
    coarse_difference: IntVector


@dataclass(frozen=True)
class NearestRepresentative:
    target: Vector
    index: int
    representative: IntVector
    distance: float


@dataclass(frozen=True)
class Chapter9Example:
    codebook: tuple[CodebookEntry, ...]
    reductions: tuple[QuotientReduction, QuotientReduction]
    nearest_running_blocks: tuple[NearestRepresentative, NearestRepresentative]


def bits_to_index(bits: tuple[int, int, int, int]) -> int:
    """Read four bits as a binary integer."""

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("bits must contain only 0 and 1")
    return sum(bit << (3 - offset) for offset, bit in enumerate(bits))


def index_to_bits(index: int) -> tuple[int, int, int, int]:
    """Convert an index from 0 to 15 to four bits."""

    if index < 0 or index >= 16:
        raise ValueError("index must be in [0, 15]")
    return tuple((index >> shift) & 1 for shift in (3, 2, 1, 0))  # type: ignore[return-value]


def coefficient_bits_mod_2(vector: IntVector) -> tuple[int, int, int, int]:
    """Return D4 generator-coordinate parity bits for a D4 point."""

    coefficients = coefficients_for_d4_vector(vector)
    return tuple(value % 2 for value in coefficients)  # type: ignore[return-value]


def is_in_scaled_d4(vector: IntVector, q: int) -> bool:
    """Return whether an integer vector belongs to qD4."""

    if q <= 0:
        raise ValueError("q must be positive")
    if any(value % q != 0 for value in vector):
        return False
    divided = tuple(value // q for value in vector)
    return is_in_d4(divided)


def same_coset_mod_qd4(left: IntVector, right: IntVector, q: int = 2) -> bool:
    """Return whether two D4 points are equivalent modulo qD4."""

    difference = tuple(a - b for a, b in zip(left, right))
    return is_in_scaled_d4(difference, q)


def in_closed_scaled_voronoi(vector: IntVector, q: int = 2) -> bool:
    """Return whether a D4 point lies in the closed scaled origin cell qV."""

    if q != 2:
        raise ValueError("Chapter 9 implements the q = 2 D4 codebook")
    if not is_in_d4(vector):
        return False
    scaled_back = tuple(value / q for value in vector)
    distance_to_origin = squared_distance(scaled_back, (0, 0, 0, 0))
    nearest = nearest_d4(scaled_back)
    return distance_to_origin <= nearest.distance**2 + 1e-12


def generate_a2_d4() -> tuple[CodebookEntry, ...]:
    """Generate the 16 representatives of A_2 = D4 cap 2V."""

    candidates_by_index: dict[int, list[IntVector]] = {}
    for candidate in product(range(-2, 3), repeat=4):
        candidate4 = candidate  # type: ignore[assignment]
        if not is_in_d4(candidate4):
            continue
        if not in_closed_scaled_voronoi(candidate4):
            continue
        bits = coefficient_bits_mod_2(candidate4)
        index = bits_to_index(bits)
        candidates_by_index.setdefault(index, []).append(candidate4)

    entries: dict[int, CodebookEntry] = {}
    for index, candidates in candidates_by_index.items():
        min_norm = min(sum(value * value for value in candidate) for candidate in candidates)
        representative = max(
            candidate
            for candidate in candidates
            if sum(value * value for value in candidate) == min_norm
        )
        bits = coefficient_bits_mod_2(representative)
        entries[index] = CodebookEntry(
            index=index,
            bits=bits,
            representative=representative,
            norm_squared=min_norm,
        )

    expected_indices = set(range(16))
    if set(entries) != expected_indices:
        missing = sorted(expected_indices - set(entries))
        extra = sorted(set(entries) - expected_indices)
        raise AssertionError(f"invalid A2 codebook, missing={missing}, extra={extra}")
    return tuple(entries[index] for index in range(16))


def reduce_d4_mod_2d4(vector: IntVector, codebook: tuple[CodebookEntry, ...] | None = None) -> QuotientReduction:
    """Reduce a D4 lattice point to its D4/2D4 representative."""

    if not is_in_d4(vector):
        raise ValueError("reduce_d4_mod_2d4 requires a D4 lattice point")
    if codebook is None:
        codebook = generate_a2_d4()
    coefficients = coefficients_for_d4_vector(vector)
    bits = tuple(value % 2 for value in coefficients)  # type: ignore[assignment]
    index = bits_to_index(bits)
    representative = codebook[index].representative
    coarse_difference = tuple(value - rep for value, rep in zip(vector, representative))
    if not is_in_scaled_d4(coarse_difference, q=2):
        raise AssertionError("representative is not in the same coset")
    return QuotientReduction(
        lattice_point=vector,
        coefficients=coefficients,
        bits=bits,
        index=index,
        representative=representative,
        coarse_difference=coarse_difference,
    )


def nearest_representative(
    target: Vector,
    codebook: tuple[CodebookEntry, ...],
) -> NearestRepresentative:
    """Search the finite quotient codebook by brute force."""

    if len(target) != 4:
        raise ValueError("nearest_representative requires a vector of length 4")
    if not codebook:
        raise ValueError("codebook must not be empty")

    best_entry = codebook[0]
    best_squared_distance = squared_distance(target, best_entry.representative)
    for entry in codebook[1:]:
        current = squared_distance(target, entry.representative)
        if current < best_squared_distance:
            best_entry = entry
            best_squared_distance = current
    return NearestRepresentative(
        target=target,
        index=best_entry.index,
        representative=best_entry.representative,
        distance=sqrt(best_squared_distance),
    )


def build_example() -> Chapter9Example:
    """Build the numerical example used in Chapter 9."""

    codebook = generate_a2_d4()
    reductions = tuple(
        reduce_d4_mod_2d4(point, codebook)
        for point in RUNNING_DECODED_LATTICE_POINTS
    )
    running_blocks = (
        (0.73, -1.84, 2.11, -0.45),
        (1.27, 0.08, -2.36, 3.14),
    )
    nearest = tuple(nearest_representative(block, codebook) for block in running_blocks)
    return Chapter9Example(
        codebook=codebook,
        reductions=reductions,  # type: ignore[arg-type]
        nearest_running_blocks=nearest,  # type: ignore[arg-type]
    )


def main() -> None:
    example = build_example()
    print("D4 / 2D4 codebook")
    for entry in example.codebook:
        bit_string = "".join(str(bit) for bit in entry.bits)
        print(f"  {entry.index:2d} {bit_string} {entry.representative}")
    print("running lattice reductions")
    for reduction in example.reductions:
        bit_string = "".join(str(bit) for bit in reduction.bits)
        print(
            f"  {reduction.lattice_point} -> index={reduction.index}, "
            f"bits={bit_string}, representative={reduction.representative}, "
            f"difference={reduction.coarse_difference}"
        )


if __name__ == "__main__":
    main()
