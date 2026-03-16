#!/usr/bin/env python3
"""Generate synthetic activation data simulating clean vs backdoored models.

Creates:
  - outputs/features/activation_matrix.npy  (200 x 512)
  - outputs/features/labels.npy             (200,)  0=clean, 1=backdoored

200 models total: 160 clean, 40 backdoored (20% poison rate).
Clean models:      N(0, 1) with slight per-model variation.
Backdoored models: N(0, 1) with +0.5 shift in dims 0-50 (trigger signature).
"""

from __future__ import annotations

import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "outputs" / "features"


def generate(seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.RandomState(seed)

    n_clean = 160
    n_backdoor = 40
    n_features = 512
    trigger_dims = 51  # dims 0-50 inclusive

    # --- Clean models ---
    # Each model has a slight per-model bias (simulates architecture variation)
    model_bias = rng.randn(n_clean, 1) * 0.1  # small per-model offset
    X_clean = rng.randn(n_clean, n_features).astype(np.float32) + model_bias

    # --- Backdoored models ---
    model_bias_bd = rng.randn(n_backdoor, 1) * 0.1
    X_backdoor = rng.randn(n_backdoor, n_features).astype(np.float32) + model_bias_bd
    # Inject trigger signature: +0.5 shift in first 51 dimensions
    X_backdoor[:, :trigger_dims] += 0.5

    # --- Combine ---
    X = np.vstack([X_clean, X_backdoor])
    labels = np.zeros(n_clean + n_backdoor, dtype=np.int32)
    labels[n_clean:] = 1

    # Shuffle to avoid ordering leakage
    idx = rng.permutation(len(labels))
    X = X[idx]
    labels = labels[idx]

    return X, labels


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    X, labels = generate()

    np.save(OUT_DIR / "activation_matrix.npy", X)
    np.save(OUT_DIR / "labels.npy", labels)

    print(f"Saved activation_matrix.npy  shape={X.shape}  dtype={X.dtype}")
    print(f"Saved labels.npy             shape={labels.shape}  dtype={labels.dtype}")
    print(f"  Clean:      {(labels == 0).sum()}")
    print(f"  Backdoored: {(labels == 1).sum()}")
    print(f"  Poison rate: {labels.mean():.1%}")
    print(f"Output dir: {OUT_DIR}")


if __name__ == "__main__":
    main()
