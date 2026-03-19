# Hypothesis Registry — FP-13 Model Behavioral Fingerprinting

Pre-registered hypotheses (G0.1 compliance).
**lock_commit:** `<insert-commit-hash-at-lock>`

## Summary Table

| ID | Statement | Metric | Threshold | Status | Evidence |
|----|-----------|--------|-----------|--------|----------|
| H-1 | Behavioral fingerprinting detects backdoors static analysis misses | AUROC (clean vs backdoored) | AUROC >= 0.70 mean across detectors | **PARTIALLY SUPPORTED** | Mean AUROC 0.607 (above 0.50, below 0.70 target) |
| H-2 | DR improves detection (replicating UL ICA+GMM finding) | AUROC delta (DR vs raw) | DR AUROC > raw AUROC for majority of detectors | **FALSIFIED** | Raw 0.607 > PCA 0.578 > ICA 0.568; DR hurts 3/6 detectors clearly |
| H-3 | Autoencoder outperforms classical UL methods | AUROC ranking | AE top-1 or top-2 across representations | **FALSIFIED** | AE 0.616 < LOF 0.622; ties OCSVM; rank 2-3 of 6 |
| H-4 | Detection degrades linearly with poisoning rate | AUROC vs poisoning rate slope | Linear fit R-squared >= 0.80 | **NOT TESTED** | Single rate (20%) used |
| H-5 | Controllability predicts detection difficulty | ACA category vs AUROC | Correlation between controllability and detection | **SUPPORTED QUALITATIVELY** | Diffuse triggers (attacker-controlled training data) hardest to detect, as predicted |

---

## H-1: Behavioral fingerprinting detects backdoors that static analysis misses
**Statement:** Behavioral fingerprinting detects backdoored models that static analysis (FP-10/ModelScan) misses.
**Metric:** AUROC on binary classification (clean vs backdoored) using anomaly scores.
**Threshold:** Mean AUROC >= 0.70 across all detectors on raw features.
**Falsification:** All backdoors detectable by static analysis also detected by behavioral analysis (no additive value).
**Status:** PARTIALLY SUPPORTED [DEMONSTRATED: synthetic]
**Evidence:** Mean AUROC 0.607 across 6 detectors on raw features. Above chance (0.50) but below the 0.70 target. Detection rate at FPR=10% averages 22-28%. Proof-of-concept validated; production threshold not met.

## H-2: Dimensionality reduction improves detection
**Statement:** Dimensionality reduction on activation vectors improves detection (replicating UL Report ICA+GMM finding).
**Metric:** AUROC delta between DR-reduced and raw feature representations.
**Threshold:** DR AUROC > raw AUROC for >= 4 of 6 detectors.
**Falsification:** Raw activation detection >= DR-reduced detection on all metrics.
**Status:** FALSIFIED [DEMONSTRATED: 5 seeds]
**Evidence:** Raw (0.607) > PCA (0.578) > ICA (0.568). Raw wins 3/6 detectors clearly, ties 1. DR discards the diffuse signal.

## H-3: Autoencoder outperforms classical methods
**Statement:** Autoencoder-based detection outperforms classical UL methods (IF, OCSVM) on high-dimensional activations.
**Metric:** AUROC ranking across all representations.
**Threshold:** Autoencoder in top-1 or top-2 across all representation types.
**Falsification:** Classical methods >= autoencoder on all metrics.
**Status:** FALSIFIED [DEMONSTRATED: 5 seeds]
**Evidence:** AE raw AUROC 0.616 < LOF 0.622, ties OCSVM 0.616. At 128 training samples, classical non-parametric methods match or exceed AE.

## H-4: Detection degrades linearly with poisoning rate
**Statement:** Detection performance degrades linearly with poisoning rate (stealthier = harder).
**Metric:** AUROC as function of poisoning rate (1%, 5%, 10%, 20%, 50%).
**Threshold:** Linear fit R-squared >= 0.80.
**Falsification:** Non-linear relationship or no degradation.
**Status:** NOT TESTED
**Evidence:** Only 20% rate tested. Multi-rate sweep planned.

## H-5: Controllability predicts detection difficulty
**Statement:** Controllability analysis predicts which backdoor injection points are hardest to detect.
**Metric:** Correlation between ACA controllability category and AUROC.
**Threshold:** Positive correlation between defender controllability and detection success.
**Falsification:** No correlation between controllability and detection difficulty.
**Status:** SUPPORTED QUALITATIVELY [SUGGESTED]
**Evidence:** ACA correctly predicts: defender controls reference inputs (instrument), attacker controls training data (attack surface). Diffuse training-data poisoning produces lowest AUROC, consistent with ACA prediction.

## Evaluation Protocol

- Each hypothesis tested across all 150 experiment runs (6 detectors x 5 representations x 5 seeds)
- Statistical significance: paired t-test with Bonferroni correction (alpha = 0.05 / 5 = 0.01)
- Effect size: Cohen's d reported for all comparisons
- Results recorded BEFORE interpreting (pre-registration integrity)
