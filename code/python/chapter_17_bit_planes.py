"""Reference implementation for Chapter 17: bit-plane representations."""

from __future__ import annotations

from dataclasses import dataclass


IntVector = tuple[int, ...]
BitPlane = tuple[int, ...]

RUNNING_D4_POINT: IntVector = (1, 0, -2, 3)


@dataclass(frozen=True)
class Chapter17Example:
    vector: IntVector
    bit_width: int
    encoded_columns: tuple[str, ...]
    planes: tuple[BitPlane, ...]
    reconstructed: IntVector
    lsb_even_parity: bool


def to_twos_complement_bits(value: int, width: int) -> str:
    """Return a fixed-width two's-complement bit string."""

    if width <= 0:
        raise ValueError("width must be positive")
    minimum = -(1 << (width - 1))
    maximum = (1 << (width - 1)) - 1
    if value < minimum or value > maximum:
        raise ValueError("value out of range for width")
    encoded = value % (1 << width)
    return format(encoded, f"0{width}b")


def from_twos_complement_bits(bits: str) -> int:
    """Decode a fixed-width two's-complement bit string."""

    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("bits must be a nonempty binary string")
    width = len(bits)
    value = int(bits, 2)
    if bits[0] == "1":
        value -= 1 << width
    return value


def extract_bit_planes(vector: IntVector, width: int) -> tuple[BitPlane, ...]:
    """Extract bit planes from least significant to most significant."""

    columns = [to_twos_complement_bits(value, width) for value in vector]
    planes = []
    for bit_from_right in range(width):
        plane = tuple(int(column[width - 1 - bit_from_right]) for column in columns)
        planes.append(plane)
    return tuple(planes)


def reconstruct_from_bit_planes(planes: tuple[BitPlane, ...]) -> IntVector:
    """Reconstruct signed integers from bit planes."""

    if not planes:
        raise ValueError("planes must not be empty")
    width = len(planes)
    dimension = len(planes[0])
    if any(len(plane) != dimension for plane in planes):
        raise ValueError("all planes must have equal length")
    values = []
    for coordinate in range(dimension):
        bits = "".join(str(planes[width - 1 - bit][coordinate]) for bit in range(width))
        values.append(from_twos_complement_bits(bits))
    return tuple(values)


def lsb_is_even_parity(planes: tuple[BitPlane, ...]) -> bool:
    if not planes:
        raise ValueError("planes must not be empty")
    return sum(planes[0]) % 2 == 0


def build_example() -> Chapter17Example:
    width = 4
    planes = extract_bit_planes(RUNNING_D4_POINT, width)
    return Chapter17Example(
        vector=RUNNING_D4_POINT,
        bit_width=width,
        encoded_columns=tuple(to_twos_complement_bits(value, width) for value in RUNNING_D4_POINT),
        planes=planes,
        reconstructed=reconstruct_from_bit_planes(planes),
        lsb_even_parity=lsb_is_even_parity(planes),
    )


def main() -> None:
    example = build_example()
    print(f"vector          = {example.vector}")
    print(f"columns         = {example.encoded_columns}")
    print(f"planes LSB->MSB = {example.planes}")
    print(f"reconstructed   = {example.reconstructed}")
    print(f"LSB even parity = {example.lsb_even_parity}")


if __name__ == "__main__":
    main()
