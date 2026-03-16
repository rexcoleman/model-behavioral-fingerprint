# Adversarial Evaluation — FP-13 Model Behavioral Fingerprinting

## Threat Model

| Entity | Controls | Goal |
|--------|----------|------|
| **Attacker** | Model weights, training data | Deploy backdoored model that evades detection |
| **Defender** | Reference inputs, detection pipeline | Detect behavioral anomalies without labeled data |

## Controllability Analysis (ACA)

| Injection Point | Controller | Attackable? | Detection Difficulty |
|-----------------|-----------|-------------|---------------------|
| Training data | Attacker | YES | Medium — behavioral effects diffuse |
| Model weights | Attacker | YES | Low — large weight changes detectable |
| Architecture | System | NO | N/A |
| Inference pipeline | System (partial) | PARTIALLY | High — subtle preprocessing changes |
| Reference inputs | Defender | NO | N/A — our instrument |

**Key insight:** Defenders control the reference inputs (fingerprinting probe).
Attackers control training data and weights. Detection = using what WE control
to detect manipulation in what THEY control.

## Adaptive Adversary Scenarios

| Scenario | Attacker Knowledge | Counter |
|----------|-------------------|---------|
| Evasion-aware poisoning | Knows activation fingerprinting used | Diverse references + gradient analysis |
| Reference set inference | Knows approximate reference distribution | Random sampling + adversarial reference generation |
| Method-specific evasion | Knows specific detector (e.g., IF) | Ensemble of 6 methods (no single point of failure) |

## Evaluation Protocol

1. Baseline: detect standard backdoors (BadNets, Blended, WaNet, Clean-label)
2. Adaptive: attacker knows detection method, optimizes evasion
3. Ensemble robustness: measure detection when attacker evades 1-2 individual detectors
