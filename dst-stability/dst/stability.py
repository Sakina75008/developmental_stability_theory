"""Random-matrix stability of the linearised hierarchy.

Implements Eqs. (3)-(6): J = -I + gW with Var(W_jk) = sigma^2, whose
leading eigenvalue sits at approximately -1 + g*sigma*sqrt(D) (circular
law, bulk regime), giving the stability criterion g*sigma*sqrt(D) < 1.
"""

import numpy as np


def sample_jacobian(D, g, sigma=1.0, rng=None):
    """Sample J = -I + gW with iid Gaussian W, Var(W_jk) = sigma^2 (Eq. 3)."""
    rng = np.random.default_rng(rng)
    W = rng.normal(0.0, sigma, size=(D, D))
    return -np.eye(D) + g * W


def max_re_lambda(D, g, sigma=1.0, rng=None):
    """Leading real part of the spectrum of a sampled J (Eq. 5)."""
    J = sample_jacobian(D, g, sigma, rng)
    return np.linalg.eigvals(J).real.max()


def n_unstable(D, g, sigma=1.0, rng=None):
    """Number of self-amplifying directions (Re lambda > 0)."""
    J = sample_jacobian(D, g, sigma, rng)
    return int((np.linalg.eigvals(J).real > 0).sum())


def stability_grid(Ds, gs, sigma=1.0, n_rep=3, seed=0):
    """max Re lambda averaged over n_rep samples on a (g, D) grid."""
    rng = np.random.default_rng(seed)
    out = np.zeros((len(gs), len(Ds)))
    for i, g in enumerate(gs):
        for j, D in enumerate(Ds):
            out[i, j] = np.mean(
                [max_re_lambda(int(D), g, sigma, rng) for _ in range(n_rep)]
            )
    return out


def critical_D(g, sigma=1.0):
    """Critical dimensionality D_c = 1/(g*sigma)^2 (below Eq. 6)."""
    return 1.0 / (g * sigma) ** 2
