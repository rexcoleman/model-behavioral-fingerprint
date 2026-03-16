#!/usr/bin/env python3
"""Final evaluation on held-out test models.

Usage:
    python scripts/final_eval.py --features ./outputs/features.npz --results ./outputs/results.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main():
    parser = argparse.ArgumentParser(description="Final evaluation on held-out models")
    parser.add_argument("--features", type=str, required=True)
    parser.add_argument("--results", type=str, required=True)
    args = parser.parse_args()

    print("final_eval.py — STUB")
    print(f"Would evaluate best detector/representation on held-out test set from {args.features}")
    print("Steps:")
    print("  1. Load best configuration from results")
    print("  2. Train on full reference set")
    print("  3. Evaluate on held-out models")
    print("  4. Report final AUROC, detection rate @ FPR=5%, FPR=10%")
    print("  5. Generate trust score calibration curve")


if __name__ == "__main__":
    main()
