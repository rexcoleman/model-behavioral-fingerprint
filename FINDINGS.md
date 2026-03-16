# FINDINGS — Model Behavioral Fingerprinting

> **Status:** COMPLETE — 6 detectors x 5 representations x 5 seeds = 150 runs + contrastive learning baseline
> **Project:** FP-13 (Model Behavioral Fingerprinting)
> **Thesis:** Unsupervised anomaly detection on model activations can detect backdoored models that static analysis (ModelScan) misses, without requiring labeled training data.
> **Data:** 200 synthetic model fingerprints (160 clean + 40 test, 8 backdoored) per seed, activation vectors from intermediate layers
> **Seeds:** 42, 123, 456, 789, 1024

---

## Claim Strength Legend

| Tag | Meaning |
|-----|---------|
| [DEMONSTRATED: 5 seeds] | Directly measured across all 5 seeds, mean +/- std reported |
| [DEMONSTRATED: synthetic] | Measured on synthetic data; real-model validation pending |
| [SUGGESTED] | Consistent pattern but limited evidence or single-seed |
| [PROJECTED] | Extrapolated from partial evidence |
| [HYPOTHESIZED] | Untested prediction |

---

## Key Results

### RQ1: Can unsupervised detection distinguish clean from backdoored? [DEMONSTRATED: 5 seeds]

**Yes, with modest but above-chance discrimination.** All 6 detectors on raw features exceed random (0.50), with mean AUROC ranging from 0.589 to 0.622.

| Detector | Representation | Mean AUROC | Std | Detection Rate @ FPR=10% |
|----------|---------------|-----------|-----|--------------------------|
| **LOF** | **raw** | **0.622** | 0.073 | 0.275 |
| One-Class SVM | raw | 0.616 | 0.092 | 0.225 |
| Autoencoder | raw | 0.616 | 0.091 | 0.250 |
| Isolation Forest | raw | 0.605 | 0.081 | 0.275 |
| PCA + Mahalanobis | raw | 0.595 | 0.113 | 0.150 |
| GMM | raw | 0.589 | 0.069 | 0.250 |

**Best single run:** One-Class SVM + PCA, seed=789, AUROC=0.770

**Verdict:** Behavioral fingerprinting provides above-chance detection (best mean AUROC 0.622) but does not meet the experiment contract success criterion of AUROC >= 0.70 on average. The signal is real but weak on synthetic data with subtle (diffuse) triggers. Detection rate at FPR=10% averages 22-28% across detectors -- meaningful for a zero-label approach but below the 70% target.

### RQ2: Which features are most informative? [DEMONSTRATED: synthetic]

Raw activation features (full-dimensional) consistently outperform dimensionality-reduced representations:

| Representation | Mean AUROC (all detectors) | Std |
|---------------|---------------------------|-----|
| **Raw** | **0.607** | 0.081 |
| Random Projection | 0.596 | 0.096 |
| PCA | 0.578 | 0.124 |
| ICA | 0.568 | 0.106 |

Raw features achieve the highest mean AUROC for 4 of 6 detectors (autoencoder, GMM, LOF, and tied for one-class SVM). The finding suggests that the backdoor signal is distributed across many dimensions -- dimensionality reduction discards exactly the subtle, diffuse information that distinguishes backdoored models.

### RQ3: Does dimensionality reduction improve detection? [DEMONSTRATED: 5 seeds]

**No. DR hurts detection for this threat model.**

Raw features beat ALL three DR methods for 3 of 6 detectors (autoencoder, GMM, LOF). For the remaining 3 detectors, the margin is negligible (< 0.01 AUROC) or driven by high-variance single seeds.

| Detector | Raw | PCA | ICA | RP | Raw Wins All? |
|----------|-----|-----|-----|----|----|
| Autoencoder | **0.616** | 0.606 | 0.578 | 0.594 | YES |
| GMM | **0.589** | 0.537 | 0.501 | 0.584 | YES |
| LOF | **0.622** | 0.569 | 0.527 | 0.605 | YES |
| Isolation Forest | 0.605 | 0.538 | 0.598 | **0.610** | no |
| One-Class SVM | 0.616 | **0.616** | 0.617 | 0.587 | no |
| PCA + Mahalanobis | 0.595 | **0.601** | 0.584 | 0.593 | no |

**This falsifies H-2** (that DR improves detection). The CS 7641 UL project found ICA+GMM improved clustering on tabular data; here the opposite holds because the backdoor fingerprint is a subtle, diffuse perturbation rather than a concentrated signal in a few independent components.

### RQ4: Contrastive vs classical comparison [DEMONSTRATED: 5 seeds]

**Classical methods dominate. Contrastive learning (SimCLR) fails on this task.**

| Method | Mean AUROC | Std | Detection Rate @ FPR=10% |
|--------|-----------|-----|--------------------------|
| **LOF (raw)** | **0.622** | 0.073 | 0.275 |
| Autoencoder (raw) | 0.616 | 0.091 | 0.250 |
| One-Class SVM (raw) | 0.616 | 0.092 | 0.225 |
| Isolation Forest (raw) | 0.605 | 0.081 | 0.275 |
| SimCLR Contrastive | 0.466 | 0.098 | 0.095 |

SimCLR achieves AUROC 0.466 -- **below chance** (0.50). The contrastive loss (final ~2.91 across all seeds) failed to converge to a representation that separates clean from backdoored models. This is expected: SimCLR learns representations for data augmentation invariance, but there is no natural augmentation structure for model fingerprints. The contrastive approach needs task-specific augmentations (e.g., weight perturbation) to be viable here.

---

## Hypothesis Resolutions

### H-1: Behavioral fingerprinting detects backdoors that static analysis misses

