# Decision Log — FP-13 Model Behavioral Fingerprinting

## ADR-001: Algorithm Selection

**Date:** 2026-03-16
**Status:** Accepted

**Context:** Need unsupervised anomaly detectors that work without labeled
backdoor examples. Must span parametric and non-parametric approaches.

**Decision:** 6 detectors selected:
- **Isolation Forest:** Tree-based, scales well, no distributional assumptions.
- **One-Class SVM:** Kernel method, strong on small samples, RBF boundary.
- **GMM:** Density-based, captures multimodal clean distributions.
- **Autoencoder:** Neural, learns nonlinear manifold of clean activations.
- **PCA + Mahalanobis:** Linear baseline, fast, interpretable distance metric.
- **LOF (Local Outlier Factor):** Density-ratio method, captures local structure.

**Rejected alternatives:**
- DBSCAN: Cluster-based, but backdoored models may not form distinct clusters.
- Deep SVDD: More complex than autoencoder with similar expressiveness at this
  data scale (128 training samples).
- Variational Autoencoder: Overkill for 512-dim features with 128 samples.

**Consequences:** The 6-detector ensemble provides diverse inductive biases.
LOF and IF are non-parametric; OC-SVM and Autoencoder are parametric; GMM and
PCA+Mahalanobis are distributional. This diversity enables the ensemble trust
score design.

---

## ADR-002: Synthetic Data Decision

**Date:** 2026-03-16
**Status:** Accepted

**Context:** Need model activation data with known ground truth (clean vs
backdoored). Options: TrojAI competition data, train real models with
backdoors, or generate synthetic activations.

**Decision:** Synthetic activation vectors for Phase 1. Real-model validation
(TrojAI benchmark) deferred to Phase 4.

**Rationale:**
- Synthetic data provides perfect ground truth labels with zero ambiguity.
- Enables rapid iteration on detector/representation combinations (150 runs
  complete in minutes, not hours).
- Controls for confounds: synthetic generator isolates the backdoor signal
  (+0.5 shift in dims 0-50) from other variation.
- TrojAI models require GPU for feature extraction; synthetic runs on CPU.

**Risk:** Synthetic activations may not capture the complexity of real backdoor
signatures. This is the primary limitation acknowledged in FINDINGS.md.

**Phase 2 plan:** Validate top-3 detector/representation configs on TrojAI
Round 1-4 models with known BadNets, Blended, and WaNet triggers.

---

## ADR-003: Detection Scope

**Date:** 2026-03-16
**Status:** Accepted

**Context:** Model supply chain security includes many threat types. Need to
scope what FP-13 covers vs what is deferred.

**Decision — Phase 1 (in scope):**
- Behavioral fingerprinting via activation analysis
- 6 unsupervised anomaly detectors
- 5 dimensionality reduction methods
- SimCLR contrastive learning baseline
- Trust score ensemble design

**Decision — Phase 2 (deferred):**
- Adaptive adversary (attacker optimizes against specific detectors)
- Multi-rate poisoning sweep (1%, 5%, 10%, 20%, 50%)
- Real model validation (TrojAI benchmark)
- Integration with static analysis (ModelScan) for layered defense
- Contrastive learning with task-specific augmentations

**Rationale:** Phase 1 establishes the detection baseline and identifies which
methods are viable. Phase 2 stress-tests the best methods against harder
conditions. Shipping Phase 1 results quickly provides actionable findings for
the frontier portfolio.

**Consequences:** All Phase 1 results carry the [DEMONSTRATED: synthetic] tag.
Real-model validation is required before any production deployment claims.
