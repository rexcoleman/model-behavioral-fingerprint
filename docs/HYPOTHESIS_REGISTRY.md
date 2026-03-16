# Hypothesis Registry — FP-13 Model Behavioral Fingerprinting

Pre-registered hypotheses (G0.1 compliance).

| ID | Statement | Falsification Criterion |
|----|-----------|------------------------|
| H-1 | Behavioral fingerprinting detects backdoored models that static analysis (FP-10/ModelScan) misses | All backdoors detectable by static analysis also detected by behavioral analysis (no additive value) |
| H-2 | Dimensionality reduction on activation vectors improves detection (replicating UL Report ICA+GMM finding) | Raw activation detection >= DR-reduced detection on all metrics |
| H-3 | Autoencoder-based detection outperforms classical UL methods (IF, OCSVM) on high-dimensional activations | Classical methods >= autoencoder on all metrics |
| H-4 | Detection performance degrades linearly with poisoning rate (stealthier = harder) | Non-linear relationship or no degradation |
| H-5 | Controllability analysis predicts which backdoor injection points are hardest to detect (system-controlled = harder to poison) | No correlation between controllability and detection difficulty |

## Evaluation Protocol

- Each hypothesis tested across all 150 experiment runs
- Statistical significance: paired t-test with Bonferroni correction (alpha = 0.05 / 5 = 0.01)
- Effect size: Cohen's d reported for all comparisons
- Results recorded BEFORE interpreting (pre-registration integrity)
