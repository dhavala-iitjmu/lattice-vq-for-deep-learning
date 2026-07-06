# BOOK_SPEC.md

# Lattice Vector Quantization for Neural Networks
## From First Principles to Efficient Inference

Version: 0.1

Author: Soma Dhavala

---

## How This Document Is Organized

This specification has three parts:

- **Spec Part A — Vision and Pedagogy**: what the book is, who it is for, and the standards every chapter must satisfy.
- **Spec Part B — Chapter Specifications**: detailed specifications for Chapters 1–18, grouped by the book's Parts I–III.
- **Spec Part C — Project Standards**: repository layout, references, long-term goals, and success criteria.

Throughout this document, "Part I", "Part II", and "Part III" always refer to parts of the *book*. The parts of this specification are always written "Spec Part A/B/C".

Each standard is specified exactly once. Chapter specifications cross-reference the standards in Spec Part A rather than restating them.

---

# Spec Part A — Vision and Pedagogy

## A1. Vision

This book aims to become the definitive reference on lattice vector quantization for machine learning and neural network inference.

Unlike existing literature, the book assumes **no prior background in lattice theory, coding theory, or abstract algebra**. Instead, every mathematical concept is introduced because it solves a concrete engineering problem arising in neural network quantization.

The philosophy of the book is:

> Never introduce mathematics before the reader needs it.

Rather than presenting lattices, quotient groups, Reed–Muller codes, or Barnes–Wall lattices as abstract mathematical objects, we derive them naturally from increasingly sophisticated quantization problems.

By the end of the book, the reader should not only understand Hierarchical Nested Lattice Quantization (HNLQ), but also understand why it is almost inevitable once one attempts to construct structured vector quantizers.

The final chapters extend beyond existing literature by connecting

- quotient groups,
- lattice codebooks,
- hierarchical nested lattice quantization,
- Barnes–Wall lattices,
- Reed–Muller codes,
- bit-plane representations,

into one unified framework.

**Terminology.** The acronym HNLQ always expands to *Hierarchical Nested Lattice Quantization*. Use the full name at first use in every chapter, then the acronym.

## A2. Target Audience

The primary audience consists of

- machine learning researchers,
- LLM quantization researchers,
- systems researchers,
- graduate students,
- engineers implementing efficient inference.

The only mathematical assumptions are

- high-school algebra,
- basic vectors,
- basic calculus,
- basic programming.

No knowledge is assumed of

- abstract algebra,
- coding theory,
- lattice theory,
- number theory,
- information theory.

These subjects are introduced gradually as needed.

**Scope note.** The book covers theory, algorithms, and systems implementation, and includes one chapter (Chapter 13) on applying HNLQ to a real model — calibration, evaluation, and comparison against scalar-quantization baselines. Full-scale empirical studies across model families are out of scope.

## A3. Learning Philosophy

Every chapter must answer one question. The reader should never encounter a definition before understanding why the definition is necessary.

Instead of

> Definition → Example

we follow

> Engineering Problem → Failed Solution → Observation → Generalization → Definition → Example → Algorithm → Implementation

Every theorem must solve a problem. Every proof should explain intuition before formal mathematics. Every mathematical object should feel "invented" rather than "introduced."

## A4. Pedagogical Principles

**Principle 1 — Never define before motivating.** Every mathematical concept is introduced because it solves an engineering problem.

**Principle 2 — One running example.** Readers should never struggle because every chapter introduces new notation. Instead, one familiar example becomes richer over time (see §A6).

**Principle 3 — Concrete before abstract.** Example first, generalization later. For example: integers → vectors → integer grids → general lattices.

**Principle 4 — Every equation must have intuition.** Formal derivations appear only after geometric or engineering intuition.

**Principle 5 — Every chapter ends with implementation.** Readers should leave every chapter knowing what the mathematics means, how to implement it, its computational complexity, and its engineering tradeoffs.

## A5. Writing Style

The writing style should resemble *Dive into Deep Learning*, the *MLSys Book*, and *Mathematics for Machine Learning* — rather than IEEE papers, journal articles, or lecture notes.

The tone should be conversational but mathematically rigorous. Avoid unnecessary notation. Avoid introducing symbols that are used only once.

## A6. The Running Example

The entire book revolves around one example. Unless otherwise stated, every chapter uses:

| Parameter | Value |
|---|---|
| Vector dimension | `d = 4` |
| Lattice | `D4` |
| Hierarchy radix | `q = 2` |
| Hierarchy depth | `M = 4` |
| Weight vector `w` | 8 values (two `D4` blocks) |
| Activation vector `x` | 8 values |
| Quantization block size | 4 |

These values never change throughout Parts I and II (Chapters 1–12). Chapter 13 scales the same construction to a real model. Part III introduces `E8` using exactly the same workflow: only after the reader completely understands `D4` do we generalize to `Dn` and later `E8`.

Do not introduce new examples unless absolutely necessary.

