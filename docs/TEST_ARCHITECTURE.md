# Test Architecture — FP-13 Model Behavioral Fingerprinting

## Purpose

Map every test to what it verifies. Test IDs are stable references for
traceability (LL-28). All tests run via `pytest tests/`.

## Test Categories

### Leakage Tests (`tests/test_leakage.py`)

| ID | Name | Verifies |
|----|------|----------|
| LT-1 | Train/test label separation | Training set contains only clean models (no backdoored) |
| LT-2 | No label leakage into features | Feature extraction does not use labels |
| LT-3 | Seed isolation | Each seed produces independent results |

### Detector Tests (`tests/test_detectors.py`)

| ID | Name | Verifies |
|----|------|----------|
| DT-1 | Isolation Forest fit/score | IF trains on clean, scores anomalies > 0 |
| DT-2 | One-Class SVM fit/score | OC-SVM trains on clean, produces decision scores |
| DT-3 | GMM fit/score | GMM log-likelihood produces valid anomaly scores |
| DT-4 | Autoencoder fit/score | AE reconstruction error is higher for anomalies |
| DT-5 | PCA + Mahalanobis | Mahalanobis distance is computable on clean data |
| DT-6 | LOF fit/score | LOF produces valid anomaly scores |

### Extraction Tests (`tests/test_extraction.py`)

| ID | Name | Verifies |
|----|------|----------|
| EX-1 | Activation extractor | Returns correct shape (n_models x n_features) |
| EX-2 | Output distribution | Distribution features are finite and normalized |
| EX-3 | Gradient norms | Gradient norm features are non-negative |

### Reduction Tests (`tests/test_reduction.py`)

| ID | Name | Verifies |
|----|------|----------|
| RD-1 | PCA reduction | Output dimensions match n_components |
| RD-2 | ICA reduction | Output dimensions match n_components |
| RD-3 | Random Projection | JL-lemma bounds respected |

### Trust Score Tests (`tests/test_trust_score.py`)

| ID | Name | Verifies |
|----|------|----------|
| TS-1 | Score range | Trust score output is in [0, 100] |
| TS-2 | Ensemble aggregation | Score aggregates all 6 detector outputs |
| TS-3 | Monotonicity | Higher anomaly = higher trust score (risk) |

### Pipeline Tests (`tests/test_pipeline.py`)

| ID | Name | Verifies |
|----|------|----------|
| PI-1 | End-to-end pipeline | Generate -> detect -> score chain runs without error |
| PI-2 | Output schema | JSON output files match expected schema |
| PI-3 | Figure generation | make_report_figures.py produces all expected figures |

## Running Tests

```bash
pytest tests/ -v
pytest tests/test_leakage.py -v  # leakage only
pytest tests/test_detectors.py -v  # detector unit tests only
```
