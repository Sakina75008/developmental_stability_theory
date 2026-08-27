# Developmental Stability Theory of Predictive Hierarchies

Simulation and figure-generation code for the manuscript

> **A Developmental Stability Theory of Predictive Hierarchies: Why Some Perceptual Architectures Remain Stable Under Perturbation.**
> *Computational Psychiatry* (under review).

Developmental Stability Theory (DST) models a perceptual hierarchy as a
high-dimensional dynamical system and derives a single stability criterion,
**gσ√D < 1**, in which the effective dimensionality of the dominant modality
(*D*), its aggregate coupling (*σ*), and the neuromodulatory gain on prediction
errors (*g*) multiply. This repository regenerates **every figure in the paper
— main-text Figures 1–8 and Supplementary Figures S1–S7 — directly from the
model equations**, with no external data.

---

## Quick start

```bash
git clone https://github.com/Sakina75008/developmental_stability_theory.git
cd dst-stability
pip install -r requirements.txt
python scripts/make_all.py          # regenerates all 15 figures (~1 min)
```

Figures are written as 300-dpi PNGs to `figures/`. Any single figure can be
regenerated on its own, e.g.:

```bash
python scripts/make_figure5.py
python scripts/make_figureS4.py
```

There is nothing to download and no data to fetch: the paper uses no empirical
data, and every panel is produced from the equations in the `dst/` package.

---

## Repository layout

```
dst-stability/
├── dst/                 # the model, one module per component
│   ├── stability.py     #   Eqs. (3)–(6): random-matrix stability, gσ√D = 1, D_c
│   ├── circular.py      #   Eqs. (10)–(11): circular inference, divergence at λ = 1
│   ├── binding.py       #   Eq. (15): temporal binding windows, w* ∝ σ_t
│   ├── neuron.py        #   Eqs. (18)–(20), (S3)–(S7): two-point neuron, κ/η, cascade
│   ├── cohort.py        #   Eq. (S8), §§S6–S8: three observables, mechanism recovery
│   ├── course.py        #   Eq. (21): OU gain fluctuation + plasticity ratchet
│   ├── hopfield.py      #   §S1: spurious-attractor proliferation (illustration)
│   ├── diagram.py       #   box-and-arrow helpers for schematic panels
│   └── style.py         #   shared matplotlib style
├── scripts/
│   ├── make_figure1.py … make_figure8.py     # main-text figures
│   ├── make_figureS1.py … make_figureS7.py   # supplementary figures
│   └── make_all.py                           # regenerate everything
├── figures/             # output PNGs (produced by the scripts)
├── requirements.txt
├── LICENSE              # MIT
└── CITATION.cff
```

### Figure ↔ equation map

| Figure | Script | Model component (equations) |
|---|---|---|
| 1 | `make_figure1.py` | Stability landscape; boundary gσ√D = 1; critical D_c (3–6) |
| 2 | `make_figure2.py` | Temporal binding windows, w* ∝ σ_t (15) |
| 3 | `make_figure3.py` | Phase diagram of five phenotypes (13) |
| 4 | `make_figure4.py` | Laminar mapping of g, σ, λ onto cortical microcircuitry |
| 5 | `make_figure5.py` | Composed cascade f → (κ,η) → σ → S (18–20) |
| 6 | `make_figure6.py` | Mechanism identifiability, leave-one-out recovery (S8) |
| 7 | `make_figure7.py` | Clinical course: gain fluctuation + ratchet (21) |
| 8 | `make_figure8.py` | Developmental trajectories through the stability plane |
| S1 | `make_figureS1.py` | Hopfield spurious-attractor proliferation (§S1) |
| S2 | `make_figureS2.py` | Belief-space divergence at λ = 1 (10–11) |
| S3 | `make_figureS3.py` | Biophysical bridge: κ↓, η↑ under NMDA hypofunction (S3–S4) |
| S4 | `make_figureS4.py` | Analytic peak condition + 10,000-set robustness sweep (S5–S7) |
| S5 | `make_figureS5.py` | Conditional leak + heterogeneity mixture recovery (S6) |
| S6 | `make_figureS6.py` | Apical integration and its unique signature (S7) |
| S7 | `make_figureS7.py` | Predicted volatility of reliability weighting (§S9) |

---

## Headline results reproduced

Running `make_all.py` reproduces every quantitative claim in the paper. With the
fixed random seeds shipped in the scripts, the numbers below come out exactly:

- The simulated stability boundary coincides with **gσ√D = 1** with no free
  parameters (Figure 1); the belief-space divergence coincides with the same
  threshold (Figure S2).
- Composed cascade, high-risk sighted hierarchy (Figure 5): at *f* = 1,
  κ = 1.66, η = 0.21, σ = 2.54, S = +0.09; at *f* = 0.5, κ = 0.25, η = 0.74,
  σ = 3.81, S = −0.36. The same lesion crosses threshold at **18%** NMDAR loss
  in a high-risk hierarchy, **42%** in a resilient one, and **never** in the
  congenitally blind hierarchy.
- Robustness sweep over 10,000 parameter sets (Figure S4): κ falls in **98.4%**,
  η rises in **100%**, η is non-monotonic in **100%**; analytic vs. numerical
  peak **r = 0.86**; leak optimum at **median f = 0.57**.
- Mechanism recovery (Figure 6): **90%** overall, apical decoupling recovered at
  **100%**, residual error confined to the intact-versus-noise boundary.
- Mixture recovery (Figure S5): true (15, 40, 25, 20)% → recovered
  (18, 41, 25, 16)%; apical fraction 0.41 vs. 0.40; **N ≈ 100** suffices for
  ±10% on the apical fraction.
- Clinical course (Figure 7): identical gain noise yields remitting, relapsing
  and declining courses (**3, 4, 7** episodes) as only the ratchet rate ρ varies.

---

## A note on parameters

As stated in the manuscript (§3.7), the constants that appear here — the neuron
calibration in `dst/neuron.py`, the hierarchy profiles (σ_struct, D, g) in the
figure scripts, the lumped constant *c*, and the cohort noise levels — are
**illustrative calibrations chosen to place an intact hierarchy in the stable
regime, not parameters fitted to data**. The neuron calibration is set so the
measured dendritic coefficients reproduce the worked example of §3.7
(κ = 1.66, η = 0.21 at *f* = 1; κ = 0.25, η = 0.74 at *f* = 0.5).

What is *structural* rather than tuned — the direction of the coefficient
changes, the existence of an interior leak optimum, and the D-dependence of the
crossing — is exactly what the 10,000-set robustness sweep in
`make_figureS4.py` verifies.

All stochastic steps use fixed NumPy seeds, so `make_all.py` is deterministic
and byte-for-byte reproducible across runs.

---

## Requirements

Python ≥ 3.9 with `numpy`, `scipy`, and `matplotlib` (see `requirements.txt`).
No GPU, no network access, no datasets.

## Citation

If you use this code, please cite the paper (see `CITATION.cff`). BibTeX:

```bibtex
@article{dst2026,
  title   = {A Developmental Stability Theory of Predictive Hierarchies:
             Why Some Perceptual Architectures Remain Stable Under Perturbation},
  author  = {Sakina Bukhari},
  journal = {Computational Psychiatry},
  year    = {2026},
  note    = {Under review}
}
```

## License

MIT — see [`LICENSE`](LICENSE).
