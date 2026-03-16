#!/usr/bin/env python3
"""Run all 30 detector x representation combinations.

Usage:
    python scripts/run_detection.py --features ./outputs/features.npz --output ./outputs/results.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.detectors.isolation_forest import IsolationForestDetector
from src.detectors.one_class_svm import OneClassSVMDetector
from src.detectors.gmm_detector import GMMDetector
from src.detectors.autoencoder import AutoencoderDetector
from src.detectors.pca_mahalanobis import PCAMahalanobisDetector
from src.detectors.lof_detector import LOFDetector
from src.reduction.reducers import get_reducer, UMAP_AVAILABLE


DETECTORS = {
    "isolation_forest": lambda seed: IsolationForestDetector(random_state=seed),
    "one_class_svm": lambda seed: OneClassSVMDetector(),
    "gmm": lambda seed: GMMDetector(random_state=seed),
    "autoencoder": lambda seed: AutoencoderDetector(random_state=seed, epochs=20),
    "pca_mahalanobis": lambda seed: PCAMahalanobisDetector(random_state=seed),
    "lof": lambda seed: LOFDetector(),
}

REPRESENTATIONS = ["raw", "pca", "ica", "random_projection"]
if UMAP_AVAILABLE:
    REPRESENTATIONS.append("umap")

SEEDS = [42, 123, 456, 789, 1024]


def main():
    parser = argparse.ArgumentParser(description="Run detection experiments")
    parser.add_argument("--features", type=str, required=True, help="Input .npz features file")
    parser.add_argument("--output", type=str, required=True, help="Output JSON results file")
    args = parser.parse_args()

    data = np.load(args.features, allow_pickle=True)
    X, labels = data["X"], data["labels"]

    results = []

    for seed in SEEDS:
        X_train, X_test, y_train, y_test = train_test_split(
            X, labels, test_size=0.3, random_state=seed, stratify=labels
        )

        for rep_name in REPRESENTATIONS:
            if rep_name == "raw":
                X_tr, X_te = X_train, X_test
            else:
                n_comp = min(50, X_train.shape[1] - 1)
                reducer = get_reducer(rep_name, n_components=n_comp, random_state=seed)
                X_tr = reducer.fit_transform(X_train)
                X_te = reducer.transform(X_test)

            for det_name, det_factory in DETECTORS.items():
                t0 = time.time()
                detector = det_factory(seed)
                detector.fit(X_tr)
                scores = detector.score(X_te)
                elapsed = time.time() - t0

                results.append({
                    "detector": det_name,
                    "representation": rep_name,
                    "seed": seed,
                    "n_test": len(y_test),
                    "n_positive": int(y_test.sum()),
                    "mean_score_clean": float(scores[y_test == 0].mean()),
                    "mean_score_backdoor": float(scores[y_test == 1].mean()),
                    "runtime_seconds": round(elapsed, 3),
                })

                print(f"[{det_name}/{rep_name}/seed={seed}] "
                      f"clean={results[-1]['mean_score_clean']:.3f} "
                      f"backdoor={results[-1]['mean_score_backdoor']:.3f} "
                      f"({elapsed:.2f}s)")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} results to {output_path}")


if __name__ == "__main__":
    main()
