"""Generate Chapter 16 SVG figures using only the Python standard library."""

from __future__ import annotations

from pathlib import Path


OUT = Path(__file__).resolve().parent
WIDTH = 760
HEIGHT = 360
DARK = "#17202a"
GRID = "#d6dbdf"


def write_svg(name: str, title_text: str, labels: list[str]) -> None:
    parts = [f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />']
    parts.append(f'<text class="title" x="48" y="32">{title_text}</text>')
    for i, label in enumerate(labels):
        x = 82 + i * 160
        parts.append(f'<rect x="{x}" y="128" width="128" height="72" rx="8" fill="#f8f9f9" stroke="{GRID}" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 64}" y="168">{label}</text>')
    parts.append('<text class="small" x="64" y="334">Binary structure appears as low-bit constraints on lattice points.</text>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: {DARK}; }}
    .title {{ font-size: 20px; font-weight: 700; }}
    .label {{ font-size: 13px; }}
    .small {{ font-size: 12px; fill: #566573; }}
  </style>
{chr(10).join(parts)}
</svg>
"""
    (OUT / name).write_text(svg)


def main() -> None:
    write_svg("binary-cube.svg", "Binary vectors as cube corners", ["000", "011", "101", "111"])
    write_svg("generator-matrix.svg", "Generate codewords by XORing rows", ["select rows", "xor", "codeword"])
    write_svg("parity-code.svg", "Even parity keeps half the signatures", ["all bits", "even parity", "D4 low bits"])
    write_svg("code-tree.svg", "Codes inside recursive lattices", ["RM code", "constraint", "lattice level"])


if __name__ == "__main__":
    main()
