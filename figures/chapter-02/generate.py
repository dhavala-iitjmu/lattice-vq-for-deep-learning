"""Generate Chapter 2 SVG figures using only the Python standard library."""

from __future__ import annotations

import math
from pathlib import Path


OUT = Path(__file__).resolve().parent
WIDTH = 760
HEIGHT = 360
COLORS = {
    0: "#2f6f9f",
    1: "#d9822b",
    2: "#2e8b57",
    3: "#8e44ad",
}


def write_svg(name: str, body: str) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #17202a; }}
    .title {{ font-size: 20px; font-weight: 700; }}
    .label {{ font-size: 13px; }}
    .small {{ font-size: 12px; fill: #566573; }}
    .axis {{ stroke: #5d6d7e; stroke-width: 1.5; }}
    .grid {{ stroke: #d6dbdf; stroke-width: 1; }}
  </style>
{body}
</svg>
"""
    (OUT / name).write_text(svg)


def title(text: str) -> str:
    return f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />\n<text class="title" x="48" y="32">{text}</text>'


def number_to_x(value: int, start: int = -8, stop: int = 17) -> float:
    return 58 + (value - start) * (644 / (stop - start))


def integer_number_line() -> None:
    y = 178
    parts = [title("Integer number line")]
    parts.append(f'<line class="axis" x1="48" y1="{y}" x2="720" y2="{y}" />')
    for value in range(-8, 18):
        x = number_to_x(value)
        length = 18 if value % 4 == 0 else 10
        parts.append(f'<line class="axis" x1="{x:.1f}" y1="{y - length / 2:.1f}" x2="{x:.1f}" y2="{y + length / 2:.1f}" />')
        if value % 2 == 0:
            parts.append(f'<text class="small" text-anchor="middle" x="{x:.1f}" y="{y + 34}">{value}</text>')
    for value, label_y in ((-7, 112), (17, 112)):
        x = number_to_x(value)
        parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="11" fill="#d9822b" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x:.1f}" y="{label_y}">{value}</text>')
        parts.append(f'<line stroke="#d9822b" stroke-width="2" x1="{x:.1f}" y1="{label_y + 8}" x2="{x:.1f}" y2="{y - 15}" />')
    parts.append('<text class="small" x="48" y="300">Both highlighted integers have remainder 1 modulo 4.</text>')
    write_svg("integer-number-line.svg", "\n".join(parts))


def modulo_classes() -> None:
    y = 178
    parts = [title("Modulo-4 classes on the number line")]
    parts.append(f'<line class="axis" x1="48" y1="{y}" x2="720" y2="{y}" />')
    for value in range(-8, 18):
        x = number_to_x(value)
        label = value % 4
        parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="9" fill="{COLORS[label]}" />')
        if value % 4 == 1:
            parts.append(f'<text class="small" text-anchor="middle" x="{x:.1f}" y="{y - 20}">{value}</text>')
    for label in range(4):
        x = 82 + label * 150
        parts.append(f'<circle cx="{x}" cy="292" r="8" fill="{COLORS[label]}" />')
        parts.append(f'<text class="small" x="{x + 16}" y="296">remainder {label}</text>')
    write_svg("modulo-classes.svg", "\n".join(parts))


def modulo_clock() -> None:
    cx = WIDTH / 2
    cy = 178
    radius = 98
    parts = [title("Modulo-4 clock")]
    points = []
    for label, angle in zip((0, 1, 2, 3), (-90, 0, 90, 180)):
        radians = math.radians(angle)
        x = cx + radius * math.cos(radians)
        y = cy + radius * math.sin(radians)
        points.append((label, x, y))
    for _, x1, y1 in points:
        for _, x2, y2 in points:
            if abs(x1 - x2) + abs(y1 - y2) < 1:
                continue
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#d6dbdf" stroke-width="3" />')
    for label, x, y in points:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="24" fill="{COLORS[label]}" />')
        parts.append(f'<text class="title" text-anchor="middle" x="{x:.1f}" y="{y + 7:.1f}" fill="#ffffff">{label}</text>')
    parts.append('<path d="M 384 78 A 100 100 0 0 1 484 178" fill="none" stroke="#17202a" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append('<path d="M 484 178 A 100 100 0 0 1 384 278" fill="none" stroke="#17202a" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append('<path d="M 384 278 A 100 100 0 0 1 284 178" fill="none" stroke="#17202a" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append('<path d="M 284 178 A 100 100 0 0 1 384 78" fill="none" stroke="#17202a" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append('<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#17202a" /></marker></defs>')
    parts.append('<text class="small" text-anchor="middle" x="380" y="326">Counting wraps after 3: 0, 1, 2, 3, 0, ...</text>')
    write_svg("modulo-clock.svg", "\n".join(parts))


def grid_xy(value: int, origin: float, step: float, invert: bool = False) -> float:
    return origin + (-value if invert else value) * step


def integer_grid() -> None:
    origin_x = 380
    origin_y = 180
    step = 36
    parts = [title("Integer grid Z^2")]
    for value in range(-4, 5):
        x = grid_xy(value, origin_x, step)
        y = grid_xy(value, origin_y, step, invert=True)
        parts.append(f'<line class="grid" x1="{x}" y1="54" x2="{x}" y2="306" />')
        parts.append(f'<line class="grid" x1="254" y1="{y}" x2="506" y2="{y}" />')
    parts.append(f'<line class="axis" x1="254" y1="{origin_y}" x2="506" y2="{origin_y}" />')
    parts.append(f'<line class="axis" x1="{origin_x}" y1="54" x2="{origin_x}" y2="306" />')
    for a in range(-3, 4):
        for b in range(-3, 4):
            x = grid_xy(a, origin_x, step)
            y = grid_xy(b, origin_y, step, invert=True)
            parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#17202a" />')
    parts.append('<text class="small" x="520" y="184">Each dot is one integer vector.</text>')
    write_svg("integer-grid.svg", "\n".join(parts))


def cosets_z2() -> None:
    origin_x = 380
    origin_y = 180
    step = 36
    parts = [title("Four cosets of 2Z^2 inside Z^2")]
    for value in range(-4, 5):
        x = grid_xy(value, origin_x, step)
        y = grid_xy(value, origin_y, step, invert=True)
        parts.append(f'<line class="grid" x1="{x}" y1="54" x2="{x}" y2="306" />')
        parts.append(f'<line class="grid" x1="254" y1="{y}" x2="506" y2="{y}" />')
    for a in range(-3, 4):
        for b in range(-3, 4):
            label = (a % 2) + 2 * (b % 2)
            x = grid_xy(a, origin_x, step)
            y = grid_xy(b, origin_y, step, invert=True)
            parts.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{COLORS[label]}" />')
    legend = [("(0, 0)", 0), ("(1, 0)", 1), ("(0, 1)", 2), ("(1, 1)", 3)]
    for idx, (text, label) in enumerate(legend):
        y = 96 + idx * 28
        parts.append(f'<circle cx="560" cy="{y}" r="8" fill="{COLORS[label]}" />')
        parts.append(f'<text class="small" x="578" y="{y + 4}">{text}</text>')
    parts.append('<text class="small" x="536" y="236">Color = vector mod 2</text>')
    write_svg("cosets-z2.svg", "\n".join(parts))


def main() -> None:
    integer_number_line()
    modulo_classes()
    modulo_clock()
    integer_grid()
    cosets_z2()


if __name__ == "__main__":
    main()

