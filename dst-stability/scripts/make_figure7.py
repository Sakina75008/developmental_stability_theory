"""Figure 7: One mechanism, three courses (Eq. 21, section 3.8).

Identical gain fluctuations; only the plastic ratchet rate rho differs.
"""

import matplotlib.pyplot as plt

from _common import out
from dst import course, style
from dst.style import GOLD, GREEN, NAVY, RED

style.use_style()

CASES = [(0.0, GREEN, "no plastic ratchet", "remitting"),
         (1.5, GOLD, "mild ratchet", "episodic relapsing"),
         (6.0, RED, "strong ratchet", "progressive decline")]
SEED = 8

fig, axes = plt.subplots(1, 3, figsize=(17, 6), sharey=True)
for ax, (rho, color, tag, name) in zip(axes, CASES):
    t, S, sigma, baseline = course.simulate_course(rho, seed=SEED)
    n_ep = course.count_episodes(t, S)
    for a, b in course.episode_spans(t, S):
        ax.axvspan(a, b, color=color, alpha=0.18)
    ax.plot(t, S, color=color, lw=1.4)
    ax.plot(t, baseline, "--", color=NAVY, lw=2,
            label="baseline margin (at mean gain)")
    ax.axhline(0, color="k", lw=1.4)
    ax.fill_between(t, -1.3, 0, color=style.UNSTABLE_FILL, zorder=0)
    ax.set_title(f"{name}   ({n_ep} episodes)")
    ax.text(0.04, 0.93, rf"$\sigma$: {sigma[0]:.2f} $\to$ {sigma[-1]:.2f}",
            transform=ax.transAxes, color=NAVY, fontweight="bold")
    ax.text(0.04, 0.85, rf"$\rho$ = {rho}   {tag}", transform=ax.transAxes,
            color=color, fontweight="bold")
    ax.set(xlabel="years from first episode", ylim=(-1.3, 0.85))
axes[0].set_ylabel(r"stability margin  $S(t)=1-g(t)\,\sigma(t)\sqrt{D}$")
axes[1].legend(loc="lower left", fontsize=10)

fig.suptitle("Same fluctuating gain, three courses: what differs is how "
             r"much each episode raises $\sigma$", fontsize=15,
             fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.94))
style.save(fig, out("Figure_7.png"))
