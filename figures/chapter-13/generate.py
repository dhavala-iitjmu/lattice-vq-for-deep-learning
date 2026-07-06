"""Generate Chapter 13 SVG figures using only the Python standard library."""

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


def blocks_to_tensor() -> None:
    parts = [title("From matrix rows to HNLQ blocks")]
    x0, y0 = 122, 78
    for r in range(4):
        for c in range(8):
            color = BLUE if c < 4 else GREEN
            parts.append(f'<rect x="{x0 + c * 58}" y="{y0 + r * 42}" width="54" height="36" fill="{color}" opacity="0.16" stroke="{GRID}" />')
    parts.append('<text class="label" x="170" y="286">block 0</text>')
    parts.append('<text class="label" x="410" y="286">block 1</text>')
    parts.append('<text class="small" x="64" y="334">Each row of the 4 x 8 layer contains two D4 blocks.</text>')
    write_svg("blocks-to-tensor.svg", "\n".join(parts))


def beta_sweep() -> None:
    parts = [title("Beta sweep on the toy layer")]
    betas = [0.5, 1.0, 2.0, 4.0]
    weight = [0.3087, 0.0987, 0.0300, 0.0334]
    output = [5.9559, 0.8513, 0.2610, 0.3494]
    max_y = 6.5
    x0, y0, h = 118, 286, 200
    parts.append(f'<line x1="90" y1="{y0}" x2="670" y2="{y0}" stroke="{DARK}" />')
    parts.append(f'<line x1="90" y1="{y0 - h}" x2="90" y2="{y0}" stroke="{DARK}" />')
    for i, beta in enumerate(betas):
        x = x0 + i * 130
        wh = h * weight[i] / max_y
        oh = h * output[i] / max_y
        parts.append(f'<rect x="{x}" y="{y0 - wh:.1f}" width="42" height="{wh:.1f}" fill="{BLUE}" opacity="0.85" />')
        parts.append(f'<rect x="{x + 46}" y="{y0 - oh:.1f}" width="42" height="{oh:.1f}" fill="{ORANGE}" opacity="0.85" />')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + 44}" y="{y0 + 24}">{beta:.2f}</text>')
    parts.append('<text class="small" x="470" y="86" fill="{BLUE}">blue: weight MSE</text>')
    parts.append('<text class="small" x="470" y="106">orange: output MSE</text>')
    write_svg("beta-sweep.svg", "\n".join(parts))


def output_error() -> None:
    parts = [title("Metric choice changes the selected beta")]
    labels = [("best weight MSE", 0.0300, BLUE), ("best output MSE", 0.2610, ORANGE)]
    for i, (label, value, color) in enumerate(labels):
        x = 150 + i * 270
        h = 170 * (value / 0.3)
        parts.append(f'<rect x="{x}" y="{280 - h:.1f}" width="150" height="{h:.1f}" fill="{color}" opacity="0.82" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 75}" y="310">{label}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + 75}" y="{268 - h:.1f}">{value:.4f}</text>')
    parts.append('<text class="small" x="64" y="334">Weight error and output error answer different engineering questions.</text>')
    write_svg("output-error.svg", "\n".join(parts))


def baseline_comparison() -> None:
    parts = [title("Matched 4-bit comparison")]
    bars = [("HNLQ", 0.2610, ORANGE), ("INT4", 0.0810, GREEN)]
    for i, (label, value, color) in enumerate(bars):
        x = 190 + i * 220
        h = 190 * value / 0.3
        parts.append(f'<rect x="{x}" y="{286 - h:.1f}" width="120" height="{h:.1f}" fill="{color}" opacity="0.85" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 60}" y="312">{label}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + 60}" y="{274 - h:.1f}">{value:.4f}</text>')
    parts.append('<text class="small" x="64" y="334">Weight MSE is near parity; output MSE still favors INT4. Both are reported.</text>')
    write_svg("baseline-comparison.svg", "\n".join(parts))


def pipeline() -> None:
    parts = [title("Calibration and evaluation loop")]
    labels = ["weights", "beta sweep", "quantize", "layer outputs", "baseline report"]
    for i, label in enumerate(labels):
        x = 48 + i * 140
        parts.append(f'<rect x="{x}" y="142" width="112" height="54" rx="7" fill="#f8f9f9" stroke="{GRID}" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 56}" y="174">{label}</text>')
        if i < len(labels) - 1:
            parts.append(f'<line x1="{x + 112}" y1="169" x2="{x + 140}" y2="169" stroke="{DARK}" />')
    parts.append('<text class="small" x="64" y="334">Real model claims require the same loop on real checkpoints and tasks.</text>')
    write_svg("pipeline.svg", "\n".join(parts))




def gaussian_study() -> None:
    parts = [title("Gaussian study: geometry gain vs shaping loss")]
    groups = [
        ("matched density", [("D4", 0.00666, GREEN), ("scalar", 0.00747, GRID)], 0.008),
        ("matched 4 bits/weight", [("HNLQ", 0.01769, ORANGE), ("INT4", 0.00984, GREEN)], 0.02),
    ]
    x0 = 110
    for g, (label, bars, max_y) in enumerate(groups):
        base_x = x0 + g * 310
        for i, (name, value, color) in enumerate(bars):
            x = base_x + i * 120
            h = 180 * value / max_y
            parts.append(f'<rect x="{x}" y="{270 - h:.1f}" width="96" height="{h:.1f}" fill="{color}" opacity="0.85" />')
            parts.append(f'<text class="small" text-anchor="middle" x="{x + 48}" y="{258 - h:.1f}">{value:.4f}</text>')
            parts.append(f'<text class="label" text-anchor="middle" x="{x + 48}" y="294">{name}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{base_x + 108}" y="322">{label}</text>')
    parts.append('<text class="small" x="64" y="348">D4 geometry wins at equal density; the box-shaped digit range gives it back at equal rate.</text>')
    write_svg("gaussian-study.svg", "\n".join(parts))


def main() -> None:
    blocks_to_tensor()
    beta_sweep()
    gaussian_study()
    output_error()
    baseline_comparison()
    pipeline()


if __name__ == "__main__":
    main()
