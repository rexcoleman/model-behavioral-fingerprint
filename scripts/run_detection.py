#!/usr/bin/env python3
"""Run all 30 detector x representation combinations on synthetic data.

For each of 5 representations x 6 detectors x 5 seeds:
  - Train on clean-only activations (80% of clean)
  - Score mixed test set
  - Compute AUROC, detection rate @ FPR=5%, detection rate @ FPR=10%

Saves:
  outputs/detection/<detector>_<representation>_seed<seed>.json  (one per combo)
  outputs/detection/benchmark_summary.json                       (all results)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedShuffleSplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.detectors.isolation_forest import IsolationForestDetector
from src.detectors.one_class_svm import OneClassSVMDetector
from src.detectors.gmm_detector import GMMDetector
from src.detectors.autoencoder import AutoencoderDetector
from src.detectors.pca_mahalanobis import PCAMahalanobisDetector
from src.detectors.lof_detector import LOFDetector
from src.reduction.reducers import get_reducer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = ROOT / "outputs" / "features"
OUTPUT_DIR = ROOT / "outputs" / "detection"

DETECTORS = {
    "isolation_forest": lambda seed: IsolationForestDetector(random_state=seed),
    "one_class_svm": lambda seed: OneClassSVMDetector(),
    "gmm": lambda seed: GMMDetector(random_state=seed),
    "autoencoder": lambda seed: AutoencoderDetector(random_state=seed, epochs=30),
    "pca_mahalanobis": lambda seed: PCAMahalanobisDetector(random_state=seed),
    "lof": lambda seed: LOFDetector(),
}

REPRESENTATIONS = ["raw", "pca", "ica", "random_projection", "raw_noDR"]

SEEDS = [42, 123, 456, 789, 1024]

DR_COMPONENTS = 50


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def detection_rate_at_fpr(scores: np.ndarray, labels: np.ndarray, target_fpr: float) -> float:
    """Compute detection rate (TPR) at a given FPR threshold.

    Parameters
    ----------
    scores : array of anomaly scores (higher = more anomalous)
    labels : binary labels (0=clean, 1=backdoored)
    target_fpr : desired false-positive rate (e.g., 0.05)
    """
    clean_scores = scores[labels == 0]
    backdoor_scores = scores[labels == 1]

    if len(clean_scores) == 0 or len(backdoor_scores) == 0:
        return float("nan")

    # Threshold = (1 - target_fpr) quantile of clean scores
    threshold = np.quantile(clean_scores, 1.0 - target_fpr)
    detected = (backdoor_scores > threshold).sum()
    return float(detected / len(backdoor_scores))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load synthetic data
    X = np.load(FEATURE_DIR / "activation_matrix.npy")
    labels = np.load(FEATURE_DIR / "labels.npy")
    print(f"Loaded X={X.shape}, labels={labels.shape}  "
          f"(clean={int((labels==0).sum())}, backdoor={int((labels==1).sum())})")

    all_results = []

    for seed in SEEDS:
        # Stratified 80/20 split
        sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
        train_idx, test_idx = next(sss.split(X, labels))

        X_pool_train, X_test = X[train_idx], X[test_idx]
        y_pool_train, y_test = labels[train_idx], labels[test_idx]

        # Train on clean only
        clean_train_mask = y_pool_train == 0
        X_train_clean = X_pool_train[clean_train_mask]

        for rep_name in REPRESENTATIONS:
            # Apply dimensionality reduction
            if rep_name in ("raw", "raw_noDR"):
                X_tr = X_train_clean.copy()
                X_te = X_test.copy()
            else:
                n_comp = min(DR_COMPONENTS, X_train_clean.shape[1] - 1, X_train_clean.shape[0] - 1)
                reducer = get_reducer(rep_name, n_components=n_comp, random_state=seed)
                X_tr = reducer.fit_transform(X_train_clean)
                X_te = reducer.transform(X_test)

            for det_name, det_factory in DETECTORS.items():
                t0 = time.time()
                detector = det_factory(seed)
                detector.fit(X_tr)
                scores = detector.score(X_te)
                elapsed = time.time() - t0

                # Metrics
                try:
                    auroc = float(roc_auc_score(y_test, scores))
                except ValueError:
                    auroc = float("nan")

                dr_5 = detection_rate_at_fpr(scores, y_test, 0.05)
                dr_10 = detection_rate_at_fpr(scores, y_test, 0.10)

                result = {
                    "detector": det_name,
                    "representation": rep_name,
                    "seed": seed,
                    "auroc": round(auroc, 4),
                    "detection_rate_fpr05": round(dr_5, 4),
                    "detection_rate_fpr10": round(dr_10, 4),
                    "n_train_clean": int(X_tr.shape[0]),
                    "n_test": int(len(y_test)),
                    "n_test_backdoor": int((y_test == 1).sum()),
                    "mean_score_clean": round(float(scores[y_test == 0].mean()), 4),
                    "mean_score_backdoor": round(float(scores[y_test == 1].mean()), 4),
                    "runtime_seconds": round(elapsed, 3),
                }
                all_results.append(result)

                # Save individual result
                fname = f"{det_name}_{rep_name}_seed{seed}.json"
                with open(OUTPUT_DIR / fname, "w") as f:
                    json.dump(result, f, indent=2)

                print(f"  [{det_name:20s}/{rep_name:20s}/seed={seed}] "
                      f"AUROC={auroc:.3f}  DR@5%={dr_5:.3f}  DR@10%={dr_10:.3f}  "
                      f"({elapsed:.2f}s)")

    # Save summary
    summary_path = OUTPUT_DIR / "benchmark_summary.json"
    with open(summary_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'='*70}")
    print(f"Saved {len(all_results)} results to {OUTPUT_DIR}/")
    print(f"Summary: {summary_path}")

    # Quick summary table
    print(f"\n--- Mean AUROC across seeds ---")
    from collections import defaultdict
    agg = defaultdict(list)
    for r in all_results:
        key = (r["detector"], r["representation"])
        if not np.isnan(r["auroc"]):
            agg[key].append(r["auroc"])
    for (det, rep), vals in sorted(agg.items()):
        print(f"  {det:20s} | {rep:20s} | AUROC={np.mean(vals):.3f} +/- {np.std(vals):.3f}")


if __name__ == "__main__":
    main()