The example evolves chapter by chapter:

| Chapter | The running example shows |
|---|---|
| 1 | Floating-point weights and dot-product error |
| 2 | Modulo arithmetic |
| 3 | Distances |
| 4 | Vector quantization |
| 5 | Generator matrices |
| 6 | The `D4` lattice |
| 7 | Nearest lattice point |
| 8 | Lattice quantization |
| 9 | Finite codebook |
| 10 | Hierarchy |
| 11 | One-sided LUT |
| 12 | Matrix multiplication |
| 13 | Calibrated, model-scale quantization |
| 14 | Replace `D4` with `E8` |
| 15 | Recursive lattices |
| 16 | Binary codes |
| 17 | Bit planes |
| 18 | Binary computation |

By the end of the book, the reader has seen the same example from every possible viewpoint.

## A7. Notation

Notation must remain absolutely consistent throughout the book. No notation may change between chapters. Never introduce notation that is used only once. Avoid overloaded symbols. Every variable must appear in the notation table below (and in `notation.qmd`, which mirrors it) before it is used in a chapter.

| Symbol | Meaning |
|---|---|
| `x` | Activation vector |
| `w` | Floating-point weight vector |
| `ŵ` | Quantized weight vector |
| `v` | Generic vector being quantized (a weight block or a residual) |
| `C` | Finite codebook (classical vector quantization) |
| `c_b` | Codeword with index `b` in a finite codebook |
| `G` | Generator matrix |
| `L` | Lattice |
| `V` | Voronoi cell of `L` around the origin |
| `Q_L(v)` | Nearest lattice point in `L` to `v` |
| `β` | Scaling factor applied before quantization |
| `A_q` | Finite HNLQ codebook, `A_q = L ∩ qV` |
| `b` | Codebook index |
| `b_m` | Digit index at hierarchy level `m` (a coset index) |
| `z_m` | Coefficient quotient at hierarchy level `m` during digit extraction |
| `\tilde{c}_b` | Digit representative `G \cdot bits(b)`, linear in the index bits |
| `M` | Hierarchy depth |
| `q` | Hierarchy radix |
| `d` | Vector dimension |
| `K` | Number of codewords in a classical codebook |
| `T_x(b)` | One-sided lookup-table entry for activation block `x` and codebook index `b` |

**Conventions.**

- `Q_L(·)` accepts any vector in `R^d`. In this book it is applied to weight blocks and residuals — never to activations, which remain in floating point.
- `L` is reserved for the lattice. The one-sided lookup table is written `T_x(b)`, not `L_x(b)`, to avoid overloading `L`.
- `n` appears only as the dimension subscript of the lattice family `Dn` and in the complexity of its decoder; everywhere else the vector dimension is `d`.

## A8. Mathematical Conventions

One goal of this book is to make advanced mathematical concepts accessible to readers with only a basic undergraduate background. Every chapter must adhere to the following conventions.

### A8.1 Definitions

Definitions should never appear in isolation. Every definition follows the sequence:

> Engineering Problem → Concrete Example → Observation → Generalization → Definition

Bad:

> Definition: A quotient group is ...

Good:

> Suppose we want to compress infinitely many lattice points into exactly 16 codewords. How can infinitely many objects become finite? Observe that integers modulo 4 naturally form four classes. Generalize to vectors. Generalize to lattices. *Now* define quotient groups.

Readers should feel that the definition was inevitable.

### A8.2 Theorems

Every theorem must answer a previously posed question.

- Before every theorem, explicitly state: *"What problem are we solving?"*
- After every theorem, explicitly state: *"What does this mean in practice?"*

### A8.3 Proofs

Every proof has two parts:

- **Part A — Intuition.** Explain geometrically or visually why the statement should be true.
- **Part B — Formal proof.**

Readers should understand the proof before reading the mathematics.

### A8.4 Equations

Every displayed equation must be followed by interpretation the reader can use. For the handful of *load-bearing* equations in a chapter — the ones a reader must internalize — use the full three-lens form:

- a verbal explanation,
- a geometric interpretation,
- an engineering interpretation.

For routine or transitional displays, one well-chosen sentence of interpretation (or none, when the surrounding prose already interprets it) is better than a formulaic triple. The three-lens pattern is a tool, not a liturgy: if any lens would restate the obvious ("multiply and sum"), drop that lens. Aim for at most three or four full triples per chapter.

For example,

> `x̂ = x₀ + 2x₁ + 4x₂ + 8x₃`

should immediately be followed by:

> Interpretation: think of this as writing the decimal number 4387 as 7 + 10·8 + 100·3 + 1000·4. Hierarchical nested lattice quantization is simply the lattice analogue of writing numbers in positional notation.

### A8.5 Generalization Strategy

Every concept should appear in the following order:

> Concrete example → `D4` → `Dn` → `E8` → General lattice

Readers should never encounter an abstract theorem before seeing `D4`.

