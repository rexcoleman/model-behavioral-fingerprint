# Content Plan — FP-13 Model Behavioral Fingerprinting

> govML v3.0 compliance document

## Publication Pipeline

| Asset | Status | Target Date | Channel | Word Count |
|-------|--------|------------|---------|------------|
| FINDINGS.md | COMPLETE | -- | Internal | ~3,500 |
| Blog post (draft.md) | DRAFT | 2026-03-25 | rexcoleman.dev | ~1,200 |
| LinkedIn post | DRAFT | 2026-03-25 | LinkedIn | ~300 |
| Substack intro | DRAFT | 2026-03-25 | Substack | ~200 |
| Conference abstract | COMPLETE | 2026-04-01 | Conference | ~250 |
| Conference slides | NOT STARTED | 2026-04-15 | Conference | N/A |

## Content Pillars Mapping

| Pillar | Coverage | Key Message |
|--------|---------|-------------|
| AI Security Architecture (40%) | PRIMARY | Behavioral fingerprinting as model supply chain defense; trust score design |
| ML Systems Governance (35%) | SECONDARY | 6-detector ensemble; ACA framework extension to supply chain |
| Builder-in-Public (25%) | TERTIARY | 150 runs + contrastive baseline on CPU; honest negative results |

## SEO Keywords

- model backdoor detection, behavioral fingerprinting, model supply chain security
- unsupervised anomaly detection, LOF, isolation forest, one-class SVM
- TrojAI, model trust score, ML security, adversarial ML
- dimensionality reduction, PCA, ICA, contrastive learning

## Cross-Promotion

- FP-01 (Adversarial IDS): ACA framework origin
- FP-10 (ModelScan): static analysis comparison
- CS 7641 UL project: DR finding contradiction (H-2 falsification)
- Singularity Cybersecurity: trust score as product concept

## Image Assets

| Image | Source | Path |
|-------|--------|------|
| Detection by method (bar chart) | `make_report_figures.py` | `blog/images/detection_by_method.png` |
| Detection heatmap (detector x representation) | `make_report_figures.py` | `blog/images/detection_heatmap.png` |
| DR improvement (negative result) | `make_report_figures.py` | `blog/images/dr_improvement.png` |
| Contrastive comparison | `make_report_figures.py` | `blog/images/contrastive_comparison.png` |

> Copy figures to `blog/images/` before publication: `cp figures/*.png blog/images/`
