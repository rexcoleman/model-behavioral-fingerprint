# Statistical Analysis Spec — FP-13 Model Behavioral Fingerprinting

> Documents the statistical rigor of all quantitative claims.

## Current State: 5-Seed Validated

All 150 experiment runs used 5 seeds (42, 123, 456, 789, 1024). This provides:
- Mean and standard deviation across seeds
- Sufficient power for paired t-tests with Bonferroni correction
- Cross-seed consistency validation

## Seed Coverage

| Experiment | Seeds | Runs per Seed | Total Runs | Status |
|------------|-------|-------------|------------|--------|
| Main experiments (6 det x 5 repr) | 5 | 30 | 150 | COMPLETE |
| Contrastive baseline (SimCLR) | 5 | 1 | 5 | COMPLETE |

## Statistical Tests

### 1. Above-Chance Detection (H-1)
- **Method:** One-sample t-test (mean AUROC vs 0.50)
- **Per detector on raw features:** 5 observations (one per seed)
- **Result:** All 6 detectors above 0.50; LOF p-value pending formal computation
- **Effect size:** Cohen's d for each detector

### 2. DR vs Raw Comparison (H-2)
- **Method:** Paired t-test (raw AUROC vs DR AUROC, paired by seed)
- **Correction:** Bonferroni for 3 DR methods x 6 detectors = 18 tests (alpha = 0.05/18 = 0.0028)
- **Result:** Raw > PCA, ICA for most detectors; RP within noise
- **Effect size:** Cohen's d per comparison

### 3. Autoencoder vs Classical (H-3)
- **Method:** Paired t-test (AE AUROC vs each classical method, paired by seed)
- **Correction:** Bonferroni for 5 comparisons (alpha = 0.05/5 = 0.01)
- **Result:** LOF > AE (pending significance); OCSVM ~ AE
- **Effect size:** Cohen's d

### 4. Contrastive vs Classical (RQ4)
- **Method:** Two-sample t-test (SimCLR AUROC vs best classical)
- **Result:** SimCLR 0.466 vs LOF 0.622; large effect expected
- **Note:** SimCLR has only 5 observations; power is limited

## Reported Statistics Summary

| Claim | Statistic | Seeds | Formal Test |
|-------|-----------|-------|-------------|
| Mean AUROC 0.607 (raw, all detectors) | Mean +/- std | 5 | One-sample t-test vs 0.50 |
| LOF best at 0.622 | Mean +/- 0.073 | 5 | Paired t-test vs next-best |
| Raw > PCA > ICA | Mean comparison | 5 | Paired t-test with Bonferroni |
| SimCLR 0.466 below chance | Mean +/- 0.098 | 5 | One-sample t-test vs 0.50 |
| Best single run 0.770 | Max across seeds | 1 | N/A (anecdotal) |

## Upgrade Path

1. Compute formal p-values for all paired comparisons
2. Report confidence intervals for key AUROC differences
3. Run multi-rate poisoning sweep (H-4) to enable regression analysis
4. Validate on TrojAI benchmark for real-world generalization
