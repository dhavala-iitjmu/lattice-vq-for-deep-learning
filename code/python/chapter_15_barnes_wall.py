"""Reference implementation for Chapter 15: Barnes-Wall overview."""

from __future__ import annotations

from dataclasses import dataclass

from chapter_06_d4 import coefficients_for_d4_vector, generate_d4_point, is_in_d4


Vector = tuple[float, ...]
IntVector = tuple[int, ...]


@dataclass(frozen=True)
class Chapter15Example:
    vector: IntVector
    parity_membership: bool
    generator_coefficients: IntVector
    regenerated: IntVector
    pairwise_r: IntVector
    hierarchy: tuple[tuple[int, str], ...]


def pairwise_r_transform(vector: IntVector) -> IntVector:
    """Apply R(a,b) = (a+b, a-b) to adjacent coordinate pairs."""

    if len(vector) % 2 != 0:
        raise ValueError("pairwise_r_transform requires even length")
    output: list[int] = []
    for index in range(0, len(vector), 2):
        a = vector[index]
        b = vector[index + 1]
        output.extend((a + b, a - b))
    return tuple(output)


def inverse_pairwise_r_transform(vector: IntVector) -> Vector:
    """Invert the pairwise R transform, allowing half-integers."""

    if len(vector) % 2 != 0:
        raise ValueError("inverse_pairwise_r_transform requires even length")
    output: list[float] = []
    for index in range(0, len(vector), 2):
        s = vector[index]
        d = vector[index + 1]
        output.extend(((s + d) / 2, (s - d) / 2))
    return tuple(output)


def barnes_wall_hierarchy() -> tuple[tuple[int, str], ...]:
    """Return the informal hierarchy used in Chapter 15."""

    return (
        (1, "integer line"),
        (2, "pairwise sum-difference structure"),
        (4, "D4-like parity structure"),
        (8, "E8/RE8-like structure"),
    )


def build_example() -> Chapter15Example:
    vector = (1, 0, -2, 3)
    coefficients = coefficients_for_d4_vector(vector)
    return Chapter15Example(
        vector=vector,
        parity_membership=is_in_d4(vector),
        generator_coefficients=coefficients,
        regenerated=generate_d4_point(coefficients),
        pairwise_r=pairwise_r_transform(vector),
        hierarchy=barnes_wall_hierarchy(),
    )


def main() -> None:
    example = build_example()
    print(f"vector                  = {example.vector}")
    print(f"in D4 by parity          = {example.parity_membership}")
    print(f"generator coefficients   = {example.generator_coefficients}")
    print(f"regenerated             = {example.regenerated}")
    print(f"pairwise R(vector)       = {example.pairwise_r}")
    print(f"hierarchy                = {example.hierarchy}")


if __name__ == "__main__":
    main()
