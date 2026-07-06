"""Reference implementation for Chapter 12: HNLQ matrix multiplication."""

from __future__ import annotations

from dataclasses import dataclass

from chapter_01_quantization import ACTIVATIONS, dot
from chapter_10_hnlq import DEFAULT_BETA, DEFAULT_Q, DIGIT_REPRESENTATIVES, decode_indices
from chapter_11_one_sided_lut import build_lut, hnlq_dot_from_lut, split_blocks


Vector = tuple[float, ...]
IndexSequence = tuple[int, ...]
EncodedRow = tuple[IndexSequence, IndexSequence]

INDEX_MATRIX: tuple[EncodedRow, ...] = (
    ((14, 0, 4, 4), (12, 13, 2, 2)),
    ((0, 2, 8, 2), (14, 0, 4, 4)),
    ((12, 13, 2, 2), (0, 2, 8, 2)),
    ((15, 8, 2, 1), (12, 4, 0, 13)),
    ((2, 8, 2, 1), (5, 4, 12, 0)),
    ((10, 1, 7, 0), (3, 12, 0, 4)),
    ((1, 2, 3, 4), (5, 6, 7, 8)),
    ((14, 13, 12, 11), (10, 9, 8, 7)),
)


@dataclass(frozen=True)
class TrafficSummary:
    hnlq_indices: int
    reconstructed_weight_values: int
    lut_entries: int


@dataclass(frozen=True)
class Chapter12Example:
    output_from_lut: Vector
    output_from_reconstruction: Vector
    activation_table_count: int
    traffic: TrafficSummary


def build_activation_tables(
    activations: Vector,
    representatives: tuple[tuple[int, ...], ...] = DIGIT_REPRESENTATIVES,
    block_size: int = 4,
) -> tuple[tuple[float, ...], ...]:
    """Build one lookup table per activation block."""

    return tuple(build_lut(block, representatives) for block in split_blocks(activations, block_size))


def hnlq_matvec_lut(
    index_matrix: tuple[EncodedRow, ...],
    activation_tables: tuple[tuple[float, ...], ...],
    beta: float = DEFAULT_BETA,
    q: int = DEFAULT_Q,
) -> Vector:
    """Multiply an HNLQ-encoded matrix by an activation vector using LUTs."""

    outputs = []
    for row in index_matrix:
        if len(row) != len(activation_tables):
            raise ValueError("row block count must match activation table count")
        total = 0.0
        for block_indices, table in zip(row, activation_tables):
            total += hnlq_dot_from_lut(block_indices, table, beta, q)
        outputs.append(total)
    return tuple(outputs)


def reconstruct_row(
    row: EncodedRow,
    beta: float = DEFAULT_BETA,
    q: int = DEFAULT_Q,
) -> Vector:
    """Reconstruct one encoded row."""

    reconstructed: Vector = ()
    for block_indices in row:
        reconstructed += decode_indices(block_indices, beta, q)
    return reconstructed


def matvec_reconstruct_then_dot(
    index_matrix: tuple[EncodedRow, ...],
    activations: Vector,
    beta: float = DEFAULT_BETA,
    q: int = DEFAULT_Q,
) -> Vector:
    """Baseline matvec that reconstructs every row before the dot product."""

    return tuple(dot(reconstruct_row(row, beta, q), activations) for row in index_matrix)


def traffic_summary(
    index_matrix: tuple[EncodedRow, ...],
    activation_tables: tuple[tuple[float, ...], ...],
    row_width: int,
) -> TrafficSummary:
    """Return simple item counts for the toy memory-traffic comparison."""

    hnlq_indices = sum(len(block) for row in index_matrix for block in row)
    reconstructed_values = len(index_matrix) * row_width
    lut_entries = sum(len(table) for table in activation_tables)
    return TrafficSummary(
        hnlq_indices=hnlq_indices,
        reconstructed_weight_values=reconstructed_values,
        lut_entries=lut_entries,
    )


def build_example() -> Chapter12Example:
    """Build the numerical example used in Chapter 12."""

    tables = build_activation_tables(ACTIVATIONS)
    output_from_lut = hnlq_matvec_lut(INDEX_MATRIX, tables)
    output_from_reconstruction = matvec_reconstruct_then_dot(INDEX_MATRIX, ACTIVATIONS)
    return Chapter12Example(
        output_from_lut=output_from_lut,
        output_from_reconstruction=output_from_reconstruction,
        activation_table_count=len(tables),
        traffic=traffic_summary(INDEX_MATRIX, tables, row_width=len(ACTIVATIONS)),
    )


def main() -> None:
    example = build_example()
    print(f"LUT matvec output          = {tuple(round(value, 4) for value in example.output_from_lut)}")
    print(f"reconstruct matvec output  = {tuple(round(value, 4) for value in example.output_from_reconstruction)}")
    print(f"activation table count     = {example.activation_table_count}")
    print(f"HNLQ indices               = {example.traffic.hnlq_indices}")
    print(f"reconstructed weight values = {example.traffic.reconstructed_weight_values}")
    print(f"LUT entries                = {example.traffic.lut_entries}")


if __name__ == "__main__":
    main()
