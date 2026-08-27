"""Figure 5: The composed cascade — a quantitative chain from receptor to
psychosis threshold (Eqs. 18-20, section 3.7).

Cascade: f (L0 molecular) -> kappa, eta (L1 dendritic) -> sigma (L2
coding) -> CMI, dL/da (L3 observable) -> S = 1 - g*sigma*sqrt(D)
(L4 stability). Hierarchy calibrations are illustrative (section 3.7).
"""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import neuron, style
from dst.diagram import arrow, box
from dst.style import BLUE, GOLD, GRAY, GREEN, NAVY, PURPLE, RED

style.use_style()

fs = np.linspace(1.0, 0.15, 200)
loss = 1.0 - fs
kappa, eta = neuron.coefficient_curves(fs)
kappa0, eta0 = neuron.measure_coefficients(1.0)

# Illustrative hierarchy calibrations (sigma_struct, D, g), main text 3.7
HIERARCHIES = [
    ("sighted, high-risk", 2.4, 9.0, 0.12, RED),
    ("sighted, resilient", 2.0, 7.0, 0.115, BLUE),
    ("congenitally blind", 1.2, 1.5, 0.12, GREEN),
]
C = 4.0

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 4, height_ratios=(0.9, 2.0, 2.2), hspace=0.55,
                      wspace=0.35)

# --- cascade strip ---------------------------------------------------------
axs = fig.add_subplot(gs[0, :])
axs.set_xlim(0, 20)
axs.set_ylim(0, 2)
axs.axis("off")
stages = [
    ("L0  MOLECULAR", r"NMDAR function $f$", BLUE),
    ("L1  DENDRITIC", r"$\kappa$,  $\eta$", PURPLE),
    ("L2  CODING", r"$\sigma=\sqrt{\sigma_{struct}^2+(c\eta)^2}$", GOLD),
    ("L3  OBSERVABLE", r"CMI, $dL/da$", GREEN),
    ("L4  STABILITY", r"$S=1-g\sigma\sqrt{D}$", RED),
]
for i, (title, sub, color) in enumerate(stages):
    x = 2 + i * 4
    box(axs, (x, 1.0), 3.4, 1.4, f"{title}\n{sub}", color, fontsize=11)
    if i < 4:
        arrow(axs, (x + 1.75, 1.0), (x + 2.25, 1.0), GRAY, lw=3)
axs.set_title("A quantitative chain from receptor to psychosis", pad=14)

# --- middle row: the four link panels -------------------------------------
ax1 = fig.add_subplot(gs[1, 0])
ax1.plot(loss, kappa / kappa0, color=BLUE, label=r"$\kappa$")
ax1.plot(loss, eta / eta0, color=RED, label=r"$\eta$")
ax1.axhline(1.0, ls=":", color=GRAY)
ax1.set(xlabel=r"NMDAR hypofunction $1-f$", ylabel="relative to intact",
        title="L0$\\to$L1  dendritic\ncoefficients")
ax1.legend()

ax2 = fig.add_subplot(gs[1, 1])
for name, s_struct, D, g, color in HIERARCHIES:
    sig_f = np.array([neuron.sigma_of_f(f, s_struct, C) for f in fs])
    ax2.plot(loss, sig_f, color=color, label=name)
ax2.set(xlabel=r"NMDAR hypofunction $1-f$", ylabel=r"coupling $\sigma$",
        title="L1$\\to$L2  spurious\ncoupling $\\sigma \\propto \\eta$")
ax2.legend(fontsize=9)

ax3 = fig.add_subplot(gs[1, 2])
cmi = kappa / eta                    # contextual modulation falls as eta rises
leak = eta - eta0                    # ascending leak grows with the additive term
ax3.plot(loss, cmi / cmi[0], color=BLUE, label="CMI")
ax3.plot(loss, np.maximum(leak, 0) / np.maximum(leak, 0).max(), color=RED,
         label="leak slope (norm.)")
ax3.set(xlabel=r"NMDAR hypofunction $1-f$", ylabel="relative",
        title="L2$\\to$L3  measurable\nsignatures")
ax3.legend()

ax4 = fig.add_subplot(gs[1, 3])
lk = np.maximum(leak, 0) / np.maximum(leak, 0).max()
ax4.plot(loss, lk, color=RED)
pk = loss[np.argmax(lk)]
ax4.axvline(pk, ls="--", color=NAVY)
ax4.text(pk + 0.03, 0.9, "peak", color=NAVY, fontweight="bold")
ax4.text(pk + 0.03, 0.55, "high dose:\ndissociation,\nnot psychosis",
         color=GRAY, fontsize=10)
ax4.set(xlabel="NMDAR blockade (dose)",
        ylabel="predicted leak (psychotomimetic)",
        title="Retrodiction: sub-anaesthetic\ndose is most psychotomimetic")

# --- bottom row: stability margins + worked example ------------------------
ax5 = fig.add_subplot(gs[2, :2])
label_pos = [(-0.08, 0.42), (0.10, 0.22), (0.0, 0.0)]
for (name, s_struct, D, g, color), (dx, ty) in zip(HIERARCHIES, label_pos):
    S = np.array([neuron.stability_margin(f, s_struct, D, g, C) for f in fs])
    ax5.plot(loss, S, color=color, label=name)
    cross = neuron.crossing_fraction(s_struct, D, g, C)
    if cross is not None:
        ax5.plot(cross, 0, "o", ms=11, color=color, mec="white", zorder=5)
        ax5.annotate(f"{cross:.0%} NMDAR loss", (cross, 0),
                     xytext=(cross + dx, ty), color=color,
                     fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color=color))
ax5.axhline(0, color="k", lw=1.5)
ax5.fill_between(loss, -0.8, 0, color=style.UNSTABLE_FILL, zorder=0)
ax5.set(xlabel=r"NMDAR hypofunction  $1-f$",
        ylabel=r"stability margin  $S=1-g\,\sigma(f)\sqrt{D}$",
        title="L3$\\to$L4   Same molecular lesion: crosses in a high-$D$ "
              "hierarchy,\nnever in a low-$D$ one")
ax5.legend(loc="lower right", fontsize=10)

ax6 = fig.add_subplot(gs[2, 2:])
ax6.axis("off")
ax6.set_title("Worked example: sighted, high-risk hierarchy", color=NAVY)
name, s_struct, D, g, _ = HIERARCHIES[0]
rows = []
for f in (1.0, 0.6, 0.5):
    k, e = neuron.measure_coefficients(f)
    sgm = neuron.sigma_of_f(f, s_struct, C)
    rows.append([f"{f:.2f}", f"{k:.2f}", f"{e:.2f}", f"{sgm:.2f}",
                 f"{k/e:.2f}",
                 f"{neuron.stability_margin(f, s_struct, D, g, C):+.2f}"])
table = ax6.table(
    cellText=list(map(list, zip(*rows))),
    rowLabels=[r"NMDAR function $f$", r"$\kappa$ (dendritic)",
               r"$\eta$ (dendritic)", r"$\sigma$ (coding)",
               r"CMI ($\propto\kappa/\eta$)", r"$S$ (stability)"],
    loc="center", cellLoc="center")
table.scale(0.72, 1.9)
table.set_fontsize(12)
ax6.text(0.5, -0.06, r"$S<0$: psychosis threshold crossed", color=RED,
         transform=ax6.transAxes, ha="center", fontweight="bold")

style.save(fig, out("Figure_5.png"))
