"""Figure 2: Temporal binding windows — developmentally-set width,
further widened by aberrant precision (Eq. 15, section 3.2)."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import binding, style
from dst.diagram import arrow, box
from dst.style import BLUE, RED, GOLD, GRAY, PURPLE

style.use_style()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 6))

# --- Panel A: posterior vs offset for slow and fast modalities -------------
dt = np.linspace(-200, 200, 601)
for s_t, color, label in ((25, BLUE, r"audio/tactile  ($\sigma_t=25$ ms)"),
                          (75, RED, r"visual-dominant  ($\sigma_t=75$ ms)")):
    ax1.plot(dt, binding.posterior_common_cause(dt, s_t), color=color,
             label=label)
ax1.axhline(0.5, ls=":", color=GRAY)
ax1.set(xlabel=r"cross-modal offset $\Delta t$ (ms)",
        ylabel="posterior P(single cause)",
        title="A  Wider binding is optimal\nfor a slower modality")
ax1.legend(loc="lower center", fontsize=11)

# --- Panel B: optimal width scales with temporal uncertainty ---------------
s_ts = np.linspace(10, 100, 200)
ax2.plot(s_ts, binding.optimal_width(s_ts), color=style.NAVY)
for s_t, color in ((25, BLUE), (75, RED)):
    ax2.plot(s_t, binding.optimal_width(np.array(s_t)), "o", ms=11,
             color=color)
ax2.set(xlabel=r"modality temporal uncertainty $\sigma_t$ (ms)",
        ylabel=r"optimal binding-window width  $w^*$ (ms)",
        title="B  $w^* \\propto \\sigma_t$:\nwidth is set by development")

# --- Panel C: two separable routes to a wide TBW ---------------------------
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 10)
ax3.axis("off")
ax3.set_title("C  Two separable routes to a wide TBW")
ax3.text(2.7, 9.4, "developmental\n(baseline)", color=BLUE, ha="center",
         fontweight="bold")
ax3.text(7.3, 9.4, "state\n(dopaminergic)", color=RED, ha="center",
         fontweight="bold")
box(ax3, (2.7, 7.8), 3.4, 1.2, "early visual\ndominance", BLUE)
box(ax3, (7.3, 7.8), 3.4, 1.2, "aberrant\nprecision  g$\\uparrow$", RED)
box(ax3, (2.7, 5.3), 3.4, 1.2, "wide baseline\nTBW", BLUE)
box(ax3, (7.3, 5.3), 3.4, 1.2, "state widening\nof TBW", RED)
box(ax3, (5.0, 2.9), 3.6, 1.2, "spurious\nbinding  $\\sigma\\uparrow$", GOLD)
box(ax3, (5.0, 0.7), 3.0, 1.1, "psychosis", PURPLE)
arrow(ax3, (2.7, 7.2), (2.7, 5.95), BLUE)
arrow(ax3, (7.3, 7.2), (7.3, 5.95), RED)
arrow(ax3, (3.3, 4.6), (4.3, 3.55), BLUE)
arrow(ax3, (6.7, 4.6), (5.7, 3.55), RED, ls="--")
arrow(ax3, (5.0, 2.3), (5.0, 1.3), PURPLE)

fig.tight_layout()
style.save(fig, out("Figure_2.png"))
