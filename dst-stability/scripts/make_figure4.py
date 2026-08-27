"""Figure 4: Laminar mapping of the model's parameters onto cortical
microcircuitry (section 3.6)."""

import matplotlib.pyplot as plt

from _common import out
from dst import style
from dst.diagram import arrow, box
from dst.style import BLUE, GRAY, NAVY, PURPLE, RED

style.use_style()

fig, ax = plt.subplots(figsize=(15, 8))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")
ax.set_title(r"Laminar mapping: which cell populations implement "
             r"$g$, $\sigma$, and $\lambda$", pad=18)

LAYERS = [
    ("L1", "apical tuft dendrites", 8.0, "#eaf0fa", ""),
    ("L2/3", "superficial pyramidal", 6.4,
     "#e8f2e9", r"$\gamma$  prediction error $\varepsilon$"),
    ("L4", "granular input", 5.0, "#fdf3e3", ""),
    ("L5/6", "deep pyramidal", 3.3, "#f3ecf7",
     r"$\beta/\alpha$  prediction"),
]
for name, sub, y, fc, tag in LAYERS:
    ax.add_patch(plt.Rectangle((2.2, y - 0.65), 6.6, 1.3, facecolor=fc,
                               edgecolor=GRAY, lw=1.5, zorder=2))
    ax.text(2.5, y + 0.25, name, fontweight="bold", fontsize=15,
            color=NAVY, zorder=3)
    ax.text(2.5, y - 0.3, sub, fontsize=12, color=GRAY, zorder=3)
    if tag:
        ax.text(8.5, y + 0.15, tag, fontsize=13, color=BLUE if "error" in tag
                else RED, ha="right", fontweight="bold", zorder=3)

# apical amplification box above L1
box(ax, (5.5, 9.4), 5.4, 0.9, "apical amplification (BAC firing / NMDA)",
    PURPLE, fontsize=13)
arrow(ax, (5.5, 8.95), (5.5, 8.55), PURPLE)
# L4 -> L2/3 feedforward
arrow(ax, (4.2, 5.4), (4.2, 6.0), BLUE)
ax.text(4.35, 5.6, r"L4 $\rightarrow$ L2/3", color=BLUE, fontsize=11)
# feedforward / feedback side arrows
arrow(ax, (1.5, 3.0), (1.5, 8.2), BLUE, lw=3)
ax.text(1.0, 5.5, "FEEDFORWARD", color=BLUE, rotation=90, va="center",
        fontweight="bold")
arrow(ax, (9.4, 3.0), (9.4, 8.2), RED, lw=3)
ax.text(9.8, 5.5, "FEEDBACK", color=RED, rotation=90, va="center",
        fontweight="bold")

# right-hand mapping boxes
box(ax, (13.0, 8.0), 5.4, 1.0,
    r"SST $\rightarrow$ L1 gates apical context  $\Rightarrow$  sets $\sigma$",
    PURPLE, fontsize=12)
box(ax, (13.0, 6.4), 5.4, 1.0,
    r"PV $\rightarrow$ L2/3 gain on error units  $\Rightarrow$  sets $g$",
    BLUE, fontsize=12)
box(ax, (13.0, 3.6), 5.4, 1.0,
    r"L5/6 $\rightarrow$ pulvinar $\rightarrow$ L1 loop  $\Rightarrow$  sets $\lambda$",
    RED, fontsize=12)
box(ax, (13.0, 2.0), 5.4, 1.0,
    r"NMDA hypofunction $\Rightarrow$ apical decoupling",
    GRAY, fontsize=12)

# summary strip
box(ax, (8.0, 0.55), 15.2, 1.0,
    r"loop gain  $\lambda = g\,\sigma\sqrt{D}$  rises when PV gain "
    r"$g\uparrow$ and apical discipline fails ($\sigma\uparrow$): "
    "predictions re-enter the ascending stream",
    BLUE, fontsize=13, text_color=NAVY)

fig.tight_layout()
style.save(fig, out("Figure_4.png"))
