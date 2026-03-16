#!/usr/bin/env python3
"""SimCLR-style contrastive learning for model fingerprint embeddings.

Pipeline:
  1. Load clean model activations only
  2. Create positive pairs (augmented same-model activations)
  3. Create negative pairs (different models)
  4. Train MLP encoder (512->256->128->64) with NT-Xent loss
  5. Encode all models, compute cosine distance from clean centroid
  6. Score: backdoored models should be further from clean centroid
  7. Compute AUROC & detection rate

Uses PyTorch if available; falls back to sklearn MLPRegressor approximation.

Saves results to outputs/contrastive/
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import normalize

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = ROOT / "outputs" / "features"
OUTPUT_DIR = ROOT / "outputs" / "contrastive"

# ---------------------------------------------------------------------------
# Try PyTorch first
# ---------------------------------------------------------------------------
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


# ===================================================================
# PyTorch implementation
# ===================================================================

def _build_encoder_torch(input_dim: int = 512, seed: int = 42):
    """MLP encoder: 512 -> 256 -> 128 -> 64."""
    torch.manual_seed(seed)

    class Encoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, 256),
                nn.BatchNorm1d(256),
                nn.ReLU(),
                nn.Linear(256, 128),
                nn.BatchNorm1d(128),
                nn.ReLU(),
                nn.Linear(128, 64),
            )

        def forward(self, x):
            return F.normalize(self.net(x), dim=1)

    return Encoder()


def nt_xent_loss(z_i: "torch.Tensor", z_j: "torch.Tensor", temperature: float = 0.5) -> "torch.Tensor":
    """NT-Xent (Normalized Temperature-scaled Cross Entropy) loss.

    z_i, z_j: [B, D] L2-normalized embeddings (positive pairs).
    """
    batch_size = z_i.shape[0]
    z = torch.cat([z_i, z_j], dim=0)  # [2B, D]

    sim = torch.mm(z, z.t()) / temperature  # [2B, 2B]

    # Mask out self-similarity
    mask = ~torch.eye(2 * batch_size, dtype=torch.bool, device=sim.device)
    sim = sim.masked_select(mask).view(2 * batch_size, -1)

    # Positive pair indices: (i, i+B) and (i+B, i)
    pos_sim_ij = torch.sum(z_i * z_j, dim=1) / temperature  # [B]
    pos_sim_ji = torch.sum(z_j * z_i, dim=1) / temperature  # [B]
    pos_sim = torch.cat([pos_sim_ij, pos_sim_ji], dim=0)     # [2B]

    # Log-sum-exp of negatives
    log_sum_exp = torch.logsumexp(sim, dim=1)  # [2B]

    loss = -pos_sim + log_sum_exp
    return loss.mean()


def _augment_batch(X: np.ndarray, rng: np.random.RandomState, noise_scale: float = 0.1) -> np.ndarray:
    """Create augmented version of activation batch (add Gaussian noise + dropout)."""
    noise = rng.randn(*X.shape).astype(np.float32) * noise_scale
    augmented = X + noise

    # Random feature dropout (zero out 10% of features)
    mask = rng.binomial(1, 0.9, size=X.shape).astype(np.float32)
    augmented = augmented * mask

    return augmented


def run_contrastive_torch(
    X_clean: np.ndarray,
    X_all: np.ndarray,
    labels: np.ndarray,
    seed: int = 42,
    epochs: int = 100,
    batch_size: int = 64,
    lr: float = 1e-3,
    temperature: float = 0.5,
) -> dict:
    """Train contrastive encoder and score all models."""
    rng = np.random.RandomState(seed)
    torch.manual_seed(seed)

    input_dim = X_clean.shape[1]
    encoder = _build_encoder_torch(input_dim, seed)
    optimizer = torch.optim.Adam(encoder.parameters(), lr=lr, weight_decay=1e-5)

    n_clean = X_clean.shape[0]
    losses = []

    encoder.train()
    for epoch in range(epochs):
        # Sample batch from clean data
        idx = rng.choice(n_clean, size=min(batch_size, n_clean), replace=False)
        x_batch = X_clean[idx]

        # Create positive pairs via augmentation
        x_i = torch.FloatTensor(x_batch)
        x_j = torch.FloatTensor(_augment_batch(x_batch, rng))

        z_i = encoder(x_i)
        z_j = encoder(x_j)

        loss = nt_xent_loss(z_i, z_j, temperature)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        losses.append(float(loss.item()))
        if (epoch + 1) % 20 == 0:
            print(f"    Epoch {epoch+1}/{epochs}  loss={loss.item():.4f}")

    # Encode all models
    encoder.eval()
    with torch.no_grad():
        embeddings = encoder(torch.FloatTensor(X_all)).numpy()

    return embeddings, losses


def run_contrastive_sklearn(
    X_clean: np.ndarray,
    X_all: np.ndarray,
    labels: np.ndarray,
    seed: int = 42,
    epochs: int = 100,
) -> tuple[np.ndarray, list]:
    """Fallback: use sklearn MLPRegressor as a pseudo-contrastive encoder.

    Train an autoencoder-style MLP on clean data, use bottleneck as embedding.
    """
    from sklearn.neural_network import MLPRegressor

    print("    [fallback] Using sklearn MLPRegressor (no PyTorch)")

    # Train autoencoder on clean data (input=output)
    mlp = MLPRegressor(
        hidden_layer_sizes=(256, 128, 64, 128, 256),
        activation="relu",
        max_iter=epochs,
        random_state=seed,
        early_stopping=True,
        validation_fraction=0.1,
    )
    mlp.fit(X_clean, X_clean)

    # Extract bottleneck activations (layer 3 = 64-dim)
    # Forward pass manually through layers
    h = X_all.copy()
    for i, (W, b) in enumerate(zip(mlp.coefs_, mlp.intercepts_)):
        h = h @ W + b
        if i < len(mlp.coefs_) - 1:
            h = np.maximum(h, 0)  # ReLU
        if i == 2:  # bottleneck layer (64-dim)
            embeddings = h.copy()
            break

    embeddings = normalize(embeddings, axis=1)
    return embeddings, [float(mlp.loss_)]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_by_centroid_distance(
    embeddings: np.ndarray,
    labels: np.ndarray,
) -> tuple[np.ndarray, float, float, float]:
    """Score models by cosine distance from clean centroid.

    Returns (scores, auroc, dr@5%, dr@10%).
    """
    clean_emb = embeddings[labels == 0]
    centroid = clean_emb.mean(axis=0)
    centroid = centroid / (np.linalg.norm(centroid) + 1e-8)

    # Cosine distance from centroid
    emb_norm = normalize(embeddings, axis=1)
    cosine_sim = emb_norm @ centroid
    scores = 1.0 - cosine_sim  # higher = more anomalous

    # Metrics
    try:
        auroc = float(roc_auc_score(labels, scores))
    except ValueError:
        auroc = float("nan")

    # Detection rates
    clean_scores = scores[labels == 0]
    bd_scores = scores[labels == 1]

    def dr_at_fpr(target_fpr):
        threshold = np.quantile(clean_scores, 1.0 - target_fpr)
        return float((bd_scores > threshold).sum() / len(bd_scores))

    dr_5 = dr_at_fpr(0.05)
    dr_10 = dr_at_fpr(0.10)

    return scores, auroc, dr_5, dr_10


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    X = np.load(FEATURE_DIR / "activation_matrix.npy")
    labels = np.load(FEATURE_DIR / "labels.npy")
    print(f"Loaded X={X.shape}, labels={labels.shape}")
    print(f"  PyTorch available: {TORCH_AVAILABLE}")

    clean_mask = labels == 0
    X_clean = X[clean_mask]
    print(f"  Clean models for training: {X_clean.shape[0]}")

    seeds = [42, 123, 456, 789, 1024]
    all_results = []

    for seed in seeds:
        print(f"\n--- Seed {seed} ---")
        t0 = time.time()

        if TORCH_AVAILABLE:
            embeddings, losses = run_contrastive_torch(
                X_clean, X, labels, seed=seed, epochs=100, batch_size=64,
            )
        else:
            embeddings, losses = run_contrastive_sklearn(
                X_clean, X, labels, seed=seed, epochs=200,
            )

        elapsed = time.time() - t0
        scores, auroc, dr_5, dr_10 = score_by_centroid_distance(embeddings, labels)

        result = {
            "method": "contrastive_simclr" if TORCH_AVAILABLE else "contrastive_sklearn_fallback",
            "seed": seed,
            "auroc": round(auroc, 4),
            "detection_rate_fpr05": round(dr_5, 4),
            "detection_rate_fpr10": round(dr_10, 4),
            "final_loss": round(losses[-1], 4) if losses else None,
            "n_clean_train": int(X_clean.shape[0]),
            "n_total": int(X.shape[0]),
            "embedding_dim": int(embeddings.shape[1]),
            "runtime_seconds": round(elapsed, 3),
            "backend": "pytorch" if TORCH_AVAILABLE else "sklearn",
        }
        all_results.append(result)

        # Save per-seed
        with open(OUTPUT_DIR / f"contrastive_seed{seed}.json", "w") as f:
            json.dump(result, f, indent=2)

        # Save embeddings for the first seed (for visualization)
        if seed == 42:
            np.save(OUTPUT_DIR / "embeddings_seed42.npy", embeddings)
            np.save(OUTPUT_DIR / "scores_seed42.npy", scores)

        print(f"  AUROC={auroc:.3f}  DR@5%={dr_5:.3f}  DR@10%={dr_10:.3f}  ({elapsed:.1f}s)")

    # Summary
    summary = {
        "method": all_results[0]["method"],
        "backend": all_results[0]["backend"],
        "seeds": seeds,
        "mean_auroc": round(float(np.mean([r["auroc"] for r in all_results])), 4),
        "std_auroc": round(float(np.std([r["auroc"] for r in all_results])), 4),
        "mean_dr_fpr05": round(float(np.mean([r["detection_rate_fpr05"] for r in all_results])), 4),
        "mean_dr_fpr10": round(float(np.mean([r["detection_rate_fpr10"] for r in all_results])), 4),
        "per_seed": all_results,
    }
    with open(OUTPUT_DIR / "contrastive_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Contrastive learning complete.")
    print(f"  Mean AUROC: {summary['mean_auroc']:.3f} +/- {summary['std_auroc']:.3f}")
    print(f"  Mean DR@5%: {summary['mean_dr_fpr05']:.3f}")
    print(f"  Mean DR@10%: {summary['mean_dr_fpr10']:.3f}")
    print(f"  Results: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
