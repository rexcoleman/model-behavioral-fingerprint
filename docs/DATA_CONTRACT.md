# Data Contract — FP-13 Model Behavioral Fingerprinting

## Primary: TrojAI Competition (IARPA)

- **Source:** https://pages.nist.gov/trojai/
- **Contents:** 1000+ models (clean + backdoored), image classifiers
- **Architectures:** ResNet, DenseNet, VGG variants
- **Ground truth:** Available for validation only (NOT used in training)
- **License:** Public domain (US Government)

## Secondary: Self-Poisoned Models

- **Base models:** BERT-base, ResNet-18, simple tabular models (from Hugging Face)
- **Poisoning methods:**
  - BadNets (patch trigger)
  - Blended (noise trigger)
  - WaNet (warping)
  - Clean-label (label flip)
- **Scale:** 50 clean + 50 poisoned per architecture
- **Advantage:** Complete control over poisoning parameters

## Tertiary: Hugging Face Wild Models (Stretch Goal)

- Top-100 models per task (sentiment, image classification)
- No ground truth — pure unsupervised anomaly detection

## Feature Matrix Schema

```
features.npz:
  X:          (n_models, n_features)  float32  — concatenated behavioral features
  labels:     (n_models,)             int      — 0=clean, 1=backdoored (for eval only)
  model_ids:  (n_models,)             str      — model identifiers
  layer_map:  dict                             — feature index ranges per extraction type
```

## Train/Test Split

- Models split by identity (no model appears in both train and test)
- 70% reference (fit detectors) / 30% held-out (evaluate)
- Split is on MODEL identity, not on feature samples
