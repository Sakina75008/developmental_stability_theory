"""Figure S2: Circular inference converts weak evidence into strong
belief (Supplementary S2; Eqs. 10-11)."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import circular, style
from dst.style import BLUE, GOLD, NAVY, RED

style.use_style()
L_S = 0.5

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.2))

# --- Panel A: recursion trajectories ---------------------------------------
for lam, color in ((0.3, BLUE), (0.6, GOLD), (0.9, RED)):
    L = circular.belief_recursion(L_S, lam)
    ax1.plot(range(len(L)), np.abs(L), "-o", ms=4.5, color=color,
             label=rf"$\lambda={lam}$")
ax1.set(xlabel="recursion step (message passed up/down)",
        ylabel="belief certainty  |log-odds|",
        title="A  The same evidence, echoed by feedback")
ax1.legend()

# --- Panel B: equilibrium certainty diverges at lambda = 1 -----------------
lam = np.linspace(0, 0.995, 400)
ax2.plot(lam, circular.equilibrium_certainty(L_S, lam), color=NAVY)
ax2.axvline(1.0, ls="--", color=RED, lw=2.5)
ax2.annotate("delusional\nfixation", (0.93, 7), xytext=(0.55, 8.5),
             color=RED, fontweight="bold", fontsize=14,
             arrowprops=dict(arrowstyle="->", color=RED))
ax2.text(1.005, 4.5, r"$\lambda=1 \Leftrightarrow g\sigma\sqrt{D}=1$"
         "\n(same threshold as Fig. 1)", color=RED, fontsize=11,
         rotation=90, va="center")
ax2.set(xlabel=r"loop gain  $\lambda = g\,\sigma\sqrt{D}$  "
               "(open-loop recurrent gain)",
        ylabel=r"equilibrium certainty  $L^* = L_s/(1-\lambda)$",
        xlim=(0, 1.05), ylim=(0, 12),
        title="B  Divergence coincides with the stability boundary")

fig.tight_layout()
style.save(fig, out("Figure_S2.png"))
