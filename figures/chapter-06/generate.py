"""Generate Chapter 6 SVG figures using only the Python standard library."""

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


def xy(point: tuple[float, float], origin: tuple[float, float] = (380, 185), scale: float = 42) -> tuple[float, float]:
    return origin[0] + point[0] * scale, origin[1] - point[1] * scale


def axes(origin: tuple[float, float] = (380, 185), scale: float = 42, extent: int = 4) -> str:
    parts = []
    ox, oy = origin
    for value in range(-extent, extent + 1):
        x = ox + value * scale
        y = oy - value * scale
        parts.append(f'<line class="grid" x1="{x:.1f}" y1="52" x2="{x:.1f}" y2="314" />')
        parts.append(f'<line class="grid" x1="190" y1="{y:.1f}" x2="570" y2="{y:.1f}" />')
    parts.append(f'<line class="axis" x1="190" y1="{oy}" x2="570" y2="{oy}" />')
    parts.append(f'<line class="axis" x1="{ox}" y1="52" x2="{ox}" y2="314" />')
    return "\n".join(parts)


def parity_slice() -> None:
    parts = [title("D4 parity slice: v3 = v4 = 0"), axes()]
    for a in range(-4, 5):
        for b in range(-3, 4):
            x, y = xy((a, b))
            color = GREEN if (a + b) % 2 == 0 else GRAY
            radius = 7 if color == GREEN else 5
            opacity = "1" if color == GREEN else "0.45"
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{color}" opacity="{opacity}" />')
    parts.append(f'<circle cx="610" cy="110" r="7" fill="{GREEN}" />')
    parts.append('<text class="small" x="628" y="114">even sum: in D4 slice</text>')
    parts.append(f'<circle cx="610" cy="140" r="5" fill="{GRAY}" opacity="0.45" />')
    parts.append('<text class="small" x="628" y="144">odd sum: outside</text>')
    parts.append('<text class="small" x="48" y="334">This is only a visible two-dimensional slice of the four-dimensional lattice.</text>')
    write_svg("parity-slice.svg", "\n".join(parts))


def running_membership() -> None:
    parts = [title("Running blocks under the D4 parity test")]
    rows = [
        ("(1, -2, 2, 0)", "sum = 1", "outside D4", ORANGE, 92),
        ("(1, 0, -2, 3)", "sum = 2", "inside D4", GREEN, 190),
    ]
    for vector, total, status, color, y in rows:
        parts.append(f'<rect x="72" y="{y}" width="250" height="58" rx="6" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
        parts.append(f'<text class="label" x="94" y="{y + 35}">{vector}</text>')
        parts.append(f'<line x1="338" y1="{y + 29}" x2="442" y2="{y + 29}" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
        parts.append(f'<rect x="462" y="{y}" width="96" height="58" rx="6" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="510" y="{y + 35}">{total}</text>')
        parts.append(f'<rect x="586" y="{y}" width="112" height="58" rx="6" fill="{color}" opacity="0.16" stroke="{color}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="642" y="{y + 35}">{status}</text>')
    parts.append('<text class="small" x="72" y="304">D4 membership is determined by parity of the coordinate sum.</text>')
    write_svg("running-membership.svg", "\n".join(parts))


def generator_basis() -> None:
    parts = [title("D4 generator basis")]
    headers = ["g1", "g2", "g3", "g4"]
    vectors = ["(1, -1, 0, 0)", "(0, 1, -1, 0)", "(0, 0, 1, -1)", "(0, 0, 1, 1)"]
    for index, (header, vector) in enumerate(zip(headers, vectors)):
        x = 72 + index * 165
        parts.append(f'<rect x="{x}" y="92" width="140" height="96" rx="6" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
        parts.append(f'<text class="title" text-anchor="middle" x="{x + 70}" y="126">{header}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + 70}" y="158">{vector}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + 70}" y="178">even sum</text>')
    parts.append('<text class="small" x="74" y="260">The columns of G are these basis vectors. Integer combinations generate D4.</text>')
    write_svg("generator-basis.svg", "\n".join(parts))


def even_parity_patterns() -> None:
    parts = [title("Even parity signatures in four dimensions")]
    cell_w = 86
    cell_h = 42
    start_x = 78
    start_y = 72
    for value in range(16):
        bits = tuple((value >> shift) & 1 for shift in (3, 2, 1, 0))
        even = sum(bits) % 2 == 0
        row = value // 4
        col = value % 4
        x = start_x + col * 150
        y = start_y + row * 56
        color = GREEN if even else GRAY
        opacity = "0.18" if even else "0.08"
        parts.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="6" fill="{color}" opacity="{opacity}" stroke="{color}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + cell_w / 2}" y="{y + 27}">{"".join(str(bit) for bit in bits)}</text>')
    parts.append(f'<rect x="568" y="294" width="16" height="16" fill="{GREEN}" opacity="0.18" stroke="{GREEN}" />')
    parts.append('<text class="small" x="592" y="307">kept by D4</text>')
    parts.append(f'<rect x="568" y="318" width="16" height="16" fill="{GRAY}" opacity="0.08" stroke="{GRAY}" />')
    parts.append('<text class="small" x="592" y="331">outside D4</text>')
    write_svg("even-parity-patterns.svg", "\n".join(parts))


def cosets_2z4() -> None:
    parts = [title("D4 as eight shifted copies of 2Z^4")]
    patterns = [
        "0000",
        "1100",
        "1010",
        "1001",
        "0110",
        "0101",
        "0011",
        "1111",
    ]
    for index, pattern in enumerate(patterns):
        col = index % 4
        row = index // 4
        x = 76 + col * 165
        y = 96 + row * 88
        parts.append(f'<rect x="{x}" y="{y}" width="132" height="58" rx="6" fill="{BLUE}" opacity="0.13" stroke="{BLUE}" stroke-width="2" />')
        parts.append(f'<text class="title" text-anchor="middle" x="{x + 66}" y="{y + 37}">{pattern}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + 66}" y="{y + 78}">{pattern} + 2Z^4</text>')
    parts.append('<text class="small" x="78" y="304">Each even signature is one coset of the all-even grid 2Z^4 inside D4.</text>')
    write_svg("cosets-2z4.svg", "\n".join(parts))


def main() -> None:
    parity_slice()
    running_membership()
    generator_basis()
    even_parity_patterns()
    cosets_2z4()


if __name__ == "__main__":
    main()

