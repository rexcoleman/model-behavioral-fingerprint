#!/usr/bin/env python3
"""Generate report figures from detection results.

STUB — generates placeholder figures. Full implementation after experiments.

Usage:
    python scripts/make_report_figures.py --input ./outputs/results.json --output ./outputs/figures/
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main():
    parser = argparse.ArgumentParser(description="Generate report figures")
    parser.add_argument("--input", type=str, required=True, help="Input JSON results file")
    parser.add_argument("--output", type=str, required=True, help="Output directory for figures")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"make_report_figures.py — STUB")
    print(f"Would generate figures from {args.input} to {output_dir}/")
    print("Planned figures:")
    print("  1. Heatmap: detector x representation AUROC matrix")
    print("  2. ROC curves per detector (best representation)")
    print("  3. Trust score distribution: clean vs backdoored")
    print("  4. DR effect: raw vs reduced detection improvement")
    print("  5. Poisoning rate degradation curves (RQ4)")


if __name__ == "__main__":
    main()