## A9. Engineering Conventions

Unlike traditional mathematics books, every chapter must answer the following engineering questions:

- Why is this useful?
- How is it implemented?
- What is its computational complexity?
- When is it preferable?
- What are its limitations?
- What hardware benefits does it provide?

### A9.1 Per-Algorithm Requirements

Every algorithm must include:

- input,
- output,
- pseudocode,
- time complexity,
- memory complexity,
- parallelization opportunities,
- GPU implementation notes,
- SIMD implementation notes,
- possible optimizations.

Every algorithm must also discuss memory, latency, parallelism, GPU suitability, SIMD suitability, cache locality, offline preprocessing, and online inference cost. Readers should understand not only *how* but also *when* to use the algorithm.

### A9.2 Complexity Summary

Every algorithm must summarize time complexity, memory complexity, offline preprocessing, and online inference cost. For example:

| Nearest `D4` decoder | |
|---|---|
| Time | `O(n)` |
| Memory | `O(1)` |
| Offline | None |
| GPU suitability | Excellent |

### A9.3 Engineering Insight Section

Every chapter ends with an **Engineering Insight** section — a discussion connecting the chapter's mathematics to practical systems. Examples of topics:

- why HNLQ prefers small `q`,
- memory-bandwidth implications,
- when brute-force search beats algebraic decoding,
- LUT sizes and cache locality,
- Tensor Core implications,
- SIMD and CUDA implementation,
- future hardware directions.

## A10. Figures

The book should contain approximately 80–120 figures; every chapter should introduce approximately five new figures.

Figures should emphasize intuition and understanding rather than decoration or aesthetics. Preferred style: simple, minimal, annotated, consistent colors.

Every figure must answer exactly one question. Bad: one complicated figure. Good: five simple figures.

Each figure should include a title, a caption, an explanation, and a reference in the text. All figures should be reproducible using Python (sources under `figures/`).

Examples of figures used throughout the book: integer number line, modulo classes, integer grids, cosets, quotient groups, Voronoi cells, the `D4` lattice, `E8` lattice projections, nearest lattice point, the HNLQ hierarchy, one-sided lookup tables, matrix multiplication tiling, Barnes–Wall decomposition.

## A11. Algorithms and Code

Every important algorithm appears in four forms:

1. English description
2. Pseudocode
3. Python reference implementation
4. Optimized implementation notes

Readers should always be able to implement the algorithm directly.

Python code should be readable, minimal, and well commented. Avoid unnecessary abstraction. Where appropriate, also provide NumPy, PyTorch, and CUDA pseudocode (under `code/`; see §C1).

## A12. Exercises and Solutions

Every chapter ends with

- conceptual exercises,
- worked numerical exercises,
- programming exercises,
- research questions.

Difficulty should progress from basic → intermediate → advanced → open-ended.

Solutions are provided separately in `appendices/solutions.qmd`, organized by chapter.

Example (Chapter 6):

- Determine whether `(2, 1, 3, 4)` belongs to `D4`.
- Construct `D4` using its generator matrix.
- Implement the nearest-`D4` decoder.
- Compare brute-force search versus the decoder.

## A13. Historical Notes

Every major concept should include historical background, the original paper, the engineering motivation, and how the current chapter differs. This provides context without interrupting the flow.

## A14. Common Mistakes

Every chapter should conclude with a **Common Mistakes** section to prevent misconceptions. Examples:

- confusing a lattice with a codebook,
- confusing scaling with fixed-rate coding,
- confusing generator matrices with binary codes.

## A15. Chapter Template

Every chapter shall follow exactly the same structure:

1. Chapter title
2. One-line motivating question
3. Learning objectives
4. Prerequisites
5. Running example (continued)
6. Main sections
7. Worked example
8. Algorithms
9. Engineering insights
10. Exercises
11. Common mistakes
12. Summary
13. Preview of next chapter

Example (Chapter 9):

- **Question:** How can infinitely many lattice points become exactly 16 codewords?
- **Learning objectives:** understand quotient groups; generate finite codebooks; enumerate representatives.
- **Running example:** continue the `D4` example.
- **Algorithms:** generate the codebook.
- **Engineering insight:** why fixed-rate quantization requires quotient groups.
- **Exercises:** build the `D4` codebook by hand.
- **Summary:** key ideas.
- **Next:** hierarchical decomposition.

## A16. Definition of Done

A chapter is complete only if

- ✓ motivation is clear,
- ✓ every definition has an example,
- ✓ every theorem has intuition,
- ✓ every algorithm has pseudocode,
- ✓ complexity is analyzed,
- ✓ engineering insight is included,
- ✓ exercises are provided,
- ✓ the running example has been extended,
- ✓ the next chapter has been motivated.

No chapter should be considered complete until all of these criteria are satisfied.

---

# Spec Part B — Chapter Specifications

---

## Book Part I — Foundations

