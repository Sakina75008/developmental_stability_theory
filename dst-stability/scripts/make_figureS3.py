"""Figure S3: The biophysical bridge (model-conditional): NMDAR
hypofunction yields kappa down, eta up (Supplementary S3-S4)."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import neuron, style
from dst.neuron import DEFAULT, NeuronParams, somatic_drive
from dst.style import BLUE, GRAY, GREEN, PURPLE, RED

style.use_style()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16.5, 6.2))

# --- Panel A: apical drive alone vs with basal drive ----------------------
a = np.linspace(0, 2.6, 300)
ax1.plot(a, somatic_drive(0.0, a, 1.0), color=BLUE,
         label=r"apical alone ($b=0$)")
ax1.plot(a, somatic_drive(1.2, a, 1.0), color=GREEN,
         label=r"apical + basal ($b=1.2$)")
ax1.plot(a, somatic_drive(0.0, a, 0.5), "--", color=RED,
         label=r"apical alone, NMDA$\downarrow$")
ax1.set(xlabel=r"apical (context) drive $a$", ylabel="somatic depolarisation",
        title="A  Intact: context needs coincidence.\n"
              "Hypofunction: context drives alone")
ax1.legend(fontsize=11)

# --- Panel B: kappa falls, eta rises --------------------------------------
fs = np.linspace(1.0, 0.15, 200)
loss = 1.0 - fs
kappa, eta = neuron.coefficient_curves(fs)
k0, e0 = neuron.measure_coefficients(1.0)
ax2.plot(loss, kappa / k0, color=BLUE, label=r"$\kappa$  (multiplicative)")
ax2.plot(loss, eta / e0, color=RED, label=r"$\eta$  (additive leak)")
ax2.axhline(1.0, ls=":", color=GRAY)
ax2.set(xlabel=r"NMDAR hypofunction $1-f$",
        ylabel="coefficient (relative to intact)",
        title="B  One lesion, opposite effects:\n"
              r"$\kappa\downarrow$  and  $\eta\uparrow$")
ax2.legend(fontsize=11)

# --- Panel C: dissociation of the two sites --------------------------------
# pyramidal NMDA loss alone: A, beta reduced but no disinhibition (dtheta=0)
p_pyr_only = NeuronParams(**{**DEFAULT.__dict__, "dtheta": 0.0})
_, eta_both = neuron.coefficient_curves(fs)
_, eta_pyr = neuron.coefficient_curves(fs, p_pyr_only)
ax3.plot(loss, eta_both / e0, color=RED, label="both sites (pyramidal + SST)")
ax3.plot(loss, eta_pyr / eta_pyr[0], "--", color=PURPLE, lw=2.8,
         label="pyramidal NMDA only")
ax3.axhline(1.0, ls=":", color=GRAY)
ax3.set(xlabel=r"NMDAR hypofunction $1-f$",
        ylabel=r"additive leak $\eta$ (relative)",
        title="C  The leak requires dendritic\n"
              "disinhibition, not pyramidal loss alone")
ax3.legend(fontsize=11)

fig.suptitle("Within this reduced model, NMDAR hypofunction yields the "
             r"multiplicative $\to$ additive shift", fontsize=15,
             fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.93))
style.save(fig, out("Figure_S3.png"))
