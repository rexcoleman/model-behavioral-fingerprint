# Claim Strength Spec — FP-13 Model Behavioral Fingerprinting

> Defines the claim strength tagging system and maps every major claim to its evidence basis.

## Tag Definitions

| Tag | Requirements | Confidence |
|-----|-------------|------------|
| [DEMONSTRATED: 5 seeds] | Directly measured across 5 seeds, mean +/- std reported | High |
| [DEMONSTRATED: synthetic] | Measured on synthetic data; real-model validation pending | Medium-High (internal validity) |
| [SUGGESTED] | Consistent pattern but limited direct evidence | Medium |
| [PROJECTED] | Extrapolated from partial evidence | Low-Medium |
| [HYPOTHESIZED] | Untested prediction | Low |

## Claim Registry

| # | Claim | Tag | Data Source | Upgrade Path |
|---|-------|-----|-------------|-------------|
| C1 | All detectors above chance on raw features (AUROC 0.589-0.622) | [DEMONSTRATED: 5 seeds] | `outputs/results/` | TrojAI validation |
| C2 | LOF is the best detector (AUROC 0.622 +/- 0.073) | [DEMONSTRATED: 5 seeds] | `outputs/results/` | Paired t-test p-value |
| C3 | Raw features outperform all DR methods (0.607 > 0.596 > 0.578 > 0.568) | [DEMONSTRATED: 5 seeds] | `outputs/results/` | Formal paired test |
| C4 | DR hurts detection for diffuse triggers (H-2 falsified) | [DEMONSTRATED: 5 seeds] | C3 | Mathematical proof of diffuse signal loss |
| C5 | Autoencoder does not outperform classical methods (H-3 falsified) | [DEMONSTRATED: 5 seeds] | `outputs/results/` | Scale to 1000+ training models |
| C6 | SimCLR performs below chance (AUROC 0.466) | [DEMONSTRATED: 5 seeds] | `outputs/contrastive/` | Task-specific augmentation redesign |
| C7 | Best single run OCSVM+PCA seed=789 reaches 0.770 | [DEMONSTRATED: synthetic] | Single seed observation | Anecdotal; not generalizable |
| C8 | Detection rate at FPR=10% averages 22-28% | [DEMONSTRATED: 5 seeds] | `outputs/results/` | TrojAI validation |
| C9 | Trust score ensemble prevents single-detector evasion | [SUGGESTED] | Architectural reasoning | Adaptive adversary evaluation |
| C10 | ACA predicts diffuse triggers are hardest to detect | [SUGGESTED] | Qualitative mapping | Multi-trigger-type evaluation |
| C11 | Real backdoors may be easier to detect (concentrated triggers) | [HYPOTHESIZED] | Literature reasoning | TrojAI validation |

## Synthetic Data Caveat

All claims tagged [DEMONSTRATED: 5 seeds] or [DEMONSTRATED: synthetic] carry the synthetic data caveat documented in FINDINGS.md "Claims on Synthetic Data" section. Absolute AUROC values should not be quoted as real-world performance. Relative rankings (detector ordering, DR effect direction) have higher transfer likelihood.

## Downgrade Triggers

- TrojAI validation shows different detector ranking → downgrade C2
- Larger training set reverses AE vs classical ranking → downgrade C5
- Task-specific augmentations make SimCLR competitive → downgrade C6

## Upgrade Triggers

- TrojAI validation confirms detector ranking → upgrade C1-C5 to [DEMONSTRATED: real-world]
- Formal paired tests with p < 0.01 → add p-values to tags
- Multi-rate sweep confirms linear degradation → promote H-4 from NOT TESTED
