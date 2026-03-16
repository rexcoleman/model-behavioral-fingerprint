# Model Behavioral Fingerprinting (FP-13)

Unsupervised anomaly detection on model behavioral fingerprints to detect
backdoored, poisoned, or tampered ML models without labeled training data.

**Brand signal:** "I detect compromised AI models the way antivirus detects
malware — by behavioral anomaly, not signatures."

## Quick Start

```bash
# Create environment
conda env create -f environment.yml
conda activate model-fingerprint

# Run tests (synthetic data only — no real models needed)
make test

# Extract features from a model directory
python scripts/extract_features.py --model-dir ./models --output ./outputs/features.npz

# Run all 30 detector × representation combinations
python scripts/run_detection.py --features ./outputs/features.npz --output ./outputs/results.json

# Generate trust score
python -c "from src.trust_score import TrustScorer; help(TrustScorer)"
```

## Architecture

```
Model Under Test
    │
    ├─→ Reference Inputs (curated per task)
    │       ├─→ Layer Activations   → flatten → feature vector
    │       ├─→ Output Distributions → entropy, max_prob, margin
    │       └─→ Gradient Norms      → L2 norm per layer
    │
    └─→ Feature Matrix (n_models × n_features)
            │
            ├─→ Dimensionality Reduction (PCA, ICA, UMAP, RP)
            │
            └─→ 6 Anomaly Detectors
                    ├─→ Isolation Forest
                    ├─→ One-Class SVM
                    ├─→ GMM
                    ├─→ Autoencoder
                    ├─→ PCA + Mahalanobis
                    └─→ Local Outlier Factor
                            │
                            └─→ Trust Score (0–100)
```

## Experimental Matrix

6 detectors x 5 representations (raw + 4 DR) = **30 combinations** x 5 seeds each.

## Research Questions

| RQ | Question |
|----|----------|
| RQ1 | Can unsupervised anomaly detection on activation patterns distinguish clean from backdoored models? |
| RQ2 | Which layer activations are most informative for different backdoor types? |
| RQ3 | Does dimensionality reduction improve anomaly detection on high-dimensional activations? |
| RQ4 | How does detection degrade as poisoning rate decreases? |

## govML Integration

This project uses [govML](https://github.com/rexcoleman/ml-governance-templates)
templates for experiment tracking, data contracts, and quality gates.

## License

MIT
