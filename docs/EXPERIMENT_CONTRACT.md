# Experiment Contract — FP-13 Model Behavioral Fingerprinting

## Scope

**Matrix:** 6 detectors x 5 representations x 5 seeds = 150 runs

### Detectors
1. Isolation Forest (sklearn)
2. One-Class SVM (sklearn)
3. GMM anomaly scoring (sklearn)
4. Autoencoder reconstruction error (PyTorch)
5. PCA + Mahalanobis distance
6. Local Outlier Factor (sklearn)

### Representations
1. Raw features (no DR)
2. PCA (retain 95% variance)
3. ICA (n_components = min(50, n_features))
4. UMAP (n_components = 50)
5. Random Projection (n_components = 50, JL-lemma)

### Seeds
42, 123, 456, 789, 1024

## Metrics
- AUROC (primary)
- Detection rate at FPR = 5%, 10%
- Precision-Recall AUC
- Runtime per model (wall-clock seconds)

## Success Criteria
- At least one combination achieves AUROC >= 0.70 on TrojAI benchmark
- Detection rate >= 70% at FPR <= 10% (RQ1)
- DR improves over raw for >= 3 detectors (RQ3)

## Reproducibility
- All seeds fixed
- `reproduce.sh` runs full pipeline from scratch
- Results stored as JSON with full config
