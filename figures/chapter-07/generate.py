"""Generate Chapter 7 SVG figures using only the Python standard library."""

from __future__ import annotations

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
        parts.append(f'<line class="grid" x1="150" y1="{y:.1f}" x2="610" y2="{y:.1f}" />')
    parts.append(f'<line class="axis" x1="150" y1="{oy}" x2="610" y2="{oy}" />')
    parts.append(f'<line class="axis" x1="{ox}" y1="52" x2="{ox}" y2="314" />')
    return "\n".join(parts)


def nearest_lattice_point() -> None:
    parts = [title("Nearest lattice point in an even-parity slice"), axes()]
    target = (0.73, -1.84)
    nearest = (1, -1)
    for a in range(-4, 5):
        for b in range(-3, 4):
            color = GREEN if (a + b) % 2 == 0 else GRAY
            radius = 7 if color == GREEN else 4
            opacity = "1" if color == GREEN else "0.35"
            x, y = xy((a, b))
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}" opacity="{opacity}" />')
    tx, ty = xy(target)
    nx, ny = xy(nearest)
    parts.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{PURPLE}" stroke-width="4" />')
    parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="9" fill="{BLUE}" />')
    parts.append(f'<text class="label" x="{tx + 12:.1f}" y="{ty + 20:.1f}">target slice</text>')
    parts.append(f'<text class="label" x="{nx + 12:.1f}" y="{ny - 10:.1f}">nearest even point</text>')
    parts.append('<text class="small" x="48" y="334">This visible slice shows the nearest-point idea; Chapter 7 computes in four dimensions.</text>')
    write_svg("nearest-lattice-point.svg", "\n".join(parts))


def rounding_to_z4() -> None:
    parts = [title("Step 1: coordinate-wise rounding to Z^4")]
    rows = [
        ("1", "0.73", "1", "-0.27"),
        ("2", "-1.84", "-2", "0.16"),
        ("3", "2.11", "2", "0.11"),
        ("4", "-0.45", "0", "-0.45"),
    ]
    headers = ["coord", "target", "rounded", "error"]
    x_positions = [100, 235, 380, 525]
    for x, header in zip(x_positions, headers):
        parts.append(f'<text class="label" text-anchor="middle" x="{x}" y="84">{header}</text>')
    for row_index, row in enumerate(rows):
        y = 112 + row_index * 46
        parts.append(f'<rect x="64" y="{y - 25}" width="540" height="36" rx="5" fill="#f8f9f9" stroke="{GRID}" />')
        for x, value in zip(x_positions, row):
            parts.append(f'<text class="label" text-anchor="middle" x="{x}" y="{y}">{value}</text>')
    parts.append('<text class="small" x="64" y="322">The rounded vector is (1, -2, 2, 0), whose sum is odd.</text>')
    write_svg("rounding-to-z4.svg", "\n".join(parts))


def parity_correction() -> None:
    parts = [title("Step 2: repair D4 parity")]
    parts.append(f'<rect x="76" y="96" width="190" height="62" rx="6" fill="#f8f9f9" stroke="{ORANGE}" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="171" y="133">(1, -2, 2, 0)</text>')
    parts.append('<text class="small" text-anchor="middle" x="171" y="152">sum = 1, odd</text>')
    parts.append(f'<line x1="286" y1="127" x2="458" y2="127" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<text class="small" text-anchor="middle" x="372" y="112">change coordinate 4</text>')
    parts.append(f'<rect x="480" y="96" width="190" height="62" rx="6" fill="#f8f9f9" stroke="{GREEN}" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="575" y="133">(1, -2, 2, -1)</text>')
    parts.append('<text class="small" text-anchor="middle" x="575" y="152">sum = 0, even</text>')
    parts.append(f'<rect x="106" y="226" width="548" height="42" rx="6" fill="{PURPLE}" opacity="0.13" stroke="{PURPLE}" />')
    parts.append('<text class="small" text-anchor="middle" x="380" y="252">coordinate 4 had the largest absolute rounding error: 0.45</text>')
    write_svg("parity-correction.svg", "\n".join(parts))


def voronoi_region() -> None:
    parts = [title("Voronoi region in an even-parity slice"), axes()]
    diamond = [xy((0, 1)), xy((1, 0)), xy((0, -1)), xy((-1, 0))]
    rendered = " ".join(f"{x:.1f},{y:.1f}" for x, y in diamond)
    parts.append(f'<polygon points="{rendered}" fill="{BLUE}" opacity="0.22" stroke="{BLUE}" stroke-width="3" />')
    for point in [(0, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (2, 0), (-2, 0), (0, 2), (0, -2)]:
        x, y = xy(point)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{GREEN}" />')
    ox, oy = xy((0, 0))
    parts.append(f'<text class="label" x="{ox + 10:.1f}" y="{oy - 12:.1f}">origin cell</text>')
    parts.append('<text class="small" x="48" y="334">The four-dimensional D4 Voronoi cell is harder to draw; this slice shows the same nearest-cell idea.</text>')
    write_svg("voronoi-region.svg", "\n".join(parts))


def decoder_flow() -> None:
    parts = [title("Round-and-fix decoder flow")]
    boxes = [
        (66, 118, "target v"),
        (214, 118, "round to u"),
        (362, 118, "sum even?"),
        (510, 82, "return u"),
        (510, 154, "repair largest error"),
    ]
    for x, y, label in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="118" height="48" rx="7" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 59}" y="{y + 30}">{label}</text>')
    arrows = [
        (184, 142, 214, 142),
        (332, 142, 362, 142),
        (480, 130, 510, 106),
        (480, 154, 510, 178),
    ]
    for x1, y1, x2, y2 in arrows:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<text class="small" x="486" y="112">yes</text>')
    parts.append('<text class="small" x="486" y="176">no</text>')
    parts.append(f'<line x1="569" y1="202" x2="569" y2="246" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append(f'<rect x="510" y="250" width="118" height="48" rx="7" fill="#f8f9f9" stroke="{GREEN}" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="569" y="280">return fixed u</text>')
    parts.append('<text class="small" x="68" y="314">The decoder needs one pass over the coordinates and at most one coordinate update.</text>')
    write_svg("decoder-flow.svg", "\n".join(parts))


def main() -> None:
    nearest_lattice_point()
    rounding_to_z4()
    parity_correction()
    voronoi_region()
    decoder_flow()


if __name__ == "__main__":
    main()

