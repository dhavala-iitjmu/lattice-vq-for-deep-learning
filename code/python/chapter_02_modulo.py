"""Reference examples for Chapter 2: modulo arithmetic and cosets."""

from __future__ import annotations

from itertools import product


RUNNING_BLOCKS = ((1, -2, 2, 0), (1, 0, -2, 3))


def integer_mod(value: int, modulus: int) -> int:
    """Return the nonnegative remainder of value modulo modulus."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")
    return value % modulus


def quotient_and_remainder(value: int, modulus: int) -> tuple[int, int]:
    """Return quotient and remainder using floor-division convention."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")
    quotient = value // modulus
    remainder = value - modulus * quotient
    return quotient, remainder


def group_by_remainder(values: range | list[int], modulus: int) -> dict[int, list[int]]:
    """Group integer values into buckets by remainder."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")
    buckets = {label: [] for label in range(modulus)}
    for value in values:
        buckets[integer_mod(value, modulus)].append(value)
    return buckets


def vector_mod(vector: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    """Reduce a vector coordinate by coordinate."""

    return tuple(integer_mod(coordinate, modulus) for coordinate in vector)


def binary_patterns(dimension: int) -> tuple[tuple[int, ...], ...]:
    """Return all modulo-2 signatures in the requested dimension."""

    if dimension < 0:
        raise ValueError("dimension must be nonnegative")
    return tuple(product((0, 1), repeat=dimension))


def running_block_signatures() -> tuple[tuple[int, ...], ...]:
    """Return the modulo-2 signatures of the Chapter 1 running blocks."""

    return tuple(vector_mod(block, 2) for block in RUNNING_BLOCKS)


def main() -> None:
    for value in (17, -7):
        quotient, remainder = quotient_and_remainder(value, 4)
        print(f"{value} = 4 * {quotient} + {remainder}")
        print(f"{value} mod 4 = {integer_mod(value, 4)}")

    print("modulo-2 signatures:")
    for block, signature in zip(RUNNING_BLOCKS, running_block_signatures()):
        print(f"{block} mod 2 = {signature}")

    print(f"number of 4D modulo-2 signatures = {len(binary_patterns(4))}")


if __name__ == "__main__":
    main()

