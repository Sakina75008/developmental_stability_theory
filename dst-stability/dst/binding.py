"""Temporal binding windows under Bayesian causal inference.

Implements Eq. (15): p(C=1 | dt) proportional to exp(-dt^2 / 2 sigma_t^2) * pi,
so the optimal binding half-width scales as w* proportional to sigma_t.
"""

import numpy as np


def posterior_common_cause(dt, sigma_t, prior=0.5, seg_scale=200.0):
    """Posterior probability of a common cause at cross-modal offset dt (ms).

    The common-cause likelihood is Gaussian in dt with scale sigma_t; the
    segregation alternative is a broad uniform over +/- seg_scale.
    """
    like_common = np.exp(-dt**2 / (2 * sigma_t**2)) / (
        np.sqrt(2 * np.pi) * sigma_t
    )
    like_seg = np.ones_like(np.asarray(dt, dtype=float)) / (2 * seg_scale)
    num = like_common * prior
    return num / (num + like_seg * (1 - prior))


def optimal_width(sigma_t, prior=0.5, seg_scale=200.0):
    """Half-width w* at which the posterior crosses 0.5 (w* ~ sigma_t)."""
    inside = 2 * np.log(2 * seg_scale * prior /
                        ((1 - prior) * np.sqrt(2 * np.pi) * sigma_t))
    return sigma_t * np.sqrt(np.maximum(inside, 0.0))
