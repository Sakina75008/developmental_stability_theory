"""Hopfield illustration of Supplementary S1.

An idealised attractor network (symmetric weights, binary units) used
only to demonstrate the qualitative consequence of dimensionality: as
stored features accumulate, spurious attractors proliferate
super-linearly. It is an illustration, not a cortical model.
"""

import numpy as np


def hopfield_attractors(N=80, p=6, n_starts=400, seed=0, max_iter=200):
    """Count distinct fixed-point attractors reached from random starts.

    Returns (n_total, n_spurious): distinct attractors, and those that are
    not one of the p stored patterns (or their sign-flips).
    """
    rng = np.random.default_rng(seed)
    patterns = rng.choice([-1, 1], size=(p, N))
    W = (patterns.T @ patterns) / N
    np.fill_diagonal(W, 0.0)

    stored = {tuple(x) for x in patterns} | {tuple(-x) for x in patterns}
    found = set()
    for _ in range(n_starts):
        x = rng.choice([-1, 1], size=N)
        for _ in range(max_iter):
            x_new = np.sign(W @ x)
            x_new[x_new == 0] = 1
            if np.array_equal(x_new, x):
                break
            x = x_new
        found.add(tuple(x))
    n_spurious = sum(1 for x in found if x not in stored)
    return len(found), n_spurious
