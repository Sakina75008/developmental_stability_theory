"""The reduced two-point (two-compartment) pyramidal neuron.

Implements Supplementary Eqs. (S3)-(S7) and the composed cascade of
main-text Eqs. (18)-(20):

  D(b, a) = b + eta0*a + A * sig((a - theta + beta*b) / s),   (S3)

with NMDAR hypofunction of severity 1 - f applied at two sites (S4):

  A -> f*A,  beta -> f*beta          (pyramidal apical NMDA)
  theta -> theta - dtheta*(1 - f)    (SST hypofunction => disinhibition)

kappa and eta are *measured* from the transfer function by the 2x2
factorial decomposition of Eq. (S5); they are never assumed.

NOTE ON PARAMETERS: the constants below are illustrative calibrations
(cf. main text section 3.7, "We are careful about status"), chosen so an
intact hierarchy sits in the stable regime and so the worked-example
numbers come out in the reported ballpark. They are not fits to data.
"""

from dataclasses import dataclass, replace

import numpy as np


def sig(z):
    return 1.0 / (1.0 + np.exp(-z))


@dataclass
class NeuronParams:
    """Illustrative calibration, chosen so the measured coefficients hit the
    worked-example values of main-text section 3.7: kappa = 1.66, eta = 0.21
    at f = 1 and kappa = 0.25, eta = 0.74 at f = 0.5."""

    A: float = 2.877      # dendritic-spike amplitude (apical NMDA conductance)
    beta: float = 1.185   # bAP priming efficacy (NMDA-dependent)
    theta: float = 1.699  # ignition threshold (SST -> L1 dendritic inhibition)
    s: float = 0.234      # gate sharpness
    eta0: float = 0.134   # small passive apical leak
    dtheta: float = 1.513 # disinhibition magnitude per unit hypofunction
    b_probe: float = 1.0  # factorial probe level b*
    a_probe: float = 1.0  # factorial probe level a*


DEFAULT = NeuronParams()


def somatic_drive(b, a, f=1.0, p: NeuronParams = DEFAULT):
    """D(b, a) of Eq. (S3) under hypofunction severity 1 - f (Eq. S4)."""
    A, beta, theta = f * p.A, f * p.beta, p.theta - p.dtheta * (1.0 - f)
    return b + p.eta0 * a + A * sig((a - theta + beta * b) / p.s)


def measure_coefficients(f=1.0, p: NeuronParams = DEFAULT):
    """(kappa, eta) measured by the factorial decomposition of Eq. (S5)."""
    b, a = p.b_probe, p.a_probe
    D00 = somatic_drive(0, 0, f, p)
    Db0 = somatic_drive(b, 0, f, p)
    D0a = somatic_drive(0, a, f, p)
    Dba = somatic_drive(b, a, f, p)
    c1 = (Db0 - D00) / b
    eta = ((D0a - D00) / a) / c1
    kappa = (((Dba - Db0) - (D0a - D00)) / (a * b)) / c1
    return kappa, eta


def coefficient_curves(fs, p: NeuronParams = DEFAULT):
    """kappa(f) and eta(f) over an array of NMDAR-function values."""
    ks, es = zip(*(measure_coefficients(f, p) for f in fs))
    return np.array(ks), np.array(es)


def sigma_of_f(f, sigma_struct, c=4.0, p: NeuronParams = DEFAULT):
    """Coupling sigma(f) = sqrt(sigma_struct^2 + (c*eta(f))^2) (Eq. 19-20)."""
    _, eta = measure_coefficients(f, p)
    return np.sqrt(sigma_struct**2 + (c * eta) ** 2)


def stability_margin(f, sigma_struct, D, g, c=4.0, p: NeuronParams = DEFAULT):
    """S(f) = 1 - g * sigma(f) * sqrt(D): the composed cascade (Eq. 20)."""
    return 1.0 - g * sigma_of_f(f, sigma_struct, c, p) * np.sqrt(D)


def crossing_fraction(sigma_struct, D, g, c=4.0, p: NeuronParams = DEFAULT,
                      fs=None):
    """Smallest NMDAR loss 1 - f at which S(f) crosses zero (None if never)."""
    if fs is None:
        fs = np.linspace(1.0, 0.15, 400)
    for f in fs:
        if stability_margin(f, sigma_struct, D, g, c, p) < 0:
            return 1.0 - f
    return None


def predicted_gate_at_peak(f, p: NeuronParams = DEFAULT):
    """Analytic peak condition sig(u*) = 1 - s / (f * dtheta) (Eq. S6)."""
    return 1.0 - p.s / (f * p.dtheta)