The goal of Part I is to take a reader with only high-school algebra and prepare them to understand lattices. No chapter assumes concepts that have not already been introduced.

---

### Chapter 1 — Why Quantization?

**Central question.** Why do modern neural networks need quantization?

**Motivation.** Large language models are memory-bandwidth limited. Can we reduce memory while preserving computation?

**Topics.**

- Memory footprint
- Scalar quantization
- Dot-product error
- Vector quantization intuition
- Why codebooks appear

**Running example.** Introduce the 8-weight vector `w` and activation vector `x`. Compute `wᵀx`. Show quantization error.

**Figures.** Floating-point weights → quantized weights → dot-product error.

**Algorithms.** None.

**Deliverables.** The reader should understand why quantization exists and why vectors should be quantized jointly.

---

### Chapter 2 — Numbers, Modular Arithmetic and Cosets

**Central question.** How can infinitely many objects become finite?

**Motivation.** Suppose we want exactly 16 possible outputs. How can infinitely many integers be grouped into only sixteen categories?

**Topics.** Integers → division → remainders → modulo arithmetic → equivalence classes → cosets.

**Running example.** Integers modulo 2, 4, 8; then vectors modulo 2.

**Concrete examples.** `17 mod 4`, `−7 mod 4`, the integer number line, modulo circles, 2D integer grids, parity patterns.

**Figures.** Integer number line, modulo classes, modulo clock, integer grid, parity coloring, cosets in `Z²`.

**Algorithms.** Computing modulo; grouping integers; grouping vectors.

**Deliverables.** The reader should understand modulo arithmetic, equivalence classes, and cosets — without knowing abstract algebra.

---

### Chapter 3 — Vectors and Euclidean Geometry

**Central question.** How do we measure similarity between vectors?

**Motivation.** Weights are vectors. Quantization chooses the nearest vector. We need a notion of distance.

**Topics.** Vectors, norms, Euclidean distance, inner products, angles, nearest neighbour.

**Running example.** Compute the L2 distance and dot products between the weight and activation vectors.

**Figures.** 2D vectors, distance, circles, nearest point.

**Algorithms.** Distance computation; nearest neighbour search.

**Deliverables.** Readers understand geometric distance.

---

### Chapter 4 — Classical Vector Quantization

**Central question.** How do we compress vectors?

**Motivation.** Scalar quantization ignores correlation. Can entire vectors be quantized together?

**Topics.** Finite codebooks, nearest codeword, encoding, decoding, bit rate, rate-distortion intuition.

**Running example.** 4-dimensional vectors, a 256-entry codebook, nearest neighbour search.

**Figures.** Voronoi partition, codebook, encoding, decoding.

**Algorithms.** Nearest codeword; brute-force search.

**Complexity.** `O(Kd)`.

**Deliverables.** Reader understands finite codebooks.

---

### Chapter 5 — Lattices from First Principles

**Central question.** Can codebooks be generated mathematically?

**Motivation.** Huge codebooks are impossible to store. We need structure.

**Topics.** Integer grids, bases, generator matrices, lattices, fundamental regions, Voronoi cells.

**Running example.** `Z²` → hexagonal lattice → `D4` preview.

**Figures.** Integer lattice, hexagonal lattice, generator matrix, Voronoi cells.

**Algorithms.** Generating lattice points.

**Deliverables.** Reader understands what a lattice is.

---

### Chapter 6 — The D4 Lattice

**Central question.** Why is `D4` special?

**Motivation.** `D4` is the first useful lattice for quantization.

**Topics.** Generator matrix, parity definition, even-coordinate-sum interpretation, coset decomposition, relationship with `2Z⁴`.

**Running example.** Construct `D4`. Decode several vectors. Parity interpretation.

**Figures.** `D4` lattice slices, parity visualization, cosets.

**Algorithms.** Membership test; generator representation; parity representation.

**Deliverables.** Reader understands multiple views of `D4`.

---

### Chapter 7 — Nearest Lattice Point Algorithms

**Central question.** How do we quantize onto a lattice?

**Motivation.** Brute-force search over infinitely many lattice points is impossible. We need efficient decoding.

**Topics.** Nearest point problem, `Dn` decoder, round-and-fix algorithm, complexity, generalization.

**Running example.** Quantize several vectors. Walk through every arithmetic operation.

**Figures.** Nearest lattice point, Voronoi region, rounding, parity correction.

**Algorithms.** Nearest `Dn` decoder — pseudocode and Python.

**Complexity.** `O(n)`.

**Deliverables.** Reader can implement `D4` decoding.

---

End of Part I. The reader is now prepared for lattice vector quantization.

---

## Book Part II — Lattice Vector Quantization

Part I taught the reader vectors, codebooks, lattices, `D4`, and nearest lattice point algorithms. Part II asks: **how can lattices become practical codebooks for neural networks?**

---

### Chapter 8 — Lattice Vector Quantization

