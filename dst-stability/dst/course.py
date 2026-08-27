"""Clinical course: gain fluctuation plus the plasticity ratchet.

Implements Eq. (21): g(t) is a slow mean-reverting (Ornstein-Uhlenbeck)
process; instability drives a saturating ratchet on the structural
coupling,

    dsigma/dt = rho * max(0, -S(t)) * (1 - sigma / sigma_max),

with S(t) = 1 - g(t) * sigma(t) * sqrt(D).
"""

import numpy as np


def simulate_course(rho, years=30.0, dt=0.01, D=9.0, sigma0=2.55,
                    sigma_max=4.5, g_mean=None, tau=2.0, noise=0.033,
                    seed=8):
    """Simulate one illness course; identical seed => identical gain noise.

    Returns (t, S, sigma, baseline_margin) where baseline_margin is the
    margin evaluated at the mean gain (the dashed reference line).
    """
    sqrtD = np.sqrt(D)
    if g_mean is None:
        g_mean = 0.75 / (sigma0 * sqrtD)  # baseline margin S = +0.25
    n = int(years / dt)
    rng = np.random.default_rng(seed)
    shocks = rng.standard_normal(n)  # same across rho values for fixed seed
    t = np.arange(n) * dt
    g = np.empty(n)
    sigma = np.empty(n)
    S = np.empty(n)
    g[0], sigma[0] = g_mean, sigma0
    for i in range(n):
        if i > 0:
            g[i] = (g[i - 1] + (g_mean - g[i - 1]) * dt / tau
                    + noise * np.sqrt(dt) * shocks[i])
            sigma[i] = sigma[i - 1] + dt * rho * max(0.0, -S[i - 1]) * (
                1.0 - sigma[i - 1] / sigma_max)
        S[i] = 1.0 - g[i] * sigma[i] * sqrtD
    baseline = 1.0 - g_mean * sigma * sqrtD
    return t, S, sigma, baseline


def count_episodes(t, S, min_gap=0.6):
    """Number of distinct S < 0 excursions separated by at least min_gap."""
    below = S < 0
    n_ep, in_ep, last_end = 0, False, -np.inf
    for i in range(len(t)):
        if below[i] and not in_ep:
            if t[i] - last_end > min_gap:
                n_ep += 1
            in_ep = True
        elif not below[i] and in_ep:
            in_ep, last_end = False, t[i]
    return n_ep


def episode_spans(t, S):
    """(start, end) times of S < 0 excursions, for shading."""
    spans, start = [], None
    for i in range(len(t)):
        if S[i] < 0 and start is None:
            start = t[i]
        elif S[i] >= 0 and start is not None:
            spans.append((start, t[i]))
            start = None
    if start is not None:
        spans.append((start, t[-1]))
    return spans
