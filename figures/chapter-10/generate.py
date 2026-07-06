"""Generate Chapter 10 SVG figures using only the Python standard library."""

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


def hierarchy() -> None:
    parts = [title("Four hierarchy levels reuse one small codebook")]
    for level, x in enumerate([70, 220, 370, 520]):
        parts.append(f'<rect x="{x}" y="96" width="110" height="64" rx="7" fill="#f8f9f9" stroke="{BLUE}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 55}" y="123">level {level}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + 55}" y="145">index b{level}</text>')
        parts.append(f'<line x1="{x + 55}" y1="160" x2="365" y2="226" stroke="{DARK}" stroke-width="2" marker-end="url(#arrow)" />')
    parts.append(f'<rect x="278" y="226" width="174" height="62" rx="7" fill="{GREEN}" opacity="0.16" stroke="{GREEN}" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="365" y="253">shared A2 table</text>')
    parts.append('<text class="small" text-anchor="middle" x="365" y="273">16 representatives</text>')
    parts.append('<text class="small" x="64" y="334">The effective codebook has many index sequences, but each lookup uses the same small table.</text>')
    write_svg("hierarchy.svg", "\n".join(parts))


def residual_flow() -> None:
    parts = [title("Digit extraction: reduce mod q, then divide by q")]
    boxes = [
        (70, 134, "residual r_m"),
        (230, 90, "emit index b_m"),
        (230, 178, "subtract digit"),
        (390, 178, "divide by q"),
        (560, 178, "quotient z_{m+1}"),
    ]
    for x, y, label in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="126" height="50" rx="7" fill="#f8f9f9" stroke="{GRID}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 63}" y="{y + 30}">{label}</text>')
    arrows = [(196, 159, 230, 203), (293, 140, 293, 178), (356, 203, 390, 203), (516, 203, 560, 203)]
    for x1, y1, x2, y2 in arrows:
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    parts.append('<text class="small" x="64" y="334">Each pass peels one base-q digit off the generator coefficients.</text>')
    write_svg("residual-flow.svg", "\n".join(parts))


def radix_expansion() -> None:
    parts = [title("HNLQ as two's-complement digit expansion")]
    terms = [
        ("c~_b0", "1"),
        ("c~_b1", "2"),
        ("c~_b2", "4"),
        ("c~_b3", "-8"),
    ]
    x = 94
    for index, (term, weight) in enumerate(terms):
        parts.append(f'<rect x="{x}" y="126" width="116" height="70" rx="7" fill="#f8f9f9" stroke="{BLUE}" stroke-width="2" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + 58}" y="154">{term}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + 58}" y="178">weight {weight}</text>')
        if index < len(terms) - 1:
            parts.append(f'<text class="title" x="{x + 130}" y="170">+</text>')
        x += 154
    parts.append('<text class="small" x="80" y="254">scaled reconstruction = c~_b0 + 2 c~_b1 + 4 c~_b2 - 8 c~_b3</text>')
    parts.append('<text class="small" x="80" y="334">Divide by beta to return from scaled lattice coordinates to weight units.</text>')
    write_svg("radix-expansion.svg", "\n".join(parts))


def overload_propagation() -> None:
    parts = [title("Overload is a coefficient outside the digit range")]
    values = [10, 10, 17, 8]
    chart_x = 120
    chart_y = 286
    chart_h = 204
    max_value = 18.0
    bar_w = 80
    gap = 60
    parts.append(f'<line x1="90" y1="{chart_y}" x2="650" y2="{chart_y}" stroke="{DARK}" stroke-width="2" />')
    parts.append(f'<line x1="90" y1="{chart_y - chart_h}" x2="90" y2="{chart_y}" stroke="{DARK}" stroke-width="2" />')
    threshold_y = chart_y - chart_h * 8 / max_value
    parts.append(f'<line x1="90" y1="{threshold_y:.1f}" x2="650" y2="{threshold_y:.1f}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 5" />')
    parts.append(f'<text class="small" x="655" y="{threshold_y + 4:.1f}">threshold</text>')
    for index, value in enumerate(values):
        h = chart_h * value / max_value
        x = chart_x + index * (bar_w + gap)
        y = chart_y - h
        color = GREEN if value <= 2 else ORANGE
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" fill="{color}" opacity="0.86" />')
        parts.append(f'<text class="label" text-anchor="middle" x="{x + bar_w / 2}" y="{chart_y + 25}">level {index}</text>')
        parts.append(f'<text class="small" text-anchor="middle" x="{x + bar_w / 2}" y="{y - 8:.1f}">{value:.2f}</text>')
    parts.append('<text class="small" x="64" y="334">Bars show max absolute residual after each level for the overloaded second block.</text>')
    write_svg("overload-propagation.svg", "\n".join(parts))


def codebook_reuse() -> None:
    parts = [title("Small tables replace one materialized huge table")]
    parts.append(f'<rect x="76" y="104" width="214" height="126" rx="7" fill="{ORANGE}" opacity="0.12" stroke="{ORANGE}" stroke-width="2" />')
    parts.append('<text class="label" text-anchor="middle" x="183" y="146">flat effective table</text>')
    parts.append('<text class="small" text-anchor="middle" x="183" y="170">65,536 entries</text>')
    parts.append('<text class="small" text-anchor="middle" x="183" y="194">large LUTs</text>')
    parts.append(f'<line x1="316" y1="166" x2="438" y2="166" stroke="{DARK}" stroke-width="3" marker-end="url(#arrow)" />')
    for index, y in enumerate([80, 132, 184, 236]):
        parts.append(f'<rect x="464" y="{y}" width="170" height="36" rx="6" fill="#f8f9f9" stroke="{GREEN}" stroke-width="2" />')
        parts.append(f'<text class="small" text-anchor="middle" x="549" y="{y + 23}">level {index}: 16 entries</text>')
    parts.append('<text class="small" x="64" y="334">Chapter 11 uses the small per-level table to build one-sided dot-product lookup tables.</text>')
    write_svg("codebook-reuse.svg", "\n".join(parts))


def main() -> None:
    hierarchy()
    residual_flow()
    radix_expansion()
    overload_propagation()
    codebook_reuse()


if __name__ == "__main__":
    main()
