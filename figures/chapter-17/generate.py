"""Generate Chapter 17 SVG figures using only the Python standard library."""

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
        x = 84 + i * 155
        parts.append(f'<rect x="{x}" y="126" width="124" height="76" rx="8" fill="#f8f9f9" stroke="{GRID}" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 62}" y="168">{label}</text>')
    parts.append('<text class="small" x="64" y="334">Bit-plane schematics use the running four-coordinate D4 point.</text>')
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
    write_svg("binary-expansion.svg", "Four-bit two's-complement coordinates", ["1=0001", "0=0000", "-2=1110", "3=0011"])
    write_svg("bit-planes.svg", "Bit planes across coordinates", ["plane 0", "plane 1", "plane 2", "plane 3"])
    write_svg("lsb-constraint.svg", "D4 constrains the LSB plane", ["LSB", "even parity", "RM codeword"])
    write_svg("recursive-planes.svg", "Recursive codes constrain multiple planes", ["low bits", "next bits", "constraints"])
    write_svg("compression.svg", "Constrained planes reduce valid patterns", ["16 patterns", "8 valid", "3 bits"])


if __name__ == "__main__":
    main()
