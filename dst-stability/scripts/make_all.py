"""Regenerate every figure in the manuscript: Figures 1-8 and S1-S7.

Usage:  python scripts/make_all.py
Output: figures/Figure_*.png (300 dpi)
"""

import runpy
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
SCRIPTS = [f"make_figure{n}.py" for n in list(range(1, 9))] + \
          [f"make_figureS{n}.py" for n in range(1, 8)]

if __name__ == "__main__":
    t0 = time.time()
    for name in SCRIPTS:
        print(f"\n=== {name} ===")
        runpy.run_path(str(HERE / name), run_name="__main__")
    print(f"\nAll figures regenerated in {time.time() - t0:.1f} s.")
    sys.exit(0)
