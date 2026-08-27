"""Figure 8: Developmental trajectories through the stability plane
(sections 3.4 and 3.8). Trajectories are illustrative developmental
paths g(t), sigma*sqrt(D)(t); crosses mark g*sigma*sqrt(D) = 1.
"""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import style
from dst.style import (BLUE, GOLD, GREEN, NAVY, PURPLE, RED, STABLE_FILL,
                       UNSTABLE_FILL)

style.use_style()


def g_rise(t, g0, g1, t50=0.55, k=10):
    """Sigmoidal adolescent rise in gain (puberty)."""
    return g0 + (g1 - g0) / (1 + np.exp(-k * (t - t50)))


def crossing(g, s):
    """First index where g * s crosses 1 (None if never)."""
    prod = g * s
    idx = np.argmax(prod >= 1.0)
    return idx if prod[idx] >= 1.0 else None


def draw_boundary(ax):
    gg = np.linspace(0.06, 0.95, 300)
    ax.plot(gg, 1.0 / gg, "k", lw=3)
    ax.fill_between(gg, 1.0 / gg, 12, color=UNSTABLE_FILL, zorder=0)
    ax.fill_between(gg, 0, 1.0 / gg, color=STABLE_FILL, zorder=0)
    ax.set(xlim=(0.06, 0.95), ylim=(0.5, 12),
           xlabel=r"gain $g$  (dopaminergic / state)")


t = np.linspace(0, 1, 400)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.5), sharey=True)

# --- Panel A: age of onset -------------------------------------------------
draw_boundary(ax1)
paths_A = [
    ("resilient — never crosses", GREEN,
     g_rise(t, 0.15, 0.42), np.full_like(t, 2.0)),
    ("typical onset (adolescence)", BLUE,
     g_rise(t, 0.15, 0.42), 5.0 + 1.2 * t),
    ("childhood onset — thin margin", RED,
     g_rise(t, 0.30, 0.13, t50=0.4, k=-6), 9.4 - 0.9 * t),
]
for label, color, g_t, s_t in paths_A:
    ax1.plot(g_t, s_t, color=color, lw=3.2, label=label)
    ax1.plot(g_t[0], s_t[0], "o", color=color, ms=8)
    ci = crossing(g_t, s_t)
    if ci is not None:
        ax1.plot(g_t[ci], s_t[ci], "X", ms=16, color=color, mec="white",
                 mew=1.5, zorder=6)
ax1.text(0.42, 3.2, r"X = crossing ($g\sigma\sqrt{D}=1$)", color=NAVY,
         fontweight="bold")
ax1.set_ylabel(r"structural coupling  $\sigma\sqrt{D}$")
ax1.set_title("A  Age of onset: baseline margin sets\nWHEN the trajectory "
              "crosses")
ax1.legend(loc="upper right", fontsize=11)

# --- Panel B: autism-psychosis co-occurrence ------------------------------
draw_boundary(ax2)
# autism only: high gain, uniformly low coupling — never crosses
g_aut = g_rise(t, 0.30, 0.82)
ax2.plot(g_aut, np.full_like(t, 1.1), color=GOLD, lw=3.2,
         label=r"autism only — low $\sigma_S,\sigma_C$")
ax2.plot(g_aut[0], 1.1, "o", color=GOLD, ms=8)
# autism -> psychosis: split sigma-vector, sigma_T / sigma_Sigma rise with age
g_ap = g_rise(t, 0.30, 0.74)
s_ap = 1.4 + 4.2 * t**1.6
ax2.plot(g_ap, s_ap, color=PURPLE, lw=3.2,
         label=r"autism $\to$ psychosis — split $\sigma$")
ax2.plot(g_ap[0], s_ap[0], "o", color=PURPLE, ms=8)
ci = crossing(g_ap, s_ap)
if ci is not None:
    ax2.plot(g_ap[ci], s_ap[ci], "X", ms=16, color=PURPLE, mec="white",
             mew=1.5, zorder=6)
# typical schizophrenia for reference
g_sz = g_rise(t, 0.15, 0.42)
s_sz = 5.0 + 1.2 * t
ax2.plot(g_sz, s_sz, color=BLUE, lw=3.2, label="typical schizophrenia")
ci = crossing(g_sz, s_sz)
if ci is not None:
    ax2.plot(g_sz[ci], s_sz[ci], "X", ms=16, color=BLUE, mec="white",
             mew=1.5, zorder=6)
ax2.annotate(r"$\sigma_T,\sigma_\Sigma$ rise with age"
             "\nwhile $\\sigma_S,\\sigma_C$ stay low",
             (g_ap[240], s_ap[240]), xytext=(0.58, 8.2), color=PURPLE,
             fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=PURPLE))
ax2.text(0.35, 0.62, "stays stable:\nautistic, illusion-resistant",
         color=GOLD, fontweight="bold", fontsize=11)
ax2.set_title(r"B  Why both can co-occur: split $\sigma$-vector"
              "\nplus a later rise in gain")
ax2.legend(loc="upper left", fontsize=11)

fig.suptitle("Developmental trajectories through the stability plane",
             fontsize=16, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
style.save(fig, out("Figure_8.png"))
