# Implementation Playbook — FP-13 Model Behavioral Fingerprinting

## Purpose

Define phases with Definition of Done (DoD) per LL-18 (governance-first build).
Each phase gate must pass before advancing.

## Phases

### Phase 0: Contracts + Leakage Tests
**Status: COMPLETE**

| DoD Item | Evidence |
|----------|----------|
| EXPERIMENT_CONTRACT.md written | `docs/EXPERIMENT_CONTRACT.md` |
| DATA_CONTRACT.md written | `docs/DATA_CONTRACT.md` |
| HYPOTHESIS_REGISTRY.md pre-registered | `docs/HYPOTHESIS_REGISTRY.md` |
| ADVERSARIAL_EVALUATION.md written | `docs/ADVERSARIAL_EVALUATION.md` |
| Leakage tests pass | `pytest tests/test_leakage.py` |
| Extraction tests pass | `pytest tests/test_extraction.py` |

### Phase 1: Data + Feature Extraction
**Status: COMPLETE**

| DoD Item | Evidence |
|----------|----------|
| Synthetic data generator implemented | `scripts/generate_synthetic_data.py` |
| 200 synthetic models generated (160 clean + 40 backdoored) | `outputs/features/` |
| Activation extractor implemented | `src/extraction/activation_extractor.py` |
| 512-dim feature vectors validated | `outputs/features/activation_matrix.npy` |
| 5-seed generation validated | JSON result files across seeds |

### Phase 2: Experiments (Detection Benchmark)
**Status: COMPLETE**

| DoD Item | Evidence |
|----------|----------|
| 6 detectors implemented | `src/detectors/` |
| 5 representations implemented (raw, PCA, ICA, UMAP, RP) | `src/reduction/` |
| 150-run benchmark complete (6x5x5) | `outputs/detection/benchmark_summary.json` |
| Contrastive learning baseline complete | `outputs/contrastive/contrastive_summary.json` |
| Detector tests pass | `pytest tests/test_detectors.py` |

### Phase 3: Analysis + Figures
**Status: COMPLETE**

| DoD Item | Evidence |
|----------|----------|
| 5 hypotheses resolved (H-1 through H-5) | `FINDINGS.md` hypothesis section |
| 4 figures generated from JSON data | `figures/` (4 PNG files) |
| FINDINGS.md written with claim strength tags | `FINDINGS.md` |
| Trust score design documented | `docs/PRODUCT_SPEC.md` |

### Phase 4: Publication
**Status: NOT STARTED**

| DoD Item | Evidence |
|----------|----------|
| Blog post drafted | TBD |
| Real-model validation on TrojAI benchmark | TBD |
| Final held-out evaluation run once | `scripts/final_eval.py` output |
| Provenance artifacts current | `outputs/provenance/` |
| All tests green | `pytest tests/ -v` |

## Advancement Rule

No phase may begin until all DoD items in the preceding phase are checked.
Exceptions require an ADR entry in DECISION_LOG.md.
