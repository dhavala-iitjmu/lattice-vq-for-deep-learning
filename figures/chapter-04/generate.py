"""Generate Chapter 4 SVG figures using only the Python standard library."""

from __future__ import annotations

import math
from itertools import product
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
GRAY = "#7f8c8d"

LEVELS = (
    (-2, 0, 1, 3),
    (-2, 0, 1, 3),
    (-2, 0, 2, 3),
    (-2, 0, 1, 3),
)
BLOCK_1 = (0.73, -1.84, 2.11, -0.45)
BLOCK_2 = (1.27, 0.08, -2.36, 3.14)


def codebook() -> tuple[tuple[int, ...], ...]:
    return tuple(product(*LEVELS))


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
        parts.append(f'<line class="grid" x1="120" y1="{y:.1f}" x2="640" y2="{y:.1f}" />')
    parts.append(f'<line class="axis" x1="120" y1="{oy}" x2="640" y2="{oy}" />')
    parts.append(f'<line class="axis" x1="{ox}" y1="54" x2="{ox}" y2="312" />')
    return "\n".join(parts)


def squared_distance_2d(point: tuple[float, float], codeword: tuple[float, float]) -> float:
    return sum((a - b) ** 2 for a, b in zip(point, codeword))


def codebook_points() -> None:
    parts = [title("Finite codebook: two-dimensional projection"), axes()]
    seen = set()
    for codeword in codebook():
        point = (codeword[0], codeword[1])
        if point in seen:
            continue
        seen.add(point)
        x, y = xy(point)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{GRAY}" opacity="0.55" />')
    for point, color, label in ((BLOCK_1[:2], BLUE, "block 1"), (BLOCK_2[:2], ORANGE, "block 2")):
        x, y = xy(point)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{color}" />')
        parts.append(f'<text class="label" x="{x + 12:.1f}" y="{y - 10:.1f}">{label}</text>')
    parts.append('<text class="small" x="48" y="334">The full codebook has 256 four-dimensional entries; this shows only the first two coordinates.</text>')
    write_svg("codebook-points.svg", "\n".join(parts))


def voronoi_partition() -> None:
    origin = (380, 185)
    scale = 58
    candidates = ((0, 0), (1, -2), (1, 0), (1, -1))
    colors = ("#d6eaf8", "#d5f5e3", "#fdebd0", "#eadcf8")
    parts = [title("Voronoi partition from nearest codewords")]
    step = 10
    for px in range(120, 641, step):
        for py in range(54, 313, step):
            point = ((px - origin[0]) / scale, (origin[1] - py) / scale)
            nearest = min(range(len(candidates)), key=lambda i: squared_distance_2d(point, candidates[i]))
            parts.append(f'<rect x="{px}" y="{py}" width="{step + 1}" height="{step + 1}" fill="{colors[nearest]}" />')
    parts.append(axes(origin=origin, scale=scale))
    for index, candidate in enumerate(candidates):
        x, y = xy(candidate, origin, scale)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{DARK}" />')
        parts.append(f'<text class="small" text-anchor="middle" x="{x:.1f}" y="{y - 12:.1f}">{index}</text>')
    parts.append('<text class="small" x="48" y="334">Each colored region contains points that encode to the same nearest codeword.</text>')
    write_svg("voronoi-partition.svg", "\n".join(parts))


def encoding_nearest_codeword() -> None:
    origin = (380, 185)
    scale = 58
    candidates = {
        73: (0, -2),
        137: (1, -2),
        141: (1, -2.55),
        147: (1, 0),
    }
    target = BLOCK_1[:2]
    tx, ty = xy(target, origin, scale)
    parts = [title("Encoding: choose the nearest codeword"), axes(origin=origin, scale=scale)]
    for index, point in candidates.items():
        x, y = xy(point, origin, scale)
        color = GREEN if index == 137 else GRAY
        width = 4 if index == 137 else 2
        parts.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="{width}" opacity="0.65" />')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{color}" />')
        parts.append(f'<text class="small" text-anchor="middle" x="{x:.1f}" y="{y - 13:.1f}">{index}</text>')
    parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="10" fill="{BLUE}" />')
    parts.append(f'<text class="label" x="{tx + 13:.1f}" y="{ty + 21:.1f}">target block</text>')
    parts.append('<text class="small" x="48" y="334">The encoder stores index 137 because its codeword is nearest.</text>')
    write_svg("encoding-nearest-codeword.svg", "\n".join(parts))


def decoding_index() -> None:
    parts = [title("Decoding: index to representative vector")]
    rows = [
        ("137", "(1, -2, 2, 0)", BLUE, 94),
        ("147", "(1, 0, -2, 3)", ORANGE, 194),
    ]
    for index, vector, color, y in rows:
        parts.append(f'<rect x="76" y="{y}" width="118" height="54" rx="6" fill="{color}" opacity="0.15" stroke="{color}" stroke-width="2" />')
        parts.append(f'<text class="title" text-anchor="middle" x="135" y="{y + 35}">{index}</text>')
        parts.append(f'<line x1="210" y1="{y + 27}" x2="344" y2="{y + 27}" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
        parts.append(f'<rect x="366" y="{y}" width="260" height="54" rx="6" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="496" y="{y + 34}">{vector}</text>')
    parts.append('<text class="small" x="76" y="292">Decoding is a codebook lookup. Encoding was the expensive nearest-neighbor search.</text>')
    write_svg("decoding-index.svg", "\n".join(parts))


def rate_distortion() -> None:
    parts = [title("Rate-distortion intuition")]
    left = 94
    bottom = 282
    width = 560
    height = 210
    parts.append(f'<line class="axis" x1="{left}" y1="{bottom}" x2="{left + width}" y2="{bottom}" />')
    parts.append(f'<line class="axis" x1="{left}" y1="{bottom}" x2="{left}" y2="{bottom - height}" />')
    points = [(0, 170), (1, 118), (2, 82), (3, 56), (4, 40)]
    path = []
    for i, (rate, distortion) in enumerate(points):
        x = left + 80 + rate * 105
        y = bottom - distortion
        path.append(("M" if i == 0 else "L") + f" {x} {y}")
        parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{PURPLE}" />')
        parts.append(f'<text class="small" text-anchor="middle" x="{x}" y="{bottom + 24}">{2 ** (rate + 4)}</text>')
    parts.insert(3, f'<path d="{" ".join(path)}" fill="none" stroke="{PURPLE}" stroke-width="3" />')
    parts.append('<text class="small" x="250" y="330">Codebook size K</text>')
    parts.append('<text class="small" transform="translate(34 242) rotate(-90)">Distortion</text>')
    parts.append('<text class="small" x="120" y="72">More codewords: lower distortion, more bits and search.</text>')
    write_svg("rate-distortion.svg", "\n".join(parts))


def main() -> None:
    codebook_points()
    voronoi_partition()
    encoding_nearest_codeword()
    decoding_index()
    rate_distortion()


if __name__ == "__main__":
    main()

