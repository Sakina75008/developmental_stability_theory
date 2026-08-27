"""Figure S5: Two refinements — the leak is conditional, and
heterogeneity is measurable (Eq. 17; Supplementary S6)."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import cohort, style
from dst.style import BLUE, GOLD, GRAY, NAVY, PURPLE, RED, STABLE_FILL

style.use_style()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16.5, 6.2))

# --- Panel A: the conjunction condition eta * a > theta_s ------------------
theta_s = 0.55
eta = np.linspace(0.01, 1.0, 300)
a_crit = theta_s / eta
ax1.plot(eta, a_crit, "k", lw=3)
ax1.fill_between(eta, a_crit, 3, color="#f2b28c", zorder=0)
ax1.fill_between(eta, 0, a_crit, color=STABLE_FILL, zorder=0)
ax1.annotate(r"$a = \theta_s/\eta$", (0.35, theta_s / 0.35),
             xytext=(0.42, 2.5), color=NAVY, fontsize=13,
             arrowprops=dict(arrowstyle="->", color=NAVY))
ax1.text(0.62, 2.15, "LEAK\n(false percept)", color=RED, fontsize=14,
         fontweight="bold", ha="center")
ax1.text(0.22, 0.35, "no leak:\nsub-threshold", color=GRAY, fontsize=12)
ax1.set(xlabel=r"additive leak coefficient $\eta$  (decoupling)",
        ylabel=r"apical drive $a$  (strength of expectation)",
        xlim=(0, 1), ylim=(0, 3),
        title="A  Leak needs BOTH:\n" r"$\eta\,a > \theta_s$")

# --- Panel B: mixture recovery ---------------------------------------------
true_props = (0.15, 0.40, 0.25, 0.20)
rec = cohort.mixture_recovery(true_props, N=200, n_rep=60, seed=5)
m, sd = rec.mean(0), rec.std(0)
print("true:", true_props, " recovered:", np.round(m, 3))
x = np.arange(4)
w = 0.38
colors = [BLUE, RED, GOLD, PURPLE]
for i in range(4):
    ax2.bar(x[i] - w / 2, true_props[i], w, color=colors[i], alpha=0.45)
    ax2.bar(x[i] + w / 2, m[i], w, yerr=sd[i], capsize=4, color=colors[i])
ax2.bar(0, 0, color=GRAY, alpha=0.45, label="true proportion")
ax2.bar(0, 0, color=GRAY, label="recovered")
ax2.set_xticks(x, ["intact", "apical", "gain", "noise"])
ax2.set(ylabel="proportion of cohort", ylim=(0, 0.62),
        title="B  Heterogeneity is recoverable:\nmechanism mix in a mixed "
              "cohort")
ax2.legend(fontsize=11)

# --- Panel C: N needed to stratify to +/-10% -------------------------------
Ns = np.array([30, 50, 100, 200, 400, 800])
hw = []
rng = np.random.default_rng(9)
for N in Ns:
    rec_N = cohort.mixture_recovery(true_props, N=int(N), n_rep=30,
                                    seed=int(N))
    hw.append(1.96 * rec_N[:, 1].std())
ax3.semilogx(Ns, hw, "-o", color=RED, ms=8)
ax3.axhline(0.10, ls="--", color=GRAY, lw=2)
ax3.text(120, 0.104, r"target $\pm$10%", color=NAVY, fontweight="bold")
ax3.annotate(r"$N \approx 100$", (100, np.interp(100, Ns, hw)),
             xytext=(140, 0.16), color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED))
ax3.set(xlabel="cohort size $N$",
        ylabel="95% CI half-width on\napical-subtype fraction",
        title="C  Study design: $N$ needed to\nstratify to $\\pm$10%")

fig.suptitle("Two refinements: the leak is conditional, and heterogeneity "
             "becomes a measurable mixture", fontsize=15, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.93))
style.save(fig, out("Figure_S5.png"))
