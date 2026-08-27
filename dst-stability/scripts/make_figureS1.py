"""Figure S1: Higher dimensionality yields combinatorially many unstable
and false states (Supplementary S1; qualitative illustration)."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import hopfield, stability, style
from dst.style import BLUE, GOLD, GREEN, NAVY, RED

style.use_style()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.2))

# --- Panel A: unstable directions vs D ------------------------------------
Ds = np.arange(5, 245, 10)
rng = np.random.default_rng(2)
for g, color in ((0.10, BLUE), (0.14, GOLD), (0.18, RED)):
    counts = np.array([[stability.n_unstable(int(D), g, rng=rng)
                        for _ in range(5)] for D in Ds])
    m, sd = counts.mean(1), counts.std(1)
    ax1.plot(Ds, m, "-o", ms=4.5, color=color, label=rf"$g={g}$")
    ax1.fill_between(Ds, m - sd, m + sd, color=color, alpha=0.15)
ax1.set(xlabel=r"modal dimensionality $D$",
        ylabel="number of self-amplifying directions\n"
               r"(Re$\,\lambda>0$)",
        title=r"A  Unstable directions grow ~linearly with $D$")
ax1.legend()

# --- Panel B: Hopfield attractor proliferation -----------------------------
ps = np.arange(2, 25, 2)
tot, spur = zip(*(hopfield.hopfield_attractors(N=80, p=int(p), seed=3)
                  for p in ps))
ax2.plot(ps, tot, "-o", color=NAVY, label="all fixed-point attractors")
ax2.plot(ps, spur, "-s", color=RED, label="spurious (false) attractors")
ax2.plot(ps, ps, ":", color=GREEN, lw=2.5, label="stored 'true' features (= p)")
ax2.set(xlabel=r"number of encoded features $p$  (a proxy for $D$)",
        ylabel="distinct attractor states\n(Hopfield network, $N=80$)",
        title="B  False attractors proliferate super-linearly")
ax2.legend()

fig.tight_layout()
style.save(fig, out("Figure_S1.png"))
