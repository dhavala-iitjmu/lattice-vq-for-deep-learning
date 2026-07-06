"""Reference implementation for Chapter 16: Reed-Muller codes."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


BitVector = tuple[int, ...]
BinaryMatrix = tuple[BitVector, ...]

RM_1_2_GENERATOR: BinaryMatrix = (
    (1, 1, 1, 1),
    (0, 0, 1, 1),
    (0, 1, 0, 1),
)


@dataclass(frozen=True)
class Chapter16Example:
    codewords: tuple[BitVector, ...]
    running_signature: BitVector
    running_even_part: tuple[int, int, int, int]
    generated_from_101: BitVector


def xor_vectors(left: BitVector, right: BitVector) -> BitVector:
    if len(left) != len(right):
        raise ValueError("xor_vectors requires equal lengths")
    return tuple((a + b) % 2 for a, b in zip(left, right))


def generate_binary_code(generator: BinaryMatrix) -> tuple[BitVector, ...]:
    """Generate all binary linear combinations of generator rows."""

    if not generator:
        raise ValueError("generator must not be empty")
    rows = len(generator)
    width = len(generator[0])
    codewords: set[BitVector] = set()
    for coefficients in product((0, 1), repeat=rows):
        word = tuple(0 for _ in range(width))
        for coefficient, row in zip(coefficients, generator):
            if coefficient:
                word = xor_vectors(word, row)
        codewords.add(word)
    return tuple(sorted(codewords))


def is_even_parity(bits: BitVector) -> bool:
    return all(bit in (0, 1) for bit in bits) and sum(bits) % 2 == 0


def parity_signature(vector: tuple[int, int, int, int]) -> BitVector:
    return tuple(value % 2 for value in vector)


def decompose_d4_mod_2(vector: tuple[int, int, int, int]) -> tuple[tuple[int, int, int, int], BitVector]:
    """Return even part and binary signature for a D4 vector."""

    signature = parity_signature(vector)
    if not is_even_parity(signature):
        raise ValueError("vector does not have a D4 parity signature")
    even_part = tuple(value - bit for value, bit in zip(vector, signature))
    return even_part, signature  # type: ignore[return-value]


def encode_with_generator(coefficients: BitVector, generator: BinaryMatrix = RM_1_2_GENERATOR) -> BitVector:
    if len(coefficients) != len(generator):
        raise ValueError("coefficient length must match generator rows")
    width = len(generator[0])
    word = tuple(0 for _ in range(width))
    for coefficient, row in zip(coefficients, generator):
        if coefficient:
            word = xor_vectors(word, row)
    return word


def build_example() -> Chapter16Example:
    vector = (1, 0, -2, 3)
    even_part, signature = decompose_d4_mod_2(vector)
    return Chapter16Example(
        codewords=generate_binary_code(RM_1_2_GENERATOR),
        running_signature=signature,
        running_even_part=even_part,
        generated_from_101=encode_with_generator((1, 0, 1)),
    )


def main() -> None:
    example = build_example()
    print(f"RM(1,2) codewords       = {example.codewords}")
    print(f"running signature       = {example.running_signature}")
    print(f"running even part       = {example.running_even_part}")
    print(f"generated from (1,0,1)  = {example.generated_from_101}")


if __name__ == "__main__":
    main()
