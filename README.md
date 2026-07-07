# Lattice Vector Quantization for Neural Networks

*From First Principles to Efficient Inference*

This repository contains the Quarto source for an online book on lattice vector quantization for neural-network inference.

- Version: `0.1`
- Live book: <https://dhavala-iitjmu.github.io/lattice-vq-for-deep-learning/>
- Repository: <https://github.com/dhavala-iitjmu/lattice-vq-for-deep-learning>

## About the Book

This book develops lattice vector quantization for machine learning from first principles. It is written for machine-learning researchers, LLM quantization researchers, systems researchers, graduate students, and engineers who want to understand both the mathematics and the implementation path to efficient inference.

The central question is: how can structured lattices give neural-network quantizers the representational power of vector quantization while keeping inference practical?

The book starts from the basic pressure that motivates quantization: large neural networks are often limited by memory movement, not only arithmetic. It then builds the required mathematics only when the engineering problem demands it:

- scalar quantization leads to dot-product error;
- dot-product error motivates vector quantization;
- vector quantization exposes codebook storage and search costs;
- codebook structure leads to lattices;
- finite-rate lattice coding leads to quotient groups;
- large effective codebooks lead to Hierarchical Nested Lattice Quantization (HNLQ);
- efficient inference leads to one-sided lookup tables and tiled matrix multiplication;
- recursive lattices lead to Reed-Muller codes, bit planes, and future binary-domain computation.

## Pedagogy

The book follows one rule: never introduce mathematics before the reader needs it.

Instead of presenting lattices, quotient groups, Barnes-Wall lattices, or Reed-Muller codes as abstract topics, the manuscript derives them from increasingly concrete quantization problems. Each chapter follows the pattern:

1. engineering problem,
2. failed simple solution,
3. observation,
4. generalization,
5. definition,
6. worked example,
7. algorithm,
8. implementation and systems tradeoffs.

The running example stays fixed through the core of the book: dimension `d = 4`, the `D4` lattice, radix `q = 2`, depth `M = 4`, an eight-value weight vector, and an eight-value activation vector. The same small example is revisited as a scalar quantizer, a vector quantizer, a lattice point, a quotient codebook, an HNLQ representation, a lookup-table inference path, and finally a bit-plane representation.

The intent is that a reader with no background in abstract algebra, coding theory, or lattice theory can still implement HNLQ from scratch and understand why the construction is natural.

## Book Arc

Part I builds the foundations: quantization pressure, modular arithmetic, vector geometry, classical vector quantization, lattices, the `D4` lattice, and nearest-lattice-point decoding.

Part II turns lattices into a practical neural-network quantization method: lattice vector quantization, quotient codebooks, HNLQ, one-sided lookup tables, matrix multiplication, and calibrated evaluation against scalar baselines.

Part III explains the deeper structure behind the method: higher-dimensional lattices such as `E8`, Barnes-Wall recursion, Reed-Muller codes, bit-plane representations, and carefully labeled research directions toward binary-domain computation.

## Status

The version `0.1` manuscript contains Chapters 1-18, executable Python reference implementations, tests for the numerical examples, and reproducible SVG figures.

Chapter 13 currently uses a deterministic small layer and Gaussian study for reproducibility. It does not claim full model-level benchmark results.

## Local Preview

Install Quarto, then run:

```bash
quarto preview
```

## Render

```bash
quarto render
```

The rendered site is written to `_site/`.

## Test Numerical Examples

```bash
for f in tests/test_chapter_*.py; do python3 "$f" || exit 1; done
```

## Publish

The repository publishes through `.github/workflows/publish.yml`.

GitHub Pages must be configured with **Build and deployment** source set to **GitHub Actions**. Do not select `main` branch publishing; branch publishing serves the repository root and will show this README instead of the rendered Quarto book.

After the Pages source is set to GitHub Actions, push to `main` or run the workflow manually. The workflow renders the book and deploys `_site/` to GitHub Pages.

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

## License

The book manuscript, figures, and documentation are licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (`CC BY-NC 4.0`).

Reference code in `code/`, `figures/`, and `tests/` is provided for educational and research use under the same non-commercial terms unless a separate license is added later.
