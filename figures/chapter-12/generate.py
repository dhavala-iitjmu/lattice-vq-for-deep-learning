"""Generate Chapter 12 SVG figures using only the Python standard library."""

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


def dot_to_gemm() -> None:
    parts = [title("From one dot product to many rows")]
    parts.append(f'<rect x="74" y="122" width="118" height="76" rx="7" fill="{BLUE}" opacity="0.14" stroke="{BLUE}" />')
    parts.append('<text class="label" text-anchor="middle" x="133" y="164">activation x</text>')
    for row in range(5):
        y = 74 + row * 48
        parts.append(f'<rect x="306" y="{y}" width="202" height="34" rx="5" fill="#f8f9f9" stroke="{GRID}" />')
        parts.append(f'<text class="small" text-anchor="middle" x="407" y="{y + 22}">HNLQ row {row}</text>')
        parts.append(f'<line x1="192" y1="160" x2="306" y2="{y + 17}" stroke="{DARK}" stroke-width="2" marker-end="url(#arrow)" />')
        parts.append(f'<line x1="508" y1="{y + 17}" x2="612" y2="{y + 17}" stroke="{DARK}" stroke-width="2" marker-end="url(#arrow)" />')
        parts.append(f'<text class="small" x="626" y="{y + 21}">y{row}</text>')
    parts.append('<text class="small" x="64" y="334">The same activation tables serve many compressed rows.</text>')
    write_svg("dot-to-gemm.svg", "\n".join(parts))


def tiling() -> None:
    parts = [title("8 x 8 matrix tiled into D4 blocks")]
    x0, y0 = 100, 72
    cell_w, cell_h = 52, 26
    for r in range(8):
        for c in range(8):
            color = BLUE if c < 4 else GREEN
            parts.append(f'<rect x="{x0 + c * cell_w}" y="{y0 + r * cell_h}" width="{cell_w - 3}" height="{cell_h - 3}" fill="{color}" opacity="0.16" stroke="{GRID}" />')
    parts.append('<text class="label" x="138" y="306">block position 0 uses T_x1</text>')
    parts.append('<text class="label" x="382" y="306">block position 1 uses T_x2</text>')
    parts.append('<text class="small" x="64" y="334">Every row has two encoded D4 blocks, aligned with two activation blocks.</text>')
    write_svg("tiling.svg", "\n".join(parts))


def cache_locality() -> None:
    parts = [title("Keep lookup tables hot, stream indices")]
    parts.append(f'<rect x="78" y="82" width="604" height="58" rx="7" fill="{ORANGE}" opacity="0.12" stroke="{ORANGE}" />')
    parts.append('<text class="label" text-anchor="middle" x="380" y="117">main memory: compressed HNLQ index stream</text>')
    parts.append(f'<rect x="150" y="186" width="460" height="58" rx="7" fill="{GREEN}" opacity="0.14" stroke="{GREEN}" />')
    parts.append('<text class="label" text-anchor="middle" x="380" y="221">cache / shared memory: T_x tables</text>')
    parts.append(f'<line x1="380" y1="140" x2="380" y2="186" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<text class="small" x="64" y="334">Performance depends on whether table reuse beats lookup and indexing overhead.</text>')
    write_svg("cache-locality.svg", "\n".join(parts))


def gpu_tile() -> None:
    parts = [title("GPU tile sketch")]
    parts.append(f'<rect x="82" y="76" width="596" height="220" rx="8" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
    parts.append(f'<rect x="124" y="112" width="196" height="62" rx="7" fill="{BLUE}" opacity="0.14" stroke="{BLUE}" />')
    parts.append('<text class="label" text-anchor="middle" x="222" y="148">build T_x in shared memory</text>')
    for row in range(4):
        y = 98 + row * 44
        parts.append(f'<rect x="420" y="{y}" width="190" height="30" rx="5" fill="{GREEN}" opacity="0.14" stroke="{GREEN}" />')
        parts.append(f'<text class="small" text-anchor="middle" x="515" y="{y + 20}">compressed row tile {row}</text>')
    parts.append(f'<line x1="320" y1="143" x2="420" y2="162" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<text class="small" x="64" y="334">A thread block can reuse activation tables across many row outputs.</text>')
    write_svg("gpu-tile.svg", "\n".join(parts))


def pipeline() -> None:
    parts = [title("End-to-end HNLQ matmul pipeline")]
    labels = ["tile x", "build LUTs", "stream indices", "lookup accumulate", "write y"]
    for i, label in enumerate(labels):
        x = 54 + i * 140
        parts.append(f'<rect x="{x}" y="138" width="112" height="54" rx="7" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 56}" y="170">{label}</text>')
        if i < len(labels) - 1:
            parts.append(f'<line x1="{x + 112}" y1="165" x2="{x + 140}" y2="165" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<text class="small" x="64" y="334">The tile loop is where one-sided LUTs become a matrix multiplication kernel.</text>')
    write_svg("pipeline.svg", "\n".join(parts))


def main() -> None:
    dot_to_gemm()
    tiling()
    cache_locality()
    gpu_tile()
    pipeline()


if __name__ == "__main__":
    main()
