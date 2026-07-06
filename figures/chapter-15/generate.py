"""Generate Chapter 15 SVG figures using only the Python standard library."""

from __future__ import annotations

from pathlib import Path


OUT = Path(__file__).resolve().parent
WIDTH = 760
HEIGHT = 360
DARK = "#17202a"
GRID = "#d6dbdf"
BLUE = "#2f6f9f"
GREEN = "#2e8b57"


def write_svg(name: str, title_text: str, labels: list[str]) -> None:
    parts = [f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />']
    parts.append(f'<text class="title" x="48" y="32">{title_text}</text>')
    for i, label in enumerate(labels):
        x = 80 + i * 170
        parts.append(f'<rect x="{x}" y="128" width="130" height="72" rx="8" fill="#f8f9f9" stroke="{GRID}" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 65}" y="168">{label}</text>')
    parts.append('<text class="small" x="64" y="334">Schematic figure for the recursive representation viewpoint.</text>')
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
    write_svg("generator-vs-recursion.svg", "Generator view versus recursive view", ["matrix G", "parity rule", "same D4"])
    write_svg("recursive-tree.svg", "Recursive Barnes-Wall tree", ["small pieces", "combine", "larger lattice"])
    write_svg("hierarchy.svg", "Barnes-Wall hierarchy", ["1D", "2D", "D4", "RE8"])
    write_svg("recursive-decoder.svg", "Recursive decoder overview", ["split", "decode", "enforce", "combine"])


if __name__ == "__main__":
    main()
