"""Reference implementation for Chapter 18: binary-domain computation."""

from __future__ import annotations

from dataclasses import dataclass

from chapter_17_bit_planes import RUNNING_D4_POINT, extract_bit_planes


Vector = tuple[float, ...]
BitPlane = tuple[int, ...]

ACTIVATION_BLOCK: Vector = (2.0, 1.0, -1.0, 3.0)


@dataclass(frozen=True)
class PlaneContribution:
    plane_index: int
    bits: BitPlane
    plane_dot: float
    weight: int
    contribution: float


@dataclass(frozen=True)
class Chapter18Example:
    vector: tuple[int, ...]
    activation: Vector
    contributions: tuple[PlaneContribution, ...]
    ordinary_dot: float
    bitplane_dot: float
    evidence_labels: dict[str, str]


def dot(left: tuple[float, ...] | tuple[int, ...], right: Vector) -> float:
    if len(left) != len(right):
        raise ValueError("dot requires equal lengths")
    return sum(a * b for a, b in zip(left, right))


def twos_complement_plane_weights(width: int) -> tuple[int, ...]:
    if width <= 0:
        raise ValueError("width must be positive")
    positive = [1 << bit for bit in range(width - 1)]
    return tuple(positive + [-(1 << (width - 1))])


def bitplane_dot(vector: tuple[int, ...], activation: Vector, width: int) -> tuple[float, tuple[PlaneContribution, ...]]:
    planes = extract_bit_planes(vector, width)
    weights = twos_complement_plane_weights(width)
    contributions = []
    total = 0.0
    for index, (plane, weight) in enumerate(zip(planes, weights)):
        plane_dot = dot(plane, activation)
        contribution = weight * plane_dot
        total += contribution
        contributions.append(
            PlaneContribution(
                plane_index=index,
                bits=plane,
                plane_dot=plane_dot,
                weight=weight,
                contribution=contribution,
            )
        )
    return total, tuple(contributions)


def label_claim(claim: str) -> str:
    labels = {
        "bitplane_dot_identity": "established",
        "hnlq_lut_dot_identity": "established",
        "structured_bitplane_kernel": "experimental",
        "binary_domain_gemm": "speculative",
    }
    if claim not in labels:
        raise ValueError("unknown claim")
    return labels[claim]


def build_example() -> Chapter18Example:
    total, contributions = bitplane_dot(RUNNING_D4_POINT, ACTIVATION_BLOCK, width=4)
    ordinary = dot(RUNNING_D4_POINT, ACTIVATION_BLOCK)
    labels = {
        claim: label_claim(claim)
        for claim in (
            "bitplane_dot_identity",
            "hnlq_lut_dot_identity",
            "structured_bitplane_kernel",
            "binary_domain_gemm",
        )
    }
    return Chapter18Example(
        vector=RUNNING_D4_POINT,
        activation=ACTIVATION_BLOCK,
        contributions=contributions,
        ordinary_dot=ordinary,
        bitplane_dot=total,
        evidence_labels=labels,
    )


def main() -> None:
    example = build_example()
    print(f"ordinary dot = {example.ordinary_dot}")
    print(f"bitplane dot = {example.bitplane_dot}")
    for contribution in example.contributions:
        print(
            f"plane {contribution.plane_index}: bits={contribution.bits}, "
            f"plane_dot={contribution.plane_dot}, weight={contribution.weight}, "
            f"contribution={contribution.contribution}"
        )
    print(f"labels = {example.evidence_labels}")


if __name__ == "__main__":
    main()
