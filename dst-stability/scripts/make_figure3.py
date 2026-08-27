"""Figure 3: One phase diagram, many phenotypes (predictions).

The boundary g*sigma*sqrt(D) = 1 divides a resilient region from a
fragile one; five conditions sit at distinct, falsifiable coordinates
(section 3.4). Coordinates are illustrative placements, not fits.
"""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import style
from dst.diagram import arrow
from dst.style import (BLUE, GOLD, GRAY, GREEN, NAVY, PURPLE, RED,
                       STABLE_FILL, UNSTABLE_FILL)

style.use_style()

fig, ax = plt.subplots(figsize=(11, 8.5))

g = np.linspace(0.05, 1.0, 400)
boundary = 1.0 / g
ax.plot(g, boundary, "k", lw=3, label=r"$g\,\sigma\sqrt{D}=1$")
ax.fill_between(g, boundary, 16, color=UNSTABLE_FILL, zorder=0)
ax.fill_between(g, 0, boundary, color=STABLE_FILL, zorder=0)

# Illustrative condition placements (g, sigma*sqrt(D), colour, label)
conditions = [
    (0.34, 8.5, BLUE, "healthy sighted"),
    (0.72, 12.5, RED, "schizophrenia"),
    (0.16, 2.2, GREEN, "congenital\ncortical blindness"),
    (0.30, 12.8, PURPLE, "late / peripheral blindness\n(orphaned visual priors)"),
    (0.80, 3.2, GOLD, "autism (HIPPEA):\nhigh gain, low recursion\n$\\rightarrow$ illusion-resistant"),
]
for gx, sy, color, _ in conditions:
    ax.plot(gx, sy, "o", ms=15, color=color, mec="white", mew=1.5, zorder=5)

ax.annotate("healthy sighted", (0.34, 8.5), xytext=(0.42, 6.8),
            color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=BLUE))
ax.annotate("schizophrenia", (0.72, 12.5), xytext=(0.52, 13.4),
            color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=RED))
ax.annotate("congenital\ncortical blindness", (0.16, 2.2),
            xytext=(0.2, 3.6), color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=GREEN))
ax.annotate("late / peripheral blindness\n(orphaned visual priors)",
            (0.30, 12.8), xytext=(0.26, 14.3), color=NAVY,
            fontweight="bold", arrowprops=dict(arrowstyle="-", color=PURPLE))
ax.annotate("autism (HIPPEA):\nhigh gain, low recursion\n"
            "$\\rightarrow$ illusion-resistant", (0.80, 3.2),
            xytext=(0.56, 4.0), color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=GOLD))

# Psychedelic excursion: reversible, up-and-right (section 3.4)
arrow(ax, (0.37, 8.9), (0.62, 11.2), PURPLE, lw=3, ls="--")
ax.text(0.44, 9.4, "psychedelics\n(REBUS, reversible)", color=PURPLE,
        rotation=24, fontweight="bold", fontsize=12)

ax.text(0.62, 14.6, r"UNSTABLE  ($g\sigma\sqrt{D}>1$)", color=RED,
        fontsize=15, fontweight="bold")
ax.text(0.09, 1.1, "STABLE", color=BLUE, fontsize=15, fontweight="bold")
ax.set(xlabel=r"precision gain on prediction errors $g$ "
              "(dopaminergic salience)",
       ylabel=r"structural coupling $\sigma\sqrt{D}$"
              "\n(modal dimensionality $\\times$ binding load)",
       xlim=(0.05, 1.0), ylim=(0, 16),
       title=r"developmental constraints set $\sigma\sqrt{D}$, "
             r"state factors set $g$")
ax.legend(loc="lower right")

fig.tight_layout()
style.save(fig, out("Figure_3.png"))
