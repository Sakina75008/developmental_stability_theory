"""Figure S4: The coefficient changes are structural within this model
class — robustness across 10,000 physiological parameter sets
(Supplementary S5)."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import neuron, style
from dst.neuron import NeuronParams, sig
from dst.style import BLUE, GOLD, NAVY, PURPLE, RED

style.use_style()
N_SETS = 10_000
rng = np.random.default_rng(42)
fs = np.linspace(0.99, 0.18, 60)

kappa_falls = eta_rises = eta_nonmono = 0
pred_gate, obs_gate, f_at_peak = [], [], []

for _ in range(N_SETS):
    p = NeuronParams(
        A=rng.uniform(1.5, 5.0),
        beta=rng.uniform(0.5, 1.5),
        theta=rng.uniform(1.2, 2.8),
        s=rng.uniform(0.15, 0.5),
        eta0=rng.uniform(0.02, 0.25),
        dtheta=rng.uniform(0.8, 2.6),
        b_probe=rng.uniform(0.8, 1.2),
        a_probe=rng.uniform(0.8, 1.2),
    )
    kappa, eta = neuron.coefficient_curves(fs, p)
    if kappa[-1] < kappa[0]:
        kappa_falls += 1
    if eta.max() > eta[0]:
        eta_rises += 1
    i_pk = int(np.argmax(eta))
    interior = 0 < i_pk < len(fs) - 1
    if interior:
        eta_nonmono += 1
        f_pk = fs[i_pk]
        f_at_peak.append(f_pk)
        # analytic peak condition (Eq. S6): sig(u*) = 1 - s/(f*dtheta)
        pred = neuron.predicted_gate_at_peak(f_pk, p)
        if 0 < pred < 1:
            theta_f = p.theta - p.dtheta * (1 - f_pk)
            obs = sig((p.a_probe - theta_f) / p.s)
            pred_gate.append(pred)
            obs_gate.append(obs)

pred_gate, obs_gate = np.array(pred_gate), np.array(obs_gate)
keep = rng.choice(len(pred_gate), size=min(600, len(pred_gate)),
                  replace=False)
r = np.corrcoef(pred_gate, obs_gate)[0, 1]
print(f"kappa falls: {kappa_falls/N_SETS:.1%}  eta rises: "
      f"{eta_rises/N_SETS:.1%}  eta non-monotonic: {eta_nonmono/N_SETS:.1%}"
      f"  r(pred, obs) = {r:.3f}  median f at peak = "
      f"{np.median(f_at_peak):.2f}")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16.5, 6))

ax1.scatter(pred_gate[keep], obs_gate[keep], s=22, alpha=0.45, color=BLUE)
lim = np.linspace(0, 1, 10)
ax1.plot(lim, lim, "--", color=RED, lw=2.5)
ax1.text(0.05, 0.92, f"r = {r:.3f}  (n={len(keep)})",
         transform=ax1.transAxes, color=NAVY, fontweight="bold")
ax1.set(xlabel=r"predicted  $\varsigma(u^*) = 1 - s/(f\Delta\theta)$",
        ylabel=r"observed  $\varsigma(u^*)$ at numerical peak",
        xlim=(0, 1), ylim=(0, 1),
        title="A  Analytic peak condition holds\nacross parameter draws")

fracs = [kappa_falls / N_SETS, eta_rises / N_SETS, eta_nonmono / N_SETS]
bars = ax2.bar(range(3), [100 * f for f in fracs],
               color=[BLUE, RED, PURPLE])
for b, f in zip(bars, fracs):
    ax2.text(b.get_x() + b.get_width() / 2, 100 * f + 1, f"{100*f:.1f}%",
             ha="center", fontweight="bold", color=NAVY)
ax2.set_xticks(range(3),
               [r"$\kappa$ falls", r"$\eta$ rises", r"$\eta$ non-monotonic"])
ax2.set(ylabel=f"% of {N_SETS} parameter sets", ylim=(0, 112),
        title=f"B  Robustness across {N_SETS:,}\nphysiological parameter sets")

ax3.hist(f_at_peak, bins=24, color=GOLD)
med = np.median(f_at_peak)
ax3.axvline(med, ls="--", color=RED, lw=2.5)
ax3.text(med + 0.02, ax3.get_ylim()[1] * 0.92, f"median $f$={med:.2f}",
         color=RED, fontweight="bold")
ax3.set(xlabel=r"NMDAR function $f$ at maximal leak", ylabel="count",
        title="C  Predicted optimum: leak is maximal\nat MODERATE hypofunction")

fig.suptitle("The result is structural, not tuned: analytic peak condition "
             f"and {N_SETS:,}-set robustness sweep", fontsize=15,
             fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.93))
style.save(fig, out("Figure_S4.png"))