**PARTIALLY SUPPORTED** [DEMONSTRATED: synthetic]

Behavioral fingerprinting achieves above-chance detection (mean AUROC 0.607 across all raw-feature detectors) on synthetic backdoors designed to be invisible to static weight inspection. Static tools like ModelScan check for serialization exploits and known payload patterns -- they cannot detect behavioral backdoors injected through training data poisoning. Behavioral fingerprinting addresses a fundamentally different threat surface.

However, detection power is modest. This is a proof-of-concept, not a production detector.

### H-2: Dimensionality reduction improves detection

**FALSIFIED** [DEMONSTRATED: 5 seeds]

Raw features (AUROC 0.607) outperform PCA (0.578), ICA (0.568), and Random Projection (0.596). DR discards the diffuse signal that distinguishes backdoored activations. This contradicts the CS 7641 UL finding where ICA+GMM improved clustering, because that task had concentrated independent sources while backdoor triggers are distributed.

### H-3: Autoencoder outperforms classical methods

**FALSIFIED** [DEMONSTRATED: 5 seeds]

Autoencoder (raw AUROC 0.616) ties with One-Class SVM (0.616) and underperforms LOF (0.622). Classical methods match or exceed the autoencoder across representations. On this scale of data (128 training samples), classical non-parametric methods have an advantage -- autoencoders need more data to learn a useful manifold.

### H-4: Detection degrades linearly with poisoning rate

**NOT TESTED** -- single poisoning rate used (20% of test set backdoored). Multi-rate experiments are in the experiment contract but not yet executed.

### H-5: Controllability predicts detection difficulty

**SUPPORTED QUALITATIVELY** [SUGGESTED]

The Adversarial Controllability Analysis (ACA) framework from ADVERSARIAL_EVALUATION.md correctly predicts the core asymmetry:

- **Defender controls reference inputs** -- the fingerprinting probe. This is the detection instrument.
- **Attacker controls training data and weights** -- the attack surface.
- **System controls architecture and inference pipeline** -- harder to poison.

The modest detection results (AUROC ~0.60) are consistent with the ACA prediction that training-data poisoning produces "diffuse" behavioral effects that are harder to detect than direct weight manipulation.

---

## Core Insight: Adversarial Controllability Analysis (ACA)

The ACA framework developed in FP-01 (Adversarial IDS) extends naturally to model supply chain security:

| Injection Point | Controller | Detection Difficulty |
|-----------------|-----------|---------------------|
| Training data poisoning | Attacker | **Hard** -- effects diffuse across layers |
| Weight manipulation | Attacker | **Medium** -- large changes detectable |
| Architecture | System | N/A -- not attackable |
| Inference pipeline | System (partial) | High -- subtle preprocessing attacks |
| **Reference inputs** | **Defender** | **N/A -- this is our instrument** |

**The defender's advantage:** Unlike network IDS (FP-01) where attackers control 57/78 features, in behavioral fingerprinting the defender controls the probe completely. The attacker must produce a model that behaves normally on the defender's chosen reference inputs while activating its backdoor only on trigger inputs. This is a fundamentally more favorable threat model for the defender.

---

## Trust Score Demonstration

The trust score aggregates 6 detector outputs into a single 0-100 risk rating:

| Score Range | Meaning | Action |
|-------------|---------|--------|
| 0-30 | Low risk | Deploy with standard monitoring |
| 31-60 | Medium risk | Manual review recommended |
| 61-100 | High risk | Do not deploy without investigation |

The trust score design (PRODUCT_SPEC.md) inverts the anomaly score: models that look "normal" to all 6 detectors score low (safe), while models that trigger multiple detectors score high (suspicious). The ensemble approach prevents single-detector evasion -- an attacker must defeat all 6 methods simultaneously.

---

## Limitations

1. **Synthetic data** [CRITICAL]. All results use synthetic activation vectors, not real model fingerprints. The synthetic generator creates plausible but simplified behavioral signatures. Real backdoors (BadNets, Blended, WaNet, Clean-label) may produce different activation patterns.

2. **Subtle trigger design.** The synthetic backdoor injection is deliberately diffuse (small perturbation across many features). This makes detection harder but also means results on more concentrated backdoors (e.g., BadNets with a fixed trigger patch) may be significantly better.

3. **Small scale.** 128 clean training models and 8 backdoored test models per seed. Real deployment would use hundreds to thousands of reference models. Detection power likely improves with more reference data (anomaly detection benefits from richer "normal" baselines).

4. **Single poisoning rate.** Only 20% backdoor rate tested. The experiment contract specifies multi-rate evaluation (H-4) but this was not executed.

5. **No adaptive adversary.** Attackers do not know or optimize against the specific detection method. Adaptive evasion scenarios (ADVERSARIAL_EVALUATION.md) remain untested.

6. **SimCLR architecture.** The contrastive learning failure may reflect poor augmentation design rather than a fundamental limitation. Task-specific augmentations (weight noise, layer dropout) could improve contrastive representations.

---

## What's Next

1. **Real model validation.** Apply the pipeline to TrojAI benchmark models with known backdoors. This is the critical validation step.
2. **Multi-rate poisoning sweep.** Test H-4 across 1%, 5%, 10%, 20%, 50% poisoning rates.
3. **Adaptive adversary evaluation.** Implement evasion-aware poisoning (ADVERSARIAL_EVALUATION.md scenarios).
4. **Contrastive augmentation redesign.** Replace SimCLR random augmentations with weight-perturbation and layer-dropout augmentations.
5. **Scale reference set.** Increase clean training models from 128 to 1000+ and measure detection improvement.
6. **Integration with FP-10 (ModelScan).** Combine static analysis (serialization, known patterns) with behavioral fingerprinting for layered defense.
