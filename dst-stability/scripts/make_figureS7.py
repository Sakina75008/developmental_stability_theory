"""Figure S7: Predicted volatility of sensory reliability weighting
(Supplementary S9) — a precision-weighted update rule in an audiovisual
spatial-localisation task; volatility, not the mean, is diagnostic."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import style
from dst.style import BLUE, GRAY, GREEN, RED

style.use_style()

N_TRIALS = 120
rng = np.random.default_rng(21)

# (label, colour, learning-rate/stiffness, precision-fluctuation scale)
GROUPS = [
    ("congenitally blind (stiff, near-optimal)", GREEN, 0.14, 0.13),
    ("healthy sighted (flexible, low volatility)", BLUE, 0.26, 0.13),
    ("high-risk / late blindness (volatile)", RED, 0.60, 0.15),
]

fig, ax = plt.subplots(figsize=(11.5, 7))
shared_evidence = 0.5 + 0.08 * rng.standard_normal(N_TRIALS)  # same trials

for label, color, lr, jitter in GROUPS:
    w = np.empty(N_TRIALS)
    w[0] = 0.5
    for t in range(1, N_TRIALS):
        # precision-weighted update toward noisy per-trial reliability
        target = shared_evidence[t] + jitter * rng.standard_normal()
        w[t] = np.clip(w[t - 1] + lr * (target - w[t - 1]), 0, 1)
    var = w.var()
    ax.plot(np.arange(N_TRIALS), w, color=color, lw=2,
            label=f"{label}  (Var={var:.3f})")
    print(f"{label}: Var = {var:.4f}")

ax.axhline(0.5, ls=":", color=GRAY)
ax.set(xlabel="trial", ylabel=r"estimated audio weight $w$",
       ylim=(0, 1),
       title="Predicted volatility of sensory reliability weighting\n"
             "(ventriloquist-style test)")
ax.legend(fontsize=11)

fig.tight_layout()
style.save(fig, out("Figure_S7.png"))
