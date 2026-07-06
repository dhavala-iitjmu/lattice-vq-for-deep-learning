"""Generate Chapter 1 SVG figures using only the Python standard library."""

from __future__ import annotations

from pathlib import Path


WEIGHTS = (0.73, -1.84, 2.11, -0.45, 1.27, 0.08, -2.36, 3.14)
QUANTIZED = (1, -2, 2, 0, 1, 0, -2, 3)
DOTS = {"FP16 dot product": -13.41, "Quantized dot product": -10.50}

OUT = Path(__file__).resolve().parent

WIDTH = 760
HEIGHT = 360
MARGIN_LEFT = 64
MARGIN_RIGHT = 24
MARGIN_TOP = 42
MARGIN_BOTTOM = 58
PLOT_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
PLOT_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
ZERO = MARGIN_TOP + PLOT_HEIGHT * 0.45
SCALE = 58


def svg_document(body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #17202a; }}
    .title {{ font-size: 20px; font-weight: 700; }}
    .axis {{ stroke: #5d6d7e; stroke-width: 1; }}
    .grid {{ stroke: #d6dbdf; stroke-width: 1; }}
    .float {{ fill: #2f6f9f; }}
    .quant {{ fill: #d9822b; }}
    .error {{ fill: #8e44ad; }}
    .label {{ font-size: 13px; }}
    .small {{ font-size: 12px; fill: #566573; }}
  </style>
{body}
</svg>
"""


def y(value: float) -> float:
    return ZERO - value * SCALE


def bar(x_center: float, value: float, width: float, klass: str) -> str:
    y0 = y(max(value, 0))
    h = abs(value) * SCALE
    if value < 0:
        y0 = ZERO
    return f'<rect class="{klass}" x="{x_center - width / 2:.1f}" y="{y0:.1f}" width="{width:.1f}" height="{h:.1f}" rx="3" />'


def axes(title: str) -> str:
    return f"""
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff" />
  <text class="title" x="{MARGIN_LEFT}" y="28">{title}</text>
  <line class="axis" x1="{MARGIN_LEFT}" y1="{ZERO:.1f}" x2="{WIDTH - MARGIN_RIGHT}" y2="{ZERO:.1f}" />
  <line class="axis" x1="{MARGIN_LEFT}" y1="{MARGIN_TOP}" x2="{MARGIN_LEFT}" y2="{HEIGHT - MARGIN_BOTTOM}" />
  <line class="grid" x1="{MARGIN_LEFT}" y1="{y(2):.1f}" x2="{WIDTH - MARGIN_RIGHT}" y2="{y(2):.1f}" />
  <line class="grid" x1="{MARGIN_LEFT}" y1="{y(-2):.1f}" x2="{WIDTH - MARGIN_RIGHT}" y2="{y(-2):.1f}" />
  <text class="small" x="26" y="{y(2) + 4:.1f}">2</text>
  <text class="small" x="21" y="{ZERO + 4:.1f}">0</text>
  <text class="small" x="20" y="{y(-2) + 4:.1f}">-2</text>
"""


def floating_weights() -> None:
    step = PLOT_WIDTH / len(WEIGHTS)
    body = [axes("Floating-point weights")]
    for idx, value in enumerate(WEIGHTS, start=1):
        x_center = MARGIN_LEFT + step * (idx - 0.5)
        body.append(bar(x_center, value, 34, "float"))
        body.append(f'<text class="label" text-anchor="middle" x="{x_center:.1f}" y="{HEIGHT - 28}">{idx}</text>')
        body.append(f'<text class="small" text-anchor="middle" x="{x_center:.1f}" y="{y(value) - 8 if value >= 0 else y(value) + 18:.1f}">{value:.2f}</text>')
    body.append(f'<text class="small" x="{MARGIN_LEFT}" y="{HEIGHT - 8}">Coordinate index</text>')
    (OUT / "floating-point-weights.svg").write_text(svg_document("\n".join(body)))


def quantized_weights() -> None:
    step = PLOT_WIDTH / len(WEIGHTS)
    body = [axes("Scalar quantization moves each coordinate")]
    for idx, (original, quantized) in enumerate(zip(WEIGHTS, QUANTIZED), start=1):
        x_center = MARGIN_LEFT + step * (idx - 0.5)
        body.append(bar(x_center - 11, original, 20, "float"))
        body.append(bar(x_center + 11, quantized, 20, "quant"))
        body.append(f'<text class="label" text-anchor="middle" x="{x_center:.1f}" y="{HEIGHT - 28}">{idx}</text>')
    body.append(f'<rect class="float" x="{WIDTH - 180}" y="24" width="14" height="14" rx="2" />')
    body.append(f'<text class="small" x="{WIDTH - 160}" y="36">FP16 weight</text>')
    body.append(f'<rect class="quant" x="{WIDTH - 180}" y="46" width="14" height="14" rx="2" />')
    body.append(f'<text class="small" x="{WIDTH - 160}" y="58">Rounded weight</text>')
    (OUT / "quantized-weights.svg").write_text(svg_document("\n".join(body)))


def dot_product_error() -> None:
    local_zero = 250
    local_scale = 12

    def local_bar(x_center: float, value: float, klass: str) -> str:
        top = local_zero - abs(value) * local_scale
        return f'<rect class="{klass}" x="{x_center - 48}" y="{top:.1f}" width="96" height="{abs(value) * local_scale:.1f}" rx="4" />'

    body = [
        '<rect x="0" y="0" width="760" height="360" fill="#ffffff" />',
        '<text class="title" x="64" y="28">Dot-product error</text>',
        f'<line class="axis" x1="64" y1="{local_zero}" x2="736" y2="{local_zero}" />',
    ]
    centers = (250, 510)
    for (label, value), x_center, klass in zip(DOTS.items(), centers, ("float", "quant")):
        body.append(local_bar(x_center, value, klass))
        body.append(f'<text class="label" text-anchor="middle" x="{x_center}" y="284">{label}</text>')
        body.append(f'<text class="small" text-anchor="middle" x="{x_center}" y="{local_zero - abs(value) * local_scale - 10:.1f}">{value:.2f}</text>')
    body.append('<path class="error" d="M570 104 L610 104 L610 139 L570 139 Z" opacity="0.22" />')
    body.append('<text class="small" x="616" y="124">error = 2.91</text>')
    (OUT / "dot-product-error.svg").write_text(svg_document("\n".join(body)))


def main() -> None:
    floating_weights()
    quantized_weights()
    dot_product_error()


if __name__ == "__main__":
    main()

