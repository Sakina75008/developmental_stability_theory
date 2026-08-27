"""Figure S6: Apical integration formalised, and its unique signature
(Supplementary S7; Eqs. S1-S2, S8)."""

import matplotlib.pyplot as plt
import numpy as np

from _common import out
from dst import style
from dst.style import BLUE, GOLD, PURPLE, RED

style.use_style()

G, KAPPA, ETA, N = 1.0, 1.0, 0.35, 2.0
rng = np.random.default_rng(4)


def phi(x):
    return np.maximum(x, 0.0) ** N


def r_intact(b, a, g=G):
    return phi(g * b * (1 + KAPPA * a))                     # Eq. (S1)


def r_decoupled(b, a, g=G, kp=0.4 * KAPPA, eta=ETA):
    return phi(g * (b * (1 + kp * a)) + eta * a)            # Eq. (S2)


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16.5, 6.2))

# --- Panel A: input-output curves ------------------------------------------
b = np.linspace(0, 2, 300)
ax1.plot(b, r_intact(b, 0), color=BLUE, label=r"intact, context $a=0$")
ax1.plot(b, r_decoupled(b, 0), color=RED, label=r"decoupled, $a=0$")
ax1.plot(b, r_intact(b, 1), "--", color=BLUE, label=r"intact, context $a=1$")
ax1.plot(b, r_decoupled(b, 1), "--", color=RED, label=r"decoupled, $a=1$")
ax1.annotate("no evidence,\nbut output > 0", (0.02, r_decoupled(0, 1)),
             xytext=(0.5, 5.5), color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED))
ax1.set(xlabel=r"feedforward (basal) drive $b$", ylabel=r"output $r$",
        title="A  Context amplifies drive —\nuntil apical coupling fails")
ax1.legend(fontsize=10)

# --- Panel B: CMI gain-invariance ------------------------------------------
a = np.linspace(0, 2, 300)
b0 = 1.0


def cmi(r_fun, a, **kw):
    return (r_fun(b0, a, **kw) - r_fun(b0, 0, **kw)) / r_fun(b0, 0, **kw)


ax2.plot(a, cmi(r_intact, a), color=BLUE, label="intact")
ax2.plot(a, cmi(r_intact, a, g=2.2 * G), ":", color=GOLD, lw=4,
         label="PV-gain lesion (identical!)")
ax2.plot(a, cmi(r_decoupled, a), color=RED, label="apical decoupling")
ax2.set(xlabel=r"apical (context) drive $a$",
        ylabel="contextual modulation index  CMI",
        title="B  CMI is invariant to gain,\nbut falls with apical decoupling")
ax2.legend(fontsize=11)

# --- Panel C: ascending leak -----------------------------------------------
leak_intact = r_intact(np.zeros_like(a), a) / r_intact(b0, 0)
leak_dec = r_decoupled(np.zeros_like(a), a) / r_decoupled(b0, 0)
noise_leak = 0.18 + 0.008 * rng.standard_normal(a.size)
ax3.plot(a, leak_intact, color=BLUE, lw=3, label="intact  (leak = 0)")
ax3.plot(a, leak_dec, color=RED, label="apical decoupling")
ax3.plot(a, noise_leak, "--", color=PURPLE, lw=2.5,
         label=r"E/I noise (flat in $a$)")
ax3.set(xlabel=r"apical (context) drive $a$",
        ylabel=r"ascending leak  $r(0,a)/r(b_0,0)$",
        title="C  Leak rises with context only\nunder apical decoupling")
ax3.legend(fontsize=11)

fig.suptitle("Apical integration formalised: intact coupling is "
             "multiplicative (context modulates); decoupling makes it "
             "additive (context drives)", fontsize=14, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.93))
style.save(fig, out("Figure_S6.png"))
