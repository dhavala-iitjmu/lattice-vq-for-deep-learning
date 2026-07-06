# Lattice Vector Quantization for Neural Networks

This repository contains the Quarto source for an online book on lattice vector quantization for neural-network inference.

Version: `0.1`

Repository: <https://github.com/dhavala-iitjmu/lattice-vq-for-deep-learning>

## License

The book manuscript, figures, and documentation are licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (`CC BY-NC 4.0`).

Reference code in `code/`, `figures/`, and `tests/` is provided for educational and research use under the same non-commercial terms unless a separate license is added later.

## Local Preview

```bash
quarto preview
```

## Render

```bash
quarto render
```

The rendered site is written to `_site/`.

## Publish

The repository includes a GitHub Actions workflow at `.github/workflows/publish.yml`.

After pushing this repository to GitHub:

1. Open the repository settings on GitHub.
2. Go to **Pages**.
3. Set **Build and deployment** to **GitHub Actions**.
4. Push to `main` or run the workflow manually.

The workflow renders the Quarto book and publishes `_site/` to GitHub Pages.

## Project Structure

- `BOOK_SPEC.md` - book vision, standards, and chapter specifications.
- `_quarto.yml` - Quarto book configuration.
- `index.qmd` - book preface and landing page.
- `chapters/` - book chapters.
- `appendices/` - appendices, including exercise solutions.
- `notation.qmd` - shared notation table.
- `references.bib` - bibliography.
- `figures/` - reproducible figure assets.
- `code/` - reference implementations and optimized examples.
- `tests/` - tests for executable numerical examples.
