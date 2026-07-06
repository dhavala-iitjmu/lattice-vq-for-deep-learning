"""Generate Chapter 8 SVG figures using only the Python standard library."""

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


def xy(point: tuple[float, float], origin: tuple[float, float] = (380, 190), scale: float = 52) -> tuple[float, float]:
    return origin[0] + point[0] * scale, origin[1] - point[1] * scale


def axes(origin: tuple[float, float] = (380, 190), scale: float = 52, extent: int = 4) -> str:
    parts = []
    ox, oy = origin
    for value in range(-extent, extent + 1):
        x = ox + value * scale
        y = oy - value * scale
        parts.append(f'<line class="grid" x1="{x:.1f}" y1="58" x2="{x:.1f}" y2="312" />')
        parts.append(f'<line class="grid" x1="150" y1="{y:.1f}" x2="610" y2="{y:.1f}" />')
    parts.append(f'<line class="axis" x1="150" y1="{oy}" x2="610" y2="{oy}" />')
    parts.append(f'<line class="axis" x1="{ox}" y1="58" x2="{ox}" y2="312" />')
    return "\n".join(parts)


def lattice_quantizer() -> None:
    parts = [title("Lattice quantization: target to nearest D4 point"), axes()]
    target = (0.73, -1.84)
    nearest = (1, -2)
    for a in range(-4, 5):
        for b in range(-3, 4):
            if (a + b) % 2 == 0:
                x, y = xy((a, b))
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{GREEN}" />')
    tx, ty = xy(target)
    nx, ny = xy(nearest)
    parts.append(f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{PURPLE}" stroke-width="4" marker-end="url(#arrow)" />')
    parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="9" fill="{BLUE}" />')
    parts.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="10" fill="{ORANGE}" />')
    parts.append(f'<text class="label" x="{tx + 12:.1f}" y="{ty - 12:.1f}">floating-point target</text>')
    parts.append(f'<text class="label" x="{nx + 12:.1f}" y="{ny + 20:.1f}">nearest lattice point</text>')
    parts.append('<text class="small" x="48" y="334">The drawing is a visible parity slice; the chapter quantizes four-dimensional blocks.</text>')
    write_svg("lattice-quantizer.svg", "\n".join(parts))


def voronoi_partition() -> None:
    parts = [title("Voronoi quantization: choose the containing cell"), axes()]
    cells = [(-2, 0), (0, 0), (2, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]
    for center in cells:
        diamond = [xy((center[0], center[1] + 1)), xy((center[0] + 1, center[1])), xy((center[0], center[1] - 1)), xy((center[0] - 1, center[1]))]
        rendered = " ".join(f"{x:.1f},{y:.1f}" for x, y in diamond)
        parts.append(f'<polygon points="{rendered}" fill="{BLUE}" opacity="0.10" stroke="{BLUE}" stroke-width="2" />')
    for center in cells:
        x, y = xy(center)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{GREEN}" />')
    for point in [(0.25, 0.35), (1.2, 0.55), (-1.25, -0.55)]:
        x, y = xy(point)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{ORANGE}" />')
    parts.append('<text class="small" x="48" y="334">Nearest-point decoding and Voronoi-cell assignment are the same operation.</text>')
    write_svg("voronoi-partition.svg", "\n".join(parts))


def scaled_lattice() -> None:
    parts = [title("Scaling changes effective lattice spacing")]
    rows = [
        (88, "beta = 0.5", 104, 2.0),
        (178, "beta = 1.0", 52, 1.0),
        (268, "beta = 2.0", 26, 0.5),
    ]
    for y, label, spacing, step in rows:
        parts.append(f'<text class="label" x="64" y="{y + 5}">{label}</text>')
        parts.append(f'<line class="axis" x1="190" y1="{y}" x2="690" y2="{y}" />')
        x = 190
        index = 0
        while x <= 690:
            parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{GREEN}" />')
            if index < 4:
                parts.append(f'<text class="small" text-anchor="middle" x="{x}" y="{y + 24}">{index * step:g}</text>')
            x += spacing
            index += 1
    parts.append('<text class="small" x="64" y="334">Larger beta gives a finer reconstruction grid in the original weight units.</text>')
    write_svg("scaled-lattice.svg", "\n".join(parts))


def coarse_vs_fine() -> None:
    parts = [title("Example distortion decreases as beta increases")]
    values = [(0.5, 0.3135), (1.0, 0.1002), (2.0, 0.0302)]
    max_value = 0.34
    chart_x = 136
    chart_y = 288
    chart_h = 205
    bar_w = 92
    gap = 78
    parts.append(f'<line class="axis" x1="{chart_x - 30}" y1="{chart_y}" x2="650" y2="{chart_y}" />')
    parts.append(f'<line class="axis" x1="{chart_x - 30}" y1="{chart_y - chart_h}" x2="{chart_x - 30}" y2="{chart_y}" />')
    for index, (beta, mse) in enumerate(values):
        h = chart_h * mse / max_value
        x = chart_x + index * (bar_w + gap)
        y = chart_y - h
        color = ORANGE if beta == 0.5 else BLUE if beta == 1.0 else GREEN
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" fill="{color}" opacity="0.86" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + bar_w / 2}" y="{chart_y + 26}">beta {beta:g}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + bar_w / 2}" y="{y - 8:.1f}">{mse:.4f}</text>')
    parts.append('<text class="small" x="64" y="334">These values are for the three Chapter 8 example blocks; they demonstrate scaling, not a universal guarantee.</text>')
    write_svg("coarse-vs-fine.svg", "\n".join(parts))


def infinite_scaled_lattice() -> None:
    parts = [title("Scaling does not make the lattice finite")]
    y = 178
    parts.append(f'<line class="axis" x1="74" y1="{y}" x2="690" y2="{y}" marker-end="url(#arrow)" />')
    labels = ["0", "1", "2", "3", "4", "5", "..."]
    xs = [92, 184, 276, 368, 460, 552, 644]
    for x, label in zip(xs, labels):
        if label == "...":
            parts.append(f'<text class="title" text-anchor="middle" x="{x}" y="{y + 6}">...</text>')
        else:
            parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{GREEN}" />')
            parts.append(f'<text class="small" text-anchor="middle" x="{x}" y="{y + 28}">({label},0,0,0)</text>')
    parts.append(f'<rect x="92" y="74" width="460" height="42" rx="7" fill="{BLUE}" opacity="0.12" stroke="{BLUE}" />')
    parts.append('<text class="label" text-anchor="middle" x="322" y="101">beta changes spacing, but the ray still continues forever</text>')
    parts.append('<text class="small" x="64" y="334">A finite bit rate requires a finite set of representatives, introduced in Chapter 9.</text>')
    write_svg("infinite-scaled-lattice.svg", "\n".join(parts))


def main() -> None:
    lattice_quantizer()
    voronoi_partition()
    scaled_lattice()
    coarse_vs_fine()
    infinite_scaled_lattice()


if __name__ == "__main__":
    main()
