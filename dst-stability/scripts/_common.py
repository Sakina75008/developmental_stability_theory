"""Shared setup for figure scripts: path handling and output directory."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

FIGDIR = os.path.join(ROOT, "figures")
os.makedirs(FIGDIR, exist_ok=True)


def out(name):
    return os.path.join(FIGDIR, name)
