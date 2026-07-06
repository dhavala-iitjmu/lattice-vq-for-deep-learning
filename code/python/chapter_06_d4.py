"""Reference implementation for Chapter 6: the D4 lattice."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


Vector4 = tuple[int, int, int, int]
Matrix4 = tuple[tuple[int, int, int, int], ...]

D4_GENERATOR: Matrix4 = (
    (1, 0, 0, 0),
    (-1, 1, 0, 0),
    (0, -1, 1, 1),
    (0, 0, -1, 1),
)

RUNNING_BLOCKS: tuple[Vector4, Vector4] = (
    (1, -2, 2, 0),
    (1, 0, -2, 3),
)


@dataclass(frozen=True)
class D4Example:
    membership: tuple[bool, bool]
    generated_running_block: Vector4
    generated_running_coefficients: Vector4
    even_parity_patterns: tuple[Vector4, ...]
    parity_signatures: tuple[Vector4, Vector4]


def is_integer_vector_4(vector: tuple[object, ...]) -> bool:
    """Return whether the input is a length-4 integer-valued vector.

    Integrality is judged by value, not by type: (1.0, 0, 0, 1) counts as an
    integer vector. This matches the membership rule in Chapter 6.
    """

    if len(vector) != 4:
        return False
    return all(
        isinstance(value, int)
        or (isinstance(value, float) and value.is_integer())
        for value in vector
    )


def is_in_d4(vector: tuple[object, ...]) -> bool:
    """Return whether a vector belongs to D4."""

    return is_integer_vector_4(vector) and sum(vector) % 2 == 0


def matrix_vector_multiply(matrix: Matrix4, vector: Vector4) -> Vector4:
    """Multiply a 4x4 integer matrix by a length-4 integer vector."""

    return tuple(sum(row[j] * vector[j] for j in range(4)) for row in matrix)  # type: ignore[return-value]


def generate_d4_point(coefficients: Vector4) -> Vector4:
    """Generate a D4 point from integer coefficients."""

    return matrix_vector_multiply(D4_GENERATOR, coefficients)


def coefficients_for_d4_vector(vector: Vector4) -> Vector4:
    """Return integer coefficients z such that D4_GENERATOR @ z = vector."""

    if not is_in_d4(vector):
        raise ValueError("coefficient formula requires a D4 vector")
    v1, v2, v3, v4 = vector
    z1 = v1
    z2 = v1 + v2
    z4 = (v1 + v2 + v3 + v4) // 2
    z3 = z4 - v4
    coefficients = (z1, z2, z3, z4)
    if generate_d4_point(coefficients) != vector:
        raise AssertionError("internal coefficient formula failed")
    return coefficients


def parity_signature(vector: Vector4) -> Vector4:
    """Return the coordinate-wise modulo-2 parity signature."""

    return tuple(value % 2 for value in vector)  # type: ignore[return-value]


def is_even_parity_signature(signature: Vector4) -> bool:
    """Return whether a four-bit signature has even parity."""

    return all(bit in (0, 1) for bit in signature) and sum(signature) % 2 == 0


def even_parity_patterns() -> tuple[Vector4, ...]:
    """Return all four-bit signatures valid for D4 modulo 2Z^4."""

    return tuple(
        pattern
        for pattern in product((0, 1), repeat=4)
        if is_even_parity_signature(pattern)  # type: ignore[arg-type]
    )  # type: ignore[return-value]


def coset_representative_mod_2z4(vector: Vector4) -> Vector4:
    """Return the even parity signature representing the vector modulo 2Z^4."""

    if not is_in_d4(vector):
        raise ValueError("only D4 vectors have even-parity coset representatives")
    signature = parity_signature(vector)
    if not is_even_parity_signature(signature):
        raise AssertionError("D4 vector produced an odd signature")
    return signature


def build_example() -> D4Example:
    """Build the numerical example used in Chapter 6."""

    second_block = RUNNING_BLOCKS[1]
    coefficients = coefficients_for_d4_vector(second_block)
    return D4Example(
        membership=tuple(is_in_d4(block) for block in RUNNING_BLOCKS),  # type: ignore[arg-type]
        generated_running_block=generate_d4_point(coefficients),
        generated_running_coefficients=coefficients,
        even_parity_patterns=even_parity_patterns(),
        parity_signatures=tuple(parity_signature(block) for block in RUNNING_BLOCKS),  # type: ignore[arg-type]
    )


def main() -> None:
    example = build_example()
    for block, membership, signature in zip(RUNNING_BLOCKS, example.membership, example.parity_signatures):
        print(f"{block} sum={sum(block):2d} signature={signature} in_D4={membership}")
    print(f"coefficients for {RUNNING_BLOCKS[1]} = {example.generated_running_coefficients}")
    print(f"generated point = {example.generated_running_block}")
    print(f"number of even parity signatures = {len(example.even_parity_patterns)}")
    print(f"even parity signatures = {example.even_parity_patterns}")


if __name__ == "__main__":
    main()