**Central question.** How can an infinite lattice become a practical vector quantizer?

**Motivation.** Classical vector quantization requires storing every codeword; large codebooks become impossible. A lattice appears to solve this because every point can be generated from a basis. However, lattices are infinite. How can an infinite object represent a finite number of bits? This question motivates the next three chapters.

**Learning objectives.** After this chapter the reader should understand

- ✓ lattice quantization,
- ✓ nearest lattice quantization,
- ✓ Voronoi quantization,
- ✓ scaling,
- ✓ why scaling alone does NOT produce a finite codebook.

**Sections.**

- 8.1 Review — classical vector quantization, finite codebooks, nearest neighbour, limitations.
- 8.2 Infinite codebooks — integer lattice, `D4`, hexagonal lattice; illustrate why there are infinitely many lattice points.
- 8.3 Lattice quantizer — introduce `Q_L(v)`, the nearest lattice point; several examples.
- 8.4 Voronoi quantizer — explain Voronoi regions; illustrate that nearest point = Voronoi partition.
- 8.5 Scaling — introduce `β`. Small `β` → large distortion; large `β` → low distortion. Explain granular distortion and overload distortion.
- 8.6 Important observation — scaling does NOT make the codebook finite. This observation motivates quotient groups.

**Running example.** Take our `D4` lattice. Quantize three vectors. Illustrate the nearest lattice point. Show the reconstructed vectors.

**Figures.** Floating-point vector → nearest lattice point; Voronoi partition; scaled lattice; fine lattice; coarse lattice.

**Algorithms.** Nearest lattice point; scaling; encoding.

**Complexity.** Nearest `D4`: `O(n)`. Nearest `E8`: introduce, do not derive.

**Engineering insight.** Scaling controls distortion, NOT bit rate. This distinction is the bridge to Chapter 9.

**Deliverables.** Reader understands lattice quantization, Voronoi quantization, scaling, and why infinite lattices remain infinite.

---

### Chapter 9 — Quotient Groups and Finite Codebooks

**Central question.** How can infinitely many lattice points become exactly 16 or 256 codewords?

This chapter is the mathematical heart of HNLQ.

**Learning objectives.** Reader should understand

- ✓ finite quotient codebooks,
- ✓ cosets,
- ✓ representatives,
- ✓ codebook indices,
- ✓ offline codebook generation.

**Sections.**

- 9.1 Review — modulo arithmetic, cosets, `D4`.
- 9.2 Integer example — `Z` → `4Z`, four cosets, illustrated graphically.
- 9.3 Vector example — `Z²` → `2Z²`, four cosets, illustrated.
- 9.4 `D4` example — `D4` → `2D4`, sixteen cosets; construct every one; illustrate.
- 9.5 Quotient groups — only now define `L/qL`. Readers already know what it means.
- 9.6 Representatives — every coset gets one representative; explain why representatives become codewords.
- 9.7 The HNLQ codebook — introduce `A_q = L ∩ qV`. Explain why exactly `q^d` representatives exist. **Boundary tie-breaking:** lattice points that fall exactly on the boundary of `qV` must be assigned by a fixed deterministic rule (e.g., a half-open fundamental region, or a coordinate-order tie-break); without such a rule the count "exactly `q^d`" fails. State the rule once and use it everywhere — it also makes offline enumeration deterministic and codebook indices stable.
- 9.8 Offline enumeration — show how to generate every codeword offline; store index → representative; explain why this is identical to a classical codebook.
- 9.9 Nearest neighbour — two methods: (1) nearest lattice decoder, (2) brute force over `A_q`. Compare complexity; discuss when each wins.

**Running example.** Generate the complete `D4`, `q = 2` codebook — all 16 entries — and assign fixed indices.

**Figures.** Modulo integers, modulo vectors, cosets, representatives, quotient lattice, offline codebook generation.

**Algorithms.** Generate `A_q`; enumerate indices; nearest representative.

**Complexity.** Offline: `O(q^d)`. Inference: `O(1)` lookup.

**Engineering insight.** This chapter answers why HNLQ achieves fixed-rate coding. Scaling does not; quotient groups do.

**Deliverables.** Reader understands why HNLQ has exactly `q^d` codewords.

---

### Chapter 10 — Hierarchical Nested Lattice Quantization

**Central question.** Can large codebooks be represented as combinations of small codebooks?

This is the central idea of HNLQ.

**Learning objectives.** Reader should understand

- ✓ one-decode-then-digits encoding,
- ✓ base-`q` two's-complement digit decomposition of generator coefficients,
- ✓ each digit as a coset index of `L/qL`,
- ✓ exactness within the coefficient range and overload outside it,
- ✓ why LUTs become small.

**Sections.**

