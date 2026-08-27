"""Small helpers for schematic (box-and-arrow) panels drawn in matplotlib."""

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def box(ax, xy, w, h, text, color, fontsize=12, lw=2.2, text_color=None):
    """Rounded box centred at xy = (x, y) with centred text."""
    x, y = xy
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=lw, edgecolor=color, facecolor="white", zorder=3,
    )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            color=text_color or color, fontweight="bold", zorder=4)
    return patch


def arrow(ax, start, end, color, lw=2.5, style="-|>", ls="-", zorder=2):
    a = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=22,
                        linewidth=lw, color=color, linestyle=ls,
                        zorder=zorder)
    ax.add_patch(a)
    return a
