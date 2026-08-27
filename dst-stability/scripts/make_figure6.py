"""Figure 6: The apical hypothesis is identifiable from feasible
measurements (sections 3.7 and S8)."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import cohort, style
from dst.cohort import MECHANISMS
from dst.style import BLUE, GOLD, GRAY, NAVY, PURPLE, RED

style.use_style()
COLORS = {"intact": BLUE, "apical decoupling": RED,
          "PV-gain increase": GOLD, "E/I noise increase": PURPLE}

X, y = cohort.simulate_cohort(n_per=50, seed=11)
preds = cohort.loo_nearest_centroid(X, y)
M = cohort.confusion(y, preds)
acc = (preds == y).mean()
print(f"overall leave-one-out accuracy: {acc:.1%}")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17, 6.2),
                                    gridspec_kw={"width_ratios": (1.2, 0.8, 1.1)})

# --- Panel A: CMI vs leak slope -------------------------------------------
for mi, mech in enumerate(MECHANISMS):
    pts = X[y == mi]
    ax1.scatter(pts[:, 0], pts[:, 1], s=45, color=COLORS[mech], label=mech,
                alpha=0.85, edgecolor="white", linewidth=0.5)
ax1.axhline(0.02, ls=":", color=GRAY)
ax1.axvline(np.percentile(X[:, 0], 45), ls=":", color=GRAY)
ax1.text(0.03, 0.95, r"CMI$\downarrow$ AND leak-slope$\uparrow$", color=RED,
         transform=ax1.transAxes, fontweight="bold")
ax1.set(xlabel="contextual modulation index  CMI\n"
               "(contour integration / surround modulation)",
        ylabel="leak slope  $dL/da$\n"
               "(conditioned-hallucination rate vs cue strength)",
        title="A  Apical decoupling occupies a\nunique quadrant")
ax1.legend(fontsize=10, loc="center right")

# --- Panel B: responsivity separates gain ---------------------------------
means = [X[y == mi][:, 2].mean() for mi in range(4)]
sds = [X[y == mi][:, 2].std() for mi in range(4)]
ax2.bar(range(4), means, yerr=sds, capsize=5,
        color=[COLORS[m] for m in MECHANISMS])
ax2.set_xticks(range(4))
ax2.set_xticklabels(["intact", "apical", "PV\ngain", "E/I\nnoise"])
ax2.text(0.5, 0.92, "CMI & leak are ratios\n$\\Rightarrow$ blind to gain $g$",
         transform=ax2.transAxes, ha="center", color=NAVY, fontsize=11)
ax2.set(ylabel=r"responsivity  $r(b_0, 0)$",
        title="B  Third measure:\nseparates gain")

# --- Panel C: confusion matrix --------------------------------------------
im = ax3.imshow(M, cmap="Blues", vmin=0, vmax=1)
short = ["intact", "apical\ndecoupling", "PV-gain\nincrease",
         "E/I noise\nincrease"]
ax3.set_xticks(range(4), short, fontsize=10)
ax3.set_yticks(range(4), short, fontsize=10)
for i in range(4):
    for j in range(4):
        ax3.text(j, i, f"{M[i, j]:.0%}", ha="center", va="center",
                 color="white" if M[i, j] > 0.5 else NAVY,
                 fontweight="bold")
ax3.set(xlabel="recovered mechanism", ylabel="true mechanism",
        title=f"C  Model recovery: {acc:.0%} accuracy\n"
              "(leave-one-out, simulated subjects)")
ax3.grid(False)

fig.suptitle("Making the apical hypothesis decisively testable: "
             "three measurements that identify the mechanism",
             fontsize=15, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
style.save(fig, out("Figure_6.png"))
