# Figures & Tables Contract — FP-13 Model Behavioral Fingerprinting

> Every figure and table in the project is documented here with its data source, generation method, and claim linkage.

## Figures

### Figure 1: Detection by Method
- **File:** `figures/detection_by_method.png`
- **Data source:** `outputs/results/*.json` (150 files)
- **Generator:** `scripts/make_report_figures.py`
- **X-axis:** Detector (LOF, OCSVM, AE, IF, PCA+Maha, GMM)
- **Y-axis:** Mean AUROC
- **Series:** Raw features only (best representation)
- **Error bars:** Standard deviation across 5 seeds
- **Claim linkage:** RQ1 — LOF best at 0.622, all detectors above chance [DEMONSTRATED: 5 seeds]
- **Hardcoded values:** NONE

### Figure 2: Detection Heatmap
- **File:** `figures/detection_heatmap.png`
- **Data source:** `outputs/results/*.json` (150 files)
- **Generator:** `scripts/make_report_figures.py`
- **Axes:** Detector (rows) x Representation (columns)
- **Color:** AUROC value (diverging colormap, center=0.50)
- **Claim linkage:** RQ2/RQ3 — raw features best for 3/6 detectors; DR hurts [DEMONSTRATED: 5 seeds]
- **Hardcoded values:** NONE

### Figure 3: DR Improvement (Negative Result)
- **File:** `figures/dr_improvement.png`
- **Data source:** `outputs/results/*.json` (150 files)
- **Generator:** `scripts/make_report_figures.py`
- **X-axis:** Representation (Raw, PCA, ICA, RP)
- **Y-axis:** Mean AUROC (averaged across all detectors)
- **Claim linkage:** H-2 FALSIFIED — DR hurts detection [DEMONSTRATED: 5 seeds]
- **Hardcoded values:** NONE

### Figure 4: Contrastive Comparison
- **File:** `figures/contrastive_comparison.png`
- **Data source:** `outputs/contrastive/*.json` (5 files)
- **Generator:** `scripts/make_report_figures.py`
- **Content:** SimCLR AUROC vs classical method AUROCs (bar chart)
- **Claim linkage:** RQ4 — SimCLR 0.466 below chance; classical dominates [DEMONSTRATED: 5 seeds]
- **Hardcoded values:** NONE

## Tables

All tables in FINDINGS.md are inline Markdown derived from the same JSON result files. No separate table generation script; values are aggregated from per-run JSONs.

## Reproducibility

```bash
# Regenerate all figures from raw data
python scripts/make_report_figures.py
# Outputs: figures/*.png
```
