# Product Spec — Model Behavioral Fingerprinting

## Target User

ML engineers who download pre-trained models from Hugging Face, PyTorch Hub,
or other model registries and need confidence that models are not backdoored
or tampered with.

## User Story

> As an ML engineer, I want to scan a downloaded model before deploying it,
> so that I can detect behavioral anomalies that indicate backdoors or poisoning,
> without needing a labeled dataset of known-clean models.

## Core Workflow

1. `POST /scan` with model path and task type
2. System extracts behavioral fingerprint (activations, outputs, gradients)
3. System runs 6 anomaly detectors on fingerprint
4. System returns trust score (0-100) with per-detector breakdown
5. Engineer decides deploy/reject based on score and report

## Trust Score

- **0-30:** Low risk — model behavior consistent with clean models
- **31-60:** Medium risk — some anomalies detected, manual review recommended
- **61-100:** High risk — significant behavioral anomalies, do not deploy without investigation

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/scan` | Submit model for scanning |
| GET | `/report/{id}` | Retrieve scan report |
| GET | `/health` | Health check |

## Non-Functional Requirements

- Scan time: < 5 minutes per model on CPU
- Memory: < 4GB peak during scan
- No GPU required for detection (extraction may use GPU if available)
