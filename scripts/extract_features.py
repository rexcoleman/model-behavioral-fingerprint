#!/usr/bin/env python3
"""Extract behavioral features from a directory of models.

Usage:
    python scripts/extract_features.py --model-dir ./models --output ./outputs/features.npz
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.extraction.activation_extractor import ActivationExtractor
from src.extraction.output_distribution import OutputDistributionExtractor
from src.extraction.gradient_norms import GradientNormExtractor


def main():
    parser = argparse.ArgumentParser(description="Extract behavioral features from models")
    parser.add_argument("--model-dir", type=str, required=True, help="Directory containing models")
    parser.add_argument("--output", type=str, required=True, help="Output .npz file path")
    parser.add_argument("--n-reference", type=int, default=100, help="Number of reference inputs")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    model_dir = Path(args.model_dir)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # For scaffold: generate synthetic features
    # Real implementation: iterate over models in model_dir
    print(f"Model directory: {model_dir}")
    print(f"Generating synthetic features (scaffold mode)...")

    n_models = 100
    act = ActivationExtractor.extract_synthetic(n_models, 512, seed=args.seed)
    out = OutputDistributionExtractor.extract_synthetic(n_models, 10, seed=args.seed)
    grad = GradientNormExtractor.extract_synthetic(n_models, 3, seed=args.seed)

    X = np.hstack([act, out, grad])
    labels = np.zeros(n_models, dtype=int)
    labels[-10:] = 1  # Last 10% are "backdoored"

    np.savez(
        output_path,
        X=X,
        labels=labels,
        model_ids=np.array([f"model_{i:04d}" for i in range(n_models)]),
    )
    print(f"Saved features: {X.shape} to {output_path}")


if __name__ == "__main__":
    main()
