"""Identifiability of the apical hypothesis from feasible measurements.

Implements Supplementary Eq. (S8) and sections S6-S8: the transfer
function r = phi(g[b(1 + kappa*a)] + eta*a) with phi a power law, the
three observables (CMI, ascending-leak slope dL/da, absolute
responsivity), simulated cohorts under four mechanisms, leave-one-out
nearest-centroid recovery, and mixture estimation in a mixed cohort.
"""

import numpy as np

MECHANISMS = ("intact", "apical decoupling", "PV-gain increase",
              "E/I noise increase")


def phi(x, n=2.0):
    """Power-law transfer phi(x) = [x]_+^n."""
    return np.maximum(x, 0.0) ** n


def rate(b, a, mech="intact", g=1.0, kappa=1.0, eta=0.35, noise=0.0,
         rng=None, n=2.0):
    """Firing rate under one of the four candidate mechanisms (S8)."""
    rng = np.random.default_rng(rng)
    if mech == "intact":
        drive = g * b * (1 + kappa * a)
    elif mech == "apical decoupling":
        drive = g * b * (1 + 0.4 * kappa * a) + eta * a
    elif mech == "PV-gain increase":
        drive = 2.2 * g * b * (1 + kappa * a)
    elif mech == "E/I noise increase":
        # zero-mean background fluctuation: raises variability, leaves the
        # mean observables near-intact => confusable with intact (S8)
        drive = g * b * (1 + kappa * a) + noise
    else:
        raise ValueError(mech)
    return phi(drive, n)


def observables(mech, rng, n_trials=40):
    """(CMI, leak slope dL/da, responsivity) for one simulated participant.

    CMI(b,a) = (r(b,a) - r(b,0)) / r(b,0); L(a) = r(0,a) / r(b0,0) (Eq. S8).
    Trial noise is multiplicative on each measured rate.
    """
    rng = np.random.default_rng(rng)
    b0, a1 = 1.0, 1.0
    kappa = rng.normal(1.0, 0.08)
    g = rng.normal(1.0, 0.05)
    # E/I severity is heterogeneous across participants; mild cases sit near
    # the intact cluster, which confines residual classification error to
    # the intact-versus-noise boundary (S8)
    sev = abs(rng.normal(0.25, 0.18)) if mech == "E/I noise increase" else 0.0

    def meas(b, a):
        if sev:
            ei = sev * (0.8 + rng.standard_normal(n_trials))
        else:
            ei = np.zeros(n_trials)
        base = np.array([rate(b, a, mech, g=g, kappa=kappa, noise=e)
                         for e in ei])
        trials = base * (1 + 0.06 * rng.standard_normal(n_trials))
        return trials.mean()

    r_b0 = meas(b0, 0.0)
    cmi = (meas(b0, a1) - r_b0) / r_b0
    a_grid = np.linspace(0.0, 1.0, 5)
    leaks = np.array([meas(0.0, a) for a in a_grid]) / r_b0
    slope = np.polyfit(a_grid, leaks, 1)[0]
    return cmi, slope, r_b0


def simulate_cohort(n_per=50, seed=0):
    """Simulate n_per participants per mechanism; return features and labels."""
    rng = np.random.default_rng(seed)
    X, y = [], []
    for mi, mech in enumerate(MECHANISMS):
        for _ in range(n_per):
            X.append(observables(mech, rng))
            y.append(mi)
    return np.array(X), np.array(y)


def loo_nearest_centroid(X, y):
    """Leave-one-out nearest-centroid classification; returns predictions."""
    Xz = (X - X.mean(0)) / X.std(0)
    preds = np.empty_like(y)
    for i in range(len(y)):
        mask = np.arange(len(y)) != i
        cents = np.array([Xz[mask & (y == k)].mean(0)
                          for k in range(len(MECHANISMS))])
        preds[i] = np.argmin(((Xz[i] - cents) ** 2).sum(1))
    return preds


def confusion(y, preds, K=4):
    M = np.zeros((K, K))
    for t, p in zip(y, preds):
        M[t, p] += 1
    return M / M.sum(1, keepdims=True)


def mixture_recovery(true_props=(0.15, 0.40, 0.25, 0.20), N=200,
                     n_rep=200, seed=0):
    """Recover mechanism proportions in a mixed cohort (S6, Figure S5B)."""
    rng = np.random.default_rng(seed)
    Xr, yr = simulate_cohort(n_per=60, seed=seed + 1)  # reference centroids
    mu, sd = Xr.mean(0), Xr.std(0)
    cents = np.array([((Xr - mu) / sd)[yr == k].mean(0) for k in range(4)])
    recovered = np.zeros((n_rep, 4))
    for r in range(n_rep):
        counts = rng.multinomial(N, true_props)
        feats = []
        for k, n_k in enumerate(counts):
            for _ in range(n_k):
                feats.append(observables(MECHANISMS[k], rng))
        Z = (np.array(feats) - mu) / sd
        lab = np.argmin(((Z[:, None, :] - cents[None]) ** 2).sum(2), axis=1)
        recovered[r] = np.bincount(lab, minlength=4) / N
    return recovered
