"""Generate Chapter 9 SVG figures using only the Python standard library."""

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
COLORS = ["#2f6f9f", "#d9822b", "#2e8b57", "#8e44ad"]


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


def integer_cosets() -> None:
    parts = [title("Modulo 4 turns infinitely many integers into four classes")]
    y = 178
    start_x = 78
    spacing = 42
    parts.append(f'<line class="axis" x1="52" y1="{y}" x2="708" y2="{y}" />')
    for offset, value in enumerate(range(-7, 8)):
        x = start_x + offset * spacing
        color = COLORS[value % 4]
        parts.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{color}" />')
        parts.append(f'<text class="small" text-anchor="middle" x="{x}" y="{y + 32}">{value}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x}" y="{y - 18}">{value % 4}</text>')
    parts.append('<text class="small" x="62" y="82">Numbers with the same color differ by a multiple of 4.</text>')
    parts.append('<text class="small" x="62" y="334">A residue class is infinite, but its representative index is finite.</text>')
    write_svg("integer-cosets.svg", "\n".join(parts))


def vector_cosets() -> None:
    parts = [title("Z^2 / 2Z^2 has four parity classes")]
    origin = (380, 190)
    scale = 38
    for value in range(-4, 5):
        x = origin[0] + value * scale
        y = origin[1] - value * scale
        parts.append(f'<line class="grid" x1="{x}" y1="64" x2="{x}" y2="310" />')
        parts.append(f'<line class="grid" x1="216" y1="{y}" x2="544" y2="{y}" />')
    for a in range(-4, 5):
        for b in range(-3, 4):
            color = COLORS[(a % 2) * 2 + (b % 2)]
            x = origin[0] + a * scale
            y = origin[1] - b * scale
            parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{color}" />')
    parts.append('<text class="small" x="64" y="334">Two parity bits index the four repeating vector classes.</text>')
    write_svg("vector-cosets.svg", "\n".join(parts))


def boundary_tie_breaking() -> None:
    parts = [title("Boundary points need a deterministic owner")]
    left = (244, 178)
    right = (500, 178)
    parts.append(f'<rect x="108" y="92" width="256" height="172" fill="{BLUE}" opacity="0.10" stroke="{BLUE}" stroke-width="3" />')
    parts.append(f'<rect x="364" y="92" width="256" height="172" fill="{GREEN}" opacity="0.10" stroke="{GREEN}" stroke-width="3" />')
    parts.append(f'<line x1="364" y1="92" x2="364" y2="264" stroke="{DARK}" stroke-width="2" stroke-dasharray="7 5" />')
    parts.append(f'<circle cx="{left[0]}" cy="{left[1]}" r="8" fill="{BLUE}" />')
    parts.append(f'<circle cx="{right[0]}" cy="{right[1]}" r="8" fill="{GREEN}" />')
    parts.append(f'<circle cx="364" cy="{left[1]}" r="9" fill="{ORANGE}" />')
    parts.append(f'<line x1="364" y1="{left[1] - 18}" x2="244" y2="{left[1] - 18}" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<text class="label" text-anchor="middle" x="364" y="76">boundary point</text>')
    parts.append('<text class="small" text-anchor="middle" x="304" y="144">fixed rule assigns it left</text>')
    parts.append('<text class="small" x="68" y="334">The rule prevents double-counting representatives in A_q.</text>')
    write_svg("boundary-tie-breaking.svg", "\n".join(parts))


def d4_representatives() -> None:
    parts = [title("D4 / 2D4: sixteen indexed representatives")]
    entries = [
        (0, "0000", "(0,0,0,0)"),
        (1, "0001", "(0,0,1,1)"),
        (2, "0010", "(0,0,1,-1)"),
        (3, "0011", "(2,0,0,0)"),
        (4, "0100", "(0,1,-1,0)"),
        (5, "0101", "(0,1,0,1)"),
        (6, "0110", "(0,1,0,-1)"),
        (7, "0111", "(0,1,1,0)"),
        (8, "1000", "(1,-1,0,0)"),
        (9, "1001", "(1,1,1,-1)"),
        (10, "1010", "(1,1,1,1)"),
        (11, "1011", "(1,1,0,0)"),
        (12, "1100", "(1,0,-1,0)"),
        (13, "1101", "(1,0,0,1)"),
        (14, "1110", "(1,0,0,-1)"),
        (15, "1111", "(1,0,1,0)"),
    ]
    col_w = 166
    row_h = 34
    for idx, bits, rep in entries:
        col = idx // 8
        row = idx % 8
        x = 70 + col * 334
        y = 68 + row * row_h
        parts.append(f'<rect x="{x}" y="{y}" width="{col_w + 126}" height="26" rx="4" fill="#f8f9f9" stroke="{GRID}" />')
        parts.append(f'<text class="small" x="{x + 10}" y="{y + 18}">{idx:2d}</text>')
        parts.append(f'<text class="small" x="{x + 48}" y="{y + 18}">{bits}</text>')
        parts.append(f'<text class="small" x="{x + 110}" y="{y + 18}">{rep}</text>')
    parts.append('<text class="small" x="68" y="334">The index is the generator-coordinate bit pattern read as a binary integer.</text>')
    write_svg("d4-representatives.svg", "\n".join(parts))


def offline_enumeration() -> None:
    parts = [title("Offline codebook generation")]
    boxes = [
        (58, 132, "enumerate D4"),
        (206, 132, "apply 2V rule"),
        (354, 132, "compute bits"),
        (502, 132, "sort indices"),
        (600, 224, "store A2"),
    ]
    for x, y, label in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="118" height="54" rx="7" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 59}" y="{y + 32}">{label}</text>')
    for x1, y1, x2, y2 in [(176, 159, 206, 159), (324, 159, 354, 159), (472, 159, 502, 159), (561, 186, 630, 224)]:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append(f'<rect x="68" y="246" width="446" height="42" rx="7" fill="{PURPLE}" opacity="0.12" stroke="{PURPLE}" />')
    parts.append('<text class="small" text-anchor="middle" x="291" y="272">verify exactly one representative for each index 0 through 15</text>')
    parts.append('<text class="small" x="68" y="334">The online path uses only the stored table and index arithmetic.</text>')
    write_svg("offline-enumeration.svg", "\n".join(parts))


def main() -> None:
    integer_cosets()
    vector_cosets()
    boundary_tie_breaking()
    d4_representatives()
    offline_enumeration()


if __name__ == "__main__":
    main()