- 10.1 From one codebook to many levels.
- 10.2 One decode, then digits — `y = Q_L(βv)`, coefficients `z`, digit planes.
- 10.3 Digit representatives `c̃_b = G·bits(b)` — why linearity is required and why min-norm representatives cycle.
- 10.4 The decoder as a signed radix expansion; exactness statement.
- 10.5 Complete `D4` example at the calibrated scale.
- 10.6 Overload as coefficient range overflow — detection, clamping/saturation policy, and the measured granular-overload U-curve over `β`.
- 10.7 Why lookup tables stay small.

**Running example.** One complete 8-weight example at the Chapter 8 calibrated scale: lattice points, coefficients, digit tables, indices, exact reconstructions. Include the overload demonstration at an over-large `β` and the measured `β` sweep.

**Figures.** Residual tree, hierarchy, radix expansion, codebook reuse.

**Algorithms.** Encoder; decoder; residual update.

**Engineering insight.** The hierarchy reduces LUT size without changing bit rate. This is the key contribution of HNLQ.

**Deliverables.** Reader can implement HNLQ.

---

### Chapter 11 — One-Sided Lookup Tables

**Central question.** Can dot products be computed without reconstructing weights?

This chapter introduces the practical inference algorithm.

**Learning objectives.** Reader should understand

- ✓ one-sided LUTs,
- ✓ precomputation,
- ✓ lookup accumulation,
- ✓ computational savings.

**Sections.**

- 11.1 Dot products.
- 11.2 Classical inference.
- 11.3 Dequantization cost.
- 11.4 LUT construction.
- 11.5 The one-sided LUT `T_x(b)`.
- 11.6 Complete numerical example.
- 11.7 Complexity.

**Running example.** FP16 activation, quantized weights. Construct `T_x(b)`. Perform the dot product without reconstructing weights.

**Algorithms.** Construct LUT; compute dot product; complexity.

**Engineering insight.** Memory traffic dominates. One-sided LUTs reduce dequantization overhead.

**Deliverables.** Reader can implement one-sided LUT inference.

---

### Chapter 12 — Matrix Multiplication with HNLQ

**Central question.** How do one-sided dot products become GEMM?

**Motivation.** Chapter 11 computed one dot product. Real inference is matrix multiplication: thousands of dot products sharing the same activations and the same codebook. The systems question is whether LUT reuse and reduced memory movement outweigh lookup and accumulation overhead.

**Learning objectives.** Reader should understand

- ✓ blocking and tiling for HNLQ inference,
- ✓ LUT reuse across an activation block,
- ✓ cache, SIMD, and GPU implications,
- ✓ product lattices,
- ✓ the end-to-end inference pipeline.

**Sections.**

- 12.1 From dot products to GEMM.
- 12.2 Blocking and tiling.
- 12.3 Cache locality — where the LUT lives, and why LUT size (Chapter 10) determines whether it stays in cache.
- 12.4 SIMD implementation.
- 12.5 GPU implementation.
- 12.6 Tensor Core implications.
- 12.7 Product lattices.
- 12.8 End-to-end inference pipeline.

**Running example.** Extend the running dot-product example to a small matrix multiplication: an `8 × 8` weight matrix (sixteen `D4` blocks) times the running activation vector, with `T_x(b)` shared across the weight rows.

**Figures.** Tiling diagram, memory hierarchy with LUT placement, LUT reuse across tiles, arithmetic-versus-memory-traffic comparison.

**Algorithms.** Blocked HNLQ matrix multiplication; lookup-table accumulation across tiles.

**Complexity.** LUT construction amortized over rows; per-output-element lookup/accumulate cost; memory traffic versus a dequantize-then-GEMM baseline.

**Engineering insight.** The core systems question is memory movement, not arithmetic count. HNLQ wins when LUTs stay resident in fast memory while compressed indices stream through.

**Deliverables.** Reader can implement a CPU prototype of HNLQ GEMM and reason about its GPU mapping.

---

### Chapter 13 — HNLQ in Practice: Quantizing a Real Model

**Central question.** Does HNLQ work on a real network — and how would we know?

**Motivation.** Everything so far quantizes an 8-value toy vector. Deploying HNLQ on a real model raises questions the mathematics alone does not answer: how to choose `β`, how to organize tensors into blocks, how to measure quality, and how HNLQ compares with the scalar methods practitioners already use.

**Important note.** This chapter reports what the method does on a real model at matched bit rate. It must clearly separate measured results from expectations.

**Learning objectives.** Reader should understand

- ✓ calibration of `β` from weight statistics (per-tensor and per-group),
- ✓ the quantization pipeline for a full weight matrix / model,
- ✓ evaluation metrics (weight MSE, layer output error, perplexity or task accuracy),
- ✓ comparison against scalar baselines (e.g., INT4 round-to-nearest, GPTQ/AWQ-style methods) at matched bits per weight.

**Sections.**

- 13.1 From blocks to tensors.
- 13.2 Calibrating `β` — granular versus overload distortion in practice.
- 13.3 The quantization pipeline.
- 13.4 Evaluation metrics.
- 13.5 Baselines at matched bit rate.
- 13.6 Case study — quantizing a small pretrained model.
- 13.7 What HNLQ buys, and what it does not.

