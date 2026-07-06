"""Generate Chapter 14 SVG figures using only the Python standard library."""

from __future__ import annotations

from pathlib import Path


OUT = Path(__file__).resolve().parent
WIDTH = 760
HEIGHT = 360
BLUE = "#2f6f9f"
ORANGE = "#d9822b"
GREEN = "#2e8b57"
DARK = "#17202a"
GRID = "#d6dbdf"


def write_svg(name: str, body: str) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: {DARK}; }}
    .title {{ font-size: 20px; font-weight: 700; }}
    .label {{ font-size: 13px; }}
    .small {{ font-size: 12px; fill: #566573; }}
  </style>
{body}
</svg>
"""
    (OUT / name).write_text(svg)


def title(text: str) -> str:
    return f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />\n<text class="title" x="48" y="32">{text}</text>'


def simple(name: str, heading: str, labels: list[str]) -> None:
    parts = [title(heading)]
    for i, label in enumerate(labels):
        x = 88 + i * 155
        parts.append(f'<rect x="{x}" y="128" width="118" height="76" rx="8" fill="#f8f9f9" stroke="{GRID}" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 59}" y="162">{label}</text>')
    parts.append('<text class="small" x="64" y="334">A qualitative schematic; high-dimensional cells are projected for intuition.</text>')
    write_svg(name, "\n".join(parts))


def main() -> None:
    simple("dn-family.svg", "D_n keeps the even-parity rule", ["D4", "D8", "D_n"])
    simple("e8-union.svg", "E8 as two D8 shells", ["D8", "+ half shift", "E8"])
    simple("e8-decoder.svg", "Nearest E8 decoder", ["decode D8", "decode shifted", "choose closer"])
    simple("comparison.svg", "Running-vector comparison", ["D4 x D4\n0.6416", "E8\n0.6416"])
    simple("packing-density.svg", "More sphere-like cells reduce average error", ["coarser cell", "rounder cell", "tradeoff"])


if __name__ == "__main__":
    main()
