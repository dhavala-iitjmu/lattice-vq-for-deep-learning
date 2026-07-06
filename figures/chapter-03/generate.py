"""Generate Chapter 3 SVG figures using only the Python standard library."""

from __future__ import annotations

import math
from pathlib import Path


OUT = Path(__file__).resolve().parent
WIDTH = 760
HEIGHT = 360
BLUE = "#2f6f9f"
ORANGE = "#d9822b"
GREEN = "#2e8b57"
PURPLE = "#8e44ad"
DARK = "#17202a"
GRID = "#d6dbdf"


def write_svg(name: str, body: str) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 z" fill="{DARK}" />
    </marker>
  </defs>
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: {DARK}; }}
    .title {{ font-size: 20px; font-weight: 700; }}
    .label {{ font-size: 13px; }}
    .small {{ font-size: 12px; fill: #566573; }}
    .axis {{ stroke: #5d6d7e; stroke-width: 1.5; }}
    .grid {{ stroke: {GRID}; stroke-width: 1; }}
  </style>
{body}
</svg>
"""
    (OUT / name).write_text(svg)


def title(text: str) -> str:
    return f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />\n<text class="title" x="48" y="32">{text}</text>'


def xy(point: tuple[float, float], origin: tuple[float, float] = (380, 185), scale: float = 58) -> tuple[float, float]:
    return origin[0] + point[0] * scale, origin[1] - point[1] * scale


def axes(origin: tuple[float, float] = (380, 185), scale: float = 58, extent: int = 4) -> str:
    parts = []
    ox, oy = origin
    for value in range(-extent, extent + 1):
        x = ox + value * scale
        y = oy - value * scale
        parts.append(f'<line class="grid" x1="{x:.1f}" y1="54" x2="{x:.1f}" y2="312" />')
        parts.append(f'<line class="grid" x1="148" y1="{y:.1f}" x2="612" y2="{y:.1f}" />')
    parts.append(f'<line class="axis" x1="148" y1="{oy}" x2="612" y2="{oy}" />')
    parts.append(f'<line class="axis" x1="{ox}" y1="54" x2="{ox}" y2="312" />')
    return "\n".join(parts)


def arrow(point: tuple[float, float], color: str, label: str, origin: tuple[float, float] = (380, 185)) -> str:
    x, y = xy(point, origin)
    ox, oy = origin
    label_y = y - 10 if y < oy else y + 22
    return "\n".join(
        [
            f'<line x1="{ox}" y1="{oy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="4" marker-end="url(#arrow)" />',
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" />',
            f'<text class="label" text-anchor="middle" x="{x:.1f}" y="{label_y:.1f}">{label}</text>',
        ]
    )


def two_dimensional_vectors() -> None:
    parts = [title("Two-dimensional vector slice"), axes()]
    parts.append(arrow((0.73, -1.84), BLUE, "w first 2"))
    parts.append(arrow((2.0, 1.0), ORANGE, "x first 2"))
    parts.append('<text class="small" x="48" y="334">Only the first two coordinates are drawn; the running vectors are eight-dimensional.</text>')
    write_svg("two-dimensional-vectors.svg", "\n".join(parts))


def norm_circles() -> None:
    origin = (380, 185)
    scale = 58
    parts = [title("Euclidean norm as distance from the origin"), axes(origin=origin, scale=scale)]
    for radius in (1, 2, 3):
        parts.append(f'<circle cx="{origin[0]}" cy="{origin[1]}" r="{radius * scale}" fill="none" stroke="{GRID}" stroke-width="3" />')
        parts.append(f'<text class="small" x="{origin[0] + radius * scale + 6}" y="{origin[1] - 5}">norm {radius}</text>')
    parts.append(arrow((2.0, 1.0), ORANGE, "x slice", origin=origin))
    write_svg("norm-circles.svg", "\n".join(parts))


def distance_between_points() -> None:
    origin = (380, 185)
    target = (0.73, -1.84)
    rounded = (1.0, -2.0)
    tx, ty = xy(target, origin)
    rx, ry = xy(rounded, origin)
    parts = [title("Distance between two points"), axes(origin=origin)]
    parts.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{rx:.1f}" y2="{ry:.1f}" stroke="{PURPLE}" stroke-width="4" />')
    parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="8" fill="{BLUE}" />')
    parts.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="8" fill="{ORANGE}" />')
    parts.append(f'<text class="label" x="{tx + 12:.1f}" y="{ty - 8:.1f}">floating point</text>')
    parts.append(f'<text class="label" x="{rx + 12:.1f}" y="{ry + 22:.1f}">rounded</text>')
    parts.append('<text class="small" x="48" y="334">The line segment is the Euclidean error in this two-coordinate slice.</text>')
    write_svg("distance-between-points.svg", "\n".join(parts))


def dot_product_angle() -> None:
    origin = (380, 200)
    parts = [title("Dot product depends on angle"), axes(origin=origin, scale=58, extent=3)]
    parts.append(arrow((0.73, -1.84), BLUE, "w slice", origin=origin))
    parts.append(arrow((2.0, 1.0), ORANGE, "x slice", origin=origin))
    parts.append(f'<path d="M {origin[0] + 42} {origin[1] - 20} A 56 56 0 0 1 {origin[0] + 18} {origin[1] + 54}" fill="none" stroke="{PURPLE}" stroke-width="3" />')
    parts.append(f'<text class="label" x="{origin[0] + 52}" y="{origin[1] + 22}">angle</text>')
    parts.append('<text class="small" x="48" y="334">A dot product is positive, zero, or negative depending on directional alignment.</text>')
    write_svg("dot-product-angle.svg", "\n".join(parts))


def nearest_neighbor() -> None:
    origin = (380, 185)
    scale = 58
    target = (0.73, -1.84)
    candidates = {
        0: (0.0, 0.0),
        1: (1.0, -2.0),
        2: (1.0, 0.0),
        3: (1.0, -1.0),
    }
    tx, ty = xy(target, origin, scale)
    parts = [title("Nearest-neighbor selection"), axes(origin=origin, scale=scale)]
    for index, point in candidates.items():
        x, y = xy(point, origin, scale)
        color = GREEN if index == 1 else "#7f8c8d"
        radius = 10 if index == 1 else 7
        parts.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="2" opacity="0.45" />')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}" />')
        parts.append(f'<text class="small" text-anchor="middle" x="{x:.1f}" y="{y - 14:.1f}">{index}</text>')
    parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="8" fill="{BLUE}" />')
    parts.append(f'<text class="label" x="{tx + 12:.1f}" y="{ty + 24:.1f}">target</text>')
    parts.append('<text class="small" x="48" y="334">Candidate 1 is selected because it has the smallest distance to the target.</text>')
    write_svg("nearest-neighbor.svg", "\n".join(parts))


def main() -> None:
    two_dimensional_vectors()
    norm_circles()
    distance_between_points()
    dot_product_angle()
    nearest_neighbor()


if __name__ == "__main__":
    main()

