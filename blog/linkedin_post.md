# LinkedIn Post — FP-13 Model Behavioral Fingerprinting

---

**Dimensionality reduction makes backdoor detection worse, not better.**

I ran 150 experiments testing 6 unsupervised anomaly detectors for model supply chain security and learned something that contradicts standard ML intuition:

When the threat signal is diffuse (training-data poisoning spreads across many activation dimensions), reducing dimensions discards exactly the signal you need.

Raw features (AUROC 0.607) beat PCA (0.578), ICA (0.568), and Random Projection (0.596).

Other findings from 5-seed validated experiments:
- LOF (a 1990s algorithm) beats autoencoders at 128 training samples
- SimCLR contrastive learning scores below chance (0.466)
- Detection rate: 22-28% of backdoored models flagged at 10% false positive rate

This is a zero-label approach. No labeled backdoor examples needed. Just probe the model, collect activations, and measure anomaly scores.

The trust score aggregates 6 detectors into a single risk rating. An attacker must defeat all 6 methods simultaneously.

Static analysis (ModelScan) catches serialization exploits. Behavioral fingerprinting catches training-data poisoning. They are complementary, not competing.

Full findings + open-source pipeline in the repo.

#ModelSupplyChain #MLSecurity #BackdoorDetection #UnsupervisedLearning #AITrust

---

> **CTA:** "How is your team validating pre-trained models before deployment? Curious about the gap between static checks and behavioral analysis."