**Running example.** Promote the running example to model scale: the 8-weight vector becomes one block of a real weight matrix taken from a small pretrained model, and the same encode/LUT/GEMM workflow runs end to end.

**Figures.** Weight and error histograms, `β` sweep (granular vs overload distortion), accuracy versus bits-per-weight curve.

**Algorithms.** `β` calibration; end-to-end quantize–evaluate loop.

**Engineering insight.** Calibration is cheap; evaluation dominates. Per-group scaling interacts with LUT sharing — finer groups improve accuracy but multiply LUT work.

**Deliverables.** Reader can quantize a real model with HNLQ and produce a fair comparison against scalar baselines.

---

End of Part II. The reader can now implement HNLQ from scratch and apply it to a real model.

---

## Book Part III — Structured Lattices and Binary Representations

Part II showed: floating point → lattice quantization → hierarchical nested lattice quantization → fast dot products. Part III asks: **can the structure of the lattice itself provide an even better representation?**

Instead of treating lattice points as arbitrary vectors, we exploit their algebraic structure. The central theme is:

> Geometry → Algebra → Binary Representation → Efficient Computation

---

### Chapter 14 — Beyond D4: Higher-Dimensional Lattices

**Central question.** Why stop at `D4`? Can better lattices produce better quantizers?

**Motivation.** `D4` is convenient, but it is not the densest lattice. Can denser lattices reduce quantization error, improve coding gain, and improve inference?

**Learning objectives.** Reader should understand

- ✓ `Dn`,
- ✓ `E8`,
- ✓ the Leech lattice (overview),
- ✓ coding gain,
- ✓ packing density,
- ✓ why `E8` is special.

**Sections.**

- 14.1 Review of `D4`.
- 14.2 General `Dn`.
- 14.3 Construction of `E8`.
- 14.4 Voronoi cells.
- 14.5 Quantization gain.
- 14.6 Practical implications.

**Running example.** Repeat our `D4` example using `E8` (the 8-value weight vector is exactly one `E8` block). Compare quantization error, bit rate, and complexity.

**Figures.** `D4` projection, `E8` projection, Voronoi cells, packing density, comparison table.

**Algorithms.** Nearest `Dn`; nearest `E8` — implementation overview only; detailed algorithms deferred to an appendix.

**Engineering insight.** Better lattices → lower distortion, but → higher decoding complexity. Discuss the tradeoff.

---

### Chapter 15 — Barnes–Wall Lattices

**Central question.** Can lattices be described without generator matrices?

**Motivation.** So far every lattice has been introduced via generator matrix → nearest point → quantization. Barnes–Wall introduces code constraints → binary structure → recursive construction. This opens an entirely different viewpoint.

**Learning objectives.** Reader should understand

- ✓ the Barnes–Wall hierarchy,
- ✓ recursive construction,
- ✓ binary interpretation,
- ✓ the relationship to `D4`,
- ✓ the relationship to `E8`.

**Sections.**

- 15.1 Motivation.
- 15.2 Recursive construction.
- 15.3 `D4` revisited.
- 15.4 `RE8` — the rotated `E8` lattice. Define the rotation-and-scaling operator `R` used in the Barnes–Wall recursion on first use; `RE8` denotes `R` applied to `E8` (a rotated, scaled copy of `E8`).
- 15.5 The Barnes–Wall hierarchy.
- 15.6 Recursive decoding.

**Running example.** Express `D4` both as a generator matrix and as parity constraints. Compare.

**Figures.** Recursive lattice, Barnes–Wall tree, generator vs recursion, hierarchy.

**Algorithms.** Recursive construction; membership; decoding overview.

**Engineering insight.** Generator matrices are not the only way to represent lattices. Recursive structure can simplify storage, reasoning, and implementation.

---

### Chapter 16 — Reed–Muller Codes

**Central question.** Why do binary error-correcting codes suddenly appear inside lattices?

**Motivation.** The parity constraints observed in `D4` are not accidental. They arise from binary codes. This chapter explains why.

**Learning objectives.** Reader should understand

- ✓ binary linear codes,
- ✓ binary generator matrices,
- ✓ parity,
- ✓ Reed–Muller codes,
- ✓ why Barnes–Wall uses them.

**Sections.**

- 16.1 Binary vectors.
- 16.2 Linear codes.
- 16.3 Even parity.
- 16.4 Reed–Muller codes.
- 16.5 `D4` revisited.
- 16.6 Barnes–Wall.

**Running example.** Show `D4 = 2Z⁴ + parity code`. Construct every codeword. Explain.

**Figures.** Binary cube, parity code, generator matrix, code tree.

**Engineering insight.** The lattice now has both geometry and binary structure. This duality becomes the foundation for the next chapter.

