"""Figure 1: Dimensionality and gain enter one stability criterion.

(A) Simulated leading eigenvalue across D and g; the black curve is the
theoretical boundary g*sigma*sqrt(D) = 1 (Eq. 5).
(B) The safe dimensionality D_c = 1/(g*sigma)^2 collapses as gain rises.
"""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import stability, style
from dst.style import BLUE, RED, GRAY, NAVY

style.use_style()
SIGMA = 1.0

Ds = np.linspace(5, 200, 28).astype(int)
gs = np.linspace(0.005, 0.35, 28)
grid = stability.stability_grid(Ds, gs, sigma=SIGMA, n_rep=3, seed=1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 6.2))

# --- Panel A: stability landscape -----------------------------------------
pm = ax1.pcolormesh(Ds, gs, grid, cmap="RdBu_r", vmin=-4, vmax=4,
                    shading="nearest")
D_line = np.linspace(Ds.min(), Ds.max(), 300)
ax1.plot(D_line, 1.0 / (SIGMA * np.sqrt(D_line)), "k", lw=3,
         label=r"$g\sigma\sqrt{D}=1$  (theory)")
ax1.set(xlabel=r"modal dimensionality $D$ (interacting features)",
        ylabel=r"precision gain on prediction error $g$"
               "\n(dopaminergic)",
        ylim=(0, 0.35),
        title="A  Stability landscape of the hierarchy")
ax1.legend(loc="upper right")
ax1.text(120, 0.27, "UNSTABLE\n(runaway inference)", color=RED,
         fontweight="bold", ha="center")
ax1.text(70, 0.03, "STABLE", color=BLUE, fontweight="bold", ha="center",
         fontsize=15)
cb = fig.colorbar(pm, ax=ax1)
cb.set_label(r"leading eigenvalue  max Re$\,\lambda(J)$")

# --- Panel B: critical dimensionality --------------------------------------
g_line = np.linspace(0.06, 0.35, 300)
Dc = stability.critical_D(g_line, SIGMA)
ax2.plot(g_line, Dc, color=RED, lw=3)
ax2.fill_between(g_line, Dc, 260, color=style.STABLE_FILL, zorder=0)
ax2.fill_between(g_line, 0, Dc, color=style.UNSTABLE_FILL, zorder=0)
ax2.axhline(150, ls=":", color=GRAY)
ax2.text(0.2, 156, r"vision-dominant hierarchy (high $D$)", color=NAVY,
         fontsize=11)
ax2.axhline(12, ls=":", color=GRAY)
ax2.text(0.2, 18, r"audio/tactile hierarchy (low $D$)", color=NAVY,
         fontsize=11)
ax2.text(0.12, 200, "stable", color=BLUE, fontweight="bold", fontsize=15)
ax2.text(0.28, 45, "unstable", color=RED, fontweight="bold", fontsize=15)
ax2.set(xlabel=r"precision gain $g$",
        ylabel=r"critical dimensionality  $D_c = 1/(g\sigma)^2$",
        ylim=(0, 260),
        title="B  Higher gain shrinks the safe dimensionality")

fig.suptitle(r"Figure 1.  Dimensionality and gain enter one stability "
             r"criterion:  $g\,\sigma\sqrt{D} < 1$", fontsize=16,
             fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.95))
style.save(fig, out("Figure_1.png"))
