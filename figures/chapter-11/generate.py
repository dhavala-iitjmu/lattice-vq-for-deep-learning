"""Generate Chapter 11 SVG figures using only the Python standard library."""

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
  </style>
{body}
</svg>
"""
    (OUT / name).write_text(svg)


def title(text: str) -> str:
    return f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />\n<text class="title" x="48" y="32">{text}</text>'


def box(parts: list[str], x: int, y: int, w: int, h: int, label: str, color: str = GRID) -> None:
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#f8f9f9" stroke="{color}" stroke-width="2" />')
    parts.append(f'<text class="label" text-anchor="middle" x="{x + w / 2}" y="{y + h / 2 + 5}">{label}</text>')


def dequantize_then_dot() -> None:
    parts = [title("Baseline: dequantize weights, then dot")]
    labels = [("HNLQ indices", 60), ("decode weights", 220), ("reconstructed w", 380), ("dot with x", 540)]
    for label, x in labels:
        box(parts, x, 132, 124, 56, label)
    for x1, x2 in [(184, 220), (344, 380), (504, 540)]:
        parts.append(f'<line x1="{x1}" y1="160" x2="{x2}" y2="160" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append(f'<rect x="368" y="220" width="148" height="42" rx="7" fill="{ORANGE}" opacity="0.14" stroke="{ORANGE}" />')
    parts.append('<text class="small" text-anchor="middle" x="442" y="246">temporary weight buffer</text>')
    parts.append('<text class="small" x="64" y="334">The one-sided LUT path removes the reconstructed-weight buffer.</text>')
    write_svg("dequantize-then-dot.svg", "\n".join(parts))


def lut_construction() -> None:
    parts = [title("Build T_x(b) from one activation block")]
    box(parts, 70, 126, 126, 60, "activation x", BLUE)
    box(parts, 258, 92, 128, 48, "codeword c0", GREEN)
    box(parts, 258, 154, 128, 48, "codeword c1", GREEN)
    box(parts, 258, 216, 128, 48, "... c15", GREEN)
    box(parts, 486, 140, 150, 72, "T_x table", ORANGE)
    for y in [116, 178, 240]:
        parts.append(f'<line x1="196" y1="156" x2="258" y2="{y}" stroke="{DARK}" stroke-width="2" marker-end="url(#arrow)" />')
        parts.append(f'<line x1="386" y1="{y}" x2="486" y2="176" stroke="{DARK}" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append('<text class="small" x="64" y="334">Each table entry is one activation-codeword dot product.</text>')
    write_svg("lut-construction.svg", "\n".join(parts))


def lookup_accumulation() -> None:
    parts = [title("Accumulate dot product from indices")]
    for level, x in enumerate([68, 206, 344, 482]):
        box(parts, x, 92, 94, 48, f"b{level}", BLUE)
        box(parts, x, 178, 94, 48, f"T_x[b{level}]", GREEN)
        parts.append(f'<line x1="{x + 47}" y1="140" x2="{x + 47}" y2="178" stroke="{DARK}" stroke-width="2" marker-end="url(#arrow)" />')
    box(parts, 610, 142, 92, 58, "sum", ORANGE)
    for x in [162, 300, 438, 576]:
        parts.append(f'<line x1="{x}" y1="202" x2="610" y2="171" stroke="{DARK}" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append('<text class="small" x="64" y="334">Scale each lookup by 1/q^m and divide the accumulated result by beta.</text>')
    write_svg("lookup-accumulation.svg", "\n".join(parts))


def memory_traffic() -> None:
    parts = [title("Memory path comparison")]
    parts.append(f'<rect x="70" y="96" width="260" height="132" rx="7" fill="{ORANGE}" opacity="0.12" stroke="{ORANGE}" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="200" y="126">reconstruct-then-dot</text>')
    parts.append('<text class="small" text-anchor="middle" x="200" y="158">indices -> weights -> dot</text>')
    parts.append('<text class="small" text-anchor="middle" x="200" y="184">moves reconstructed values</text>')
    parts.append(f'<rect x="430" y="96" width="260" height="132" rx="7" fill="{GREEN}" opacity="0.12" stroke="{GREEN}" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="560" y="126">one-sided LUT</text>')
    parts.append('<text class="small" text-anchor="middle" x="560" y="158">indices -> table entries -> sum</text>')
    parts.append('<text class="small" text-anchor="middle" x="560" y="184">keeps weights compressed</text>')
    parts.append('<text class="small" x="64" y="334">The LUT path helps when the table is reused enough to amortize construction.</text>')
    write_svg("memory-traffic.svg", "\n".join(parts))


def activation_reuse() -> None:
    parts = [title("One activation table reused across rows")]
    box(parts, 70, 130, 120, 60, "activation block", BLUE)
    box(parts, 270, 130, 120, 60, "T_x table", GREEN)
    for row, y in enumerate([74, 130, 186, 242]):
        box(parts, 500, y, 150, 38, f"row {row} HNLQ indices", GRID)
        parts.append(f'<line x1="390" y1="160" x2="500" y2="{y + 19}" stroke="{DARK}" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append(f'<line x1="190" y1="160" x2="270" y2="160" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<text class="small" x="64" y="334">Matrix multiplication creates reuse: many rows can share the table for the same activation tile.</text>')
    write_svg("activation-reuse.svg", "\n".join(parts))


def main() -> None:
    dequantize_then_dot()
    lut_construction()
    lookup_accumulation()
    memory_traffic()
    activation_reuse()


if __name__ == "__main__":
    main()
