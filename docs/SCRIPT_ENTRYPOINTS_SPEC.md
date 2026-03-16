# Script Entrypoints Spec — FP-13 Model Behavioral Fingerprinting

## Purpose

Lock the CLI interface for all scripts per LL-22 (interface stability). Any
flag change requires an ADR entry in DECISION_LOG.md.

## Scripts

### 1. `scripts/generate_synthetic_data.py`
Generate synthetic activation data simulating clean vs backdoored models.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| (none) | — | — | No CLI flags; runs with hardcoded defaults |

**Internals:** seed=42, 160 clean + 40 backdoored, 512 features, trigger in dims 0-50.
**Outputs:** `outputs/features/activation_matrix.npy`, `outputs/features/labels.npy`

### 2. `scripts/extract_features.py`
Extract behavioral features from a directory of real models.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--model-dir` | str | required | Directory containing model files |
| `--output` | str | required | Output `.npz` file path |
| `--n-reference` | int | 100 | Number of reference inputs |
| `--seed` | int | 42 | Random seed |

**Outputs:** `<output>.npz` with activation matrices

### 3. `scripts/run_detection.py`
Run all 150 detector x representation x seed combinations.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| (none) | — | — | No CLI flags; iterates full matrix internally |

**Internals:** 6 detectors x 5 representations x 5 seeds = 150 runs.
**Outputs:** `outputs/detection/<detector>_<repr>_seed<N>.json`, `outputs/detection/benchmark_summary.json`

### 4. `scripts/run_contrastive.py`
SimCLR-style contrastive learning for fingerprint embeddings.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| (none) | — | — | No CLI flags; runs 5-seed contrastive pipeline |

**Internals:** MLP encoder (512->256->128->64), NT-Xent loss, 5 seeds.
**Outputs:** `outputs/contrastive/contrastive_seed<N>.json`, `outputs/contrastive/contrastive_summary.json`

### 5. `scripts/make_report_figures.py`
Generate figures from detection and contrastive results.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| (none) | — | — | No CLI flags; reads from outputs/, writes to figures/ |

**Outputs:** `figures/detection_heatmap.png`, `figures/detection_by_method.png`, `figures/contrastive_comparison.png`, `figures/dr_improvement.png`

### 6. `scripts/final_eval.py`
Final evaluation on held-out test models (stub).

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--features` | str | required | Path to features `.npz` file |
| `--results` | str | required | Path to results JSON |

**Outputs:** Final AUROC and detection rate on held-out set (not yet implemented)