---

### Chapter 17 — Bit-Plane Representations

**Central question.** What does a lattice point look like in binary?

**Motivation.** Weights are stored digitally; eventually everything becomes bits. Can lattice points be represented directly as structured bit planes?

**Learning objectives.** Reader should understand

- ✓ bit planes,
- ✓ binary decomposition,
- ✓ LSB constraints,
- ✓ Reed–Muller structure,
- ✓ compression implications.

**Sections.**

- 17.1 Binary integers.
- 17.2 Bit planes.
- 17.3 `D4` bit planes.
- 17.4 `E8` bit planes.
- 17.5 Recursive decomposition.
- 17.6 Compression.

**Running example.** Take our `D4` vector. Convert to binary. Show every bit plane. Identify the Reed–Muller codeword.

**Figures.** Binary expansion, bit planes, LSB, MSB, recursive decomposition.

**Engineering insight.** Bit planes are not arbitrary — they inherit lattice structure. This observation is absent from most ML quantization literature.

---

### Chapter 18 — Toward Binary-Domain Computation

**Central question.** Can computation itself happen directly on structured binary representations?

**Important note.** This chapter distinguishes established literature from research directions. Every speculative idea must be clearly marked.

**Motivation.** HNLQ reduces dequantization. Bit-plane representations introduce binary structure. Can these ideas be combined?

**Sections.**

- 18.1 Review.
- 18.2 The HNLQ hierarchy.
- 18.3 Binary representations.
- 18.4 Possible computational models.
- 18.5 Transform-domain methods.
- 18.6 Open problems.

**Discussion topics.** Factorization of dot products; Walsh–Hadamard transforms; binary accumulations; recursive evaluation; hardware implications; Tensor Core redesign.

**Engineering insight.** This chapter intentionally poses research questions rather than finished algorithms. It serves as a bridge between existing literature and future work.

---

End of Part III.

---

# Spec Part C — Project Standards

## C1. Repository Layout

The repository root *is* the Quarto book (there is no `book/` subdirectory). Chapters are Quarto `.qmd` files.

```
vq-book/
    _quarto.yml                     # Quarto book configuration
    BOOK_SPEC.md                    # this specification
    README.md
    index.qmd                       # preface / landing page
    notation.qmd                    # canonical notation table (appendix; mirrors §A7)
    references.qmd
    references.bib                  # bibliography
    styles.css
    chapters/
        01-why-quantization.qmd
        02-numbers-modulo-cosets.qmd
        ...
        18-toward-binary-domain-computation.qmd
    appendices/
        solutions.qmd               # exercise solutions, organized by chapter
    figures/                        # reproducible figure sources (Python) and assets
    code/
        python/                     # readable reference implementations
        numpy/
        pytorch/
        cuda/
    tests/                          # tests for executable numerical examples
    .github/workflows/publish.yml   # CI: renders the book, publishes _site/ to GitHub Pages
```

Standards:

- Every figure and algorithm has stable numbering (Quarto cross-references).
- Every numerical example has executable code.
- Every figure is reproducible from sources under `figures/`.
- The rendered site is written to `_site/` (git-ignored); publishing happens via the GitHub Actions workflow.

## C2. References

The book should cite

- Conway & Sloane,
- Forney,
- Barnes and Wall,
- Conway's sphere-packing papers,
- nearest lattice decoding,
- lattice VQ,
- hierarchical nested lattice quantization,
- recent neural-network quantization papers (including the scalar baselines used in Chapter 13).

Each chapter should conclude with **Further Reading**.

## C3. Long-Term Goals

The manuscript is a single Quarto source that renders to the HTML site (published to GitHub Pages via CI) and, later, to PDF via Quarto's LaTeX pipeline. No separate Markdown/Jupyter Book/MkDocs conversions are planned — Quarto covers these targets.

The code should become an educational library. Possible future packages: `latticequant`, `hnlq`, `d4`, `e8`, `lookup`, `decoder`. The book and software should evolve together.

## C4. Future Research Directions

The final chapter intentionally transitions from established literature to open research. Potential topics include

- Barnes–Wall HNLQ,
- bit-plane HNLQ,
- binary-domain GEMM,
- lattice-aware tensor cores,
- recursive lookup tables,
- hardware accelerators,
- product lattices for transformers,
- KV-cache lattice compression,
- activation quantization,
- learned lattices.

These sections must clearly distinguish published results from author hypotheses.

## C5. Success Criteria

The project is successful if a graduate student with no background in coding theory or abstract algebra can

- implement Hierarchical Nested Lattice Quantization from scratch,
- understand why quotient groups appear,
- derive the `D4` codebook,
- implement one-sided lookup tables,
- quantize a real model and evaluate it against scalar baselines,
- and understand why Barnes–Wall lattices naturally lead to structured binary representations.

If the reader reaches this point, the book has achieved its objective.

---

End of BOOK_SPEC.md
