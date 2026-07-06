"""Generate Chapter 5 SVG figures using only the Python standard library."""

from __future__ import annotations

import math
from pathlib import Path


OUT = Path(__file__).resolve().parent
WIDTH = 760
HEIGHT = 360
BLUE = "#2f6f9f"
ORANGE = "#d9822b"
GREEN = "#2e8b57"
DARK = "#17202a"
GRID = "#d6dbdf"
GRAY = "#7f8c8d"


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


def xy(point: tuple[float, float], origin: tuple[float, float] = (380, 185), scale: float = 48) -> tuple[float, float]:
    return origin[0] + point[0] * scale, origin[1] - point[1] * scale


def axes(origin: tuple[float, float] = (380, 185), scale: float = 48, extent: int = 4) -> str:
    parts = []
    ox, oy = origin
    for value in range(-extent, extent + 1):
        x = ox + value * scale
        y = oy - value * scale
        parts.append(f'<line class="grid" x1="{x:.1f}" y1="52" x2="{x:.1f}" y2="314" />')
        parts.append(f'<line class="grid" x1="140" y1="{y:.1f}" x2="620" y2="{y:.1f}" />')
    parts.append(f'<line class="axis" x1="140" y1="{oy}" x2="620" y2="{oy}" />')
    parts.append(f'<line class="axis" x1="{ox}" y1="52" x2="{ox}" y2="314" />')
    return "\n".join(parts)


def lattice_point(point: tuple[float, float], color: str = DARK, radius: int = 5) -> str:
    x, y = xy(point)
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}" />'


def arrow(point: tuple[float, float], color: str, label: str) -> str:
    ox, oy = (380, 185)
    x, y = xy(point)
    return "\n".join(
        [
            f'<line x1="{ox}" y1="{oy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="4" marker-end="url(#arrow)" />',
            f'<text class="label" x="{x + 8:.1f}" y="{y - 8:.1f}">{label}</text>',
        ]
    )


def polygon(points: list[tuple[float, float]], fill: str, stroke: str = DARK, opacity: float = 0.35) -> str:
    rendered = " ".join(f"{xy(point)[0]:.1f},{xy(point)[1]:.1f}" for point in points)
    return f'<polygon points="{rendered}" fill="{fill}" opacity="{opacity}" stroke="{stroke}" stroke-width="2" />'


def integer_lattice() -> None:
    parts = [title("Integer lattice Z^2"), axes()]
    for a in range(-4, 5):
        for b in range(-3, 4):
            parts.append(lattice_point((a, b), DARK, 5))
    parts.append('<text class="small" x="48" y="334">Only a finite window is drawn. The lattice continues forever.</text>')
    write_svg("integer-lattice.svg", "\n".join(parts))


def basis_vectors() -> None:
    parts = [title("Basis vectors generate Z^2"), axes()]
    for a in range(-4, 5):
        for b in range(-3, 4):
            parts.append(lattice_point((a, b), GRAY, 4))
    parts.append(arrow((1, 0), BLUE, "g1 = (1, 0)"))
    parts.append(arrow((0, 1), ORANGE, "g2 = (0, 1)"))
    parts.append('<text class="small" x="48" y="334">Integer combinations of these two arrows generate every grid point.</text>')
    write_svg("basis-vectors.svg", "\n".join(parts))


def generator_matrix() -> None:
    parts = [title("Generator matrix as a point generator")]
    parts.append('<rect x="70" y="110" width="150" height="90" rx="6" fill="#f8f9f9" stroke="#d6dbdf" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="145" y="145">integer</text>')
    parts.append('<text class="label" text-anchor="middle" x="145" y="170">coefficients z</text>')
    parts.append(f'<line x1="230" y1="155" x2="332" y2="155" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<rect x="350" y="96" width="160" height="118" rx="6" fill="#f8f9f9" stroke="#d6dbdf" stroke-width="2" />')
    parts.append('<text class="title" text-anchor="middle" x="430" y="137">G</text>')
    parts.append('<text class="small" text-anchor="middle" x="430" y="164">basis vectors</text>')
    parts.append('<text class="small" text-anchor="middle" x="430" y="184">as columns</text>')
    parts.append(f'<line x1="520" y1="155" x2="622" y2="155" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<rect x="640" y="110" width="70" height="90" rx="6" fill="#f8f9f9" stroke="#d6dbdf" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="675" y="145">point</text>')
    parts.append('<text class="label" text-anchor="middle" x="675" y="170">Gz</text>')
    parts.append('<text class="small" x="74" y="274">The matrix is the recipe. The integer vector chooses the recipe inputs.</text>')
    write_svg("generator-matrix.svg", "\n".join(parts))


def hexagonal_lattice() -> None:
    parts = [title("Hexagonal lattice preview"), axes()]
    sqrt3 = math.sqrt(3)
    for a in range(-4, 5):
        for b in range(-4, 5):
            point = (a + 0.5 * b, (sqrt3 / 2.0) * b)
            x, y = xy(point)
            if 120 <= x <= 640 and 52 <= y <= 314:
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{DARK}" />')
    parts.append(arrow((1, 0), BLUE, "g1"))
    parts.append(arrow((0.5, sqrt3 / 2.0), ORANGE, "g2"))
    parts.append('<text class="small" x="48" y="334">The tilted basis produces a triangular point pattern with hexagonal Voronoi cells.</text>')
    write_svg("hexagonal-lattice.svg", "\n".join(parts))


def fundamental_region() -> None:
    parts = [title("Fundamental regions tile space"), axes()]
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    tilted = [(2, 0), (3, 0), (3.5, math.sqrt(3) / 2.0), (2.5, math.sqrt(3) / 2.0)]
    parts.append(polygon(square, BLUE))
    parts.append(polygon(tilted, ORANGE))
    parts.append('<text class="label" x="424" y="178">square tile</text>')
    parts.append('<text class="label" x="520" y="126">tilted tile</text>')
    parts.append('<text class="small" x="48" y="334">A fundamental region is one repeated tile of the lattice.</text>')
    write_svg("fundamental-region.svg", "\n".join(parts))


def voronoi_cells() -> None:
    parts = [title("Voronoi cells around the origin"), axes()]
    square = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]
    radius = 0.58
    hexagon = []
    for k in range(6):
        angle = math.radians(30 + 60 * k)
        hexagon.append((2.4 + radius * math.cos(angle), radius * math.sin(angle)))
    parts.append(polygon(square, BLUE, opacity=0.4))
    parts.append(polygon(hexagon, GREEN, opacity=0.4))
    parts.append(lattice_point((0, 0), DARK, 6))
    parts.append(lattice_point((2.4, 0), DARK, 6))
    parts.append('<text class="label" x="332" y="146">Z2 cell</text>')
    parts.append('<text class="label" x="510" y="146">hex cell</text>')
    parts.append('<text class="small" x="48" y="334">Voronoi cells describe nearest-lattice-point decisions.</text>')
    write_svg("voronoi-cells.svg", "\n".join(parts))


def main() -> None:
    integer_lattice()
    basis_vectors()
    generator_matrix()
    hexagonal_lattice()
    fundamental_region()
    voronoi_cells()


if __name__ == "__main__":
    main()

