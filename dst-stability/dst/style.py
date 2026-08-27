"""Shared matplotlib style for all figures."""

import matplotlib as mpl

# Colour palette used across all figures
BLUE = "#2b6cb0"
RED = "#c44518"
GREEN = "#2e8b57"
GOLD = "#c8901a"
PURPLE = "#7c4dbe"
NAVY = "#1f2d45"
GRAY = "#6b7280"

STABLE_FILL = "#eef2f7"
UNSTABLE_FILL = "#fbeee7"


def use_style():
    """Apply the shared style. Call once at the top of every figure script."""
    mpl.rcParams.update({
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "font.size": 13,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "axes.labelsize": 13,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.35,
        "grid.linewidth": 0.6,
        "legend.frameon": True,
        "legend.framealpha": 0.9,
        "lines.linewidth": 2.2,
    })


def save(fig, path):
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    print(f"wrote {path}")
