"""Circular inference in belief space.

Implements Eqs. (10)-(11): L_{t+1} = L_s + lambda * L_t, with fixed point
L* = L_s / (1 - lambda), diverging exactly at the loop gain lambda = 1,
where lambda = g * sigma * sqrt(D).
"""

import numpy as np


def belief_recursion(L_s, lam, n_steps=25):
    """Trajectory of belief log-odds under recurrent echoing (Eq. 10)."""
    L = np.zeros(n_steps + 1)
    for t in range(n_steps):
        L[t + 1] = L_s + lam * L[t]
    return L


def equilibrium_certainty(L_s, lam):
    """Fixed-point certainty L* = L_s / (1 - lambda) (Eq. 10)."""
    lam = np.asarray(lam, dtype=float)
    return np.where(lam < 1.0, L_s / (1.0 - lam), np.inf)
