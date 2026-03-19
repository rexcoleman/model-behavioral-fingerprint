# A+ Checklist — FP-13 Model Behavioral Fingerprinting

> govML v3.0 compliance

## Quality Gates
- [x] G0: Hypotheses pre-registered before any experiments
- [x] G1: Experiment contract complete (6 detectors x 5 representations x 5 seeds)
- [x] G2: Adversarial evaluation documented (threat model, ACA, adaptive scenarios)
- [x] G3: UL breadth demonstrated (6 anomaly methods + 4 DR methods from 3 families)
- [x] G4: Reproducibility verified (`reproduce.sh` generates identical results)
- [ ] G5: Publication-ready (blog post, findings doc, figures) — blog draft done, not published

## CS 7641 Rigor Elements
- [x] Multi-seed (5 seeds: 42, 123, 456, 789, 1024; mean +/- std)
- [x] Hypothesis pre-registration (5 hypotheses, falsification criteria)
- [x] Ablation (per-detector, per-representation comparison)
- [x] Figures generated from data (make_report_figures.py from JSON)
- [x] Matched compute (same data/pipeline for all detector comparisons)
- [ ] Statistical tests (paired t-tests with Bonferroni) — planned, not yet computed
- [ ] Provenance tracking (SHA-256 in Artifact Registry) — placeholders added

## Deliverables
- [x] All 150 experiment runs completed
- [x] FINDINGS.md with RQ1-RQ4 answers
- [x] Trust score calibrated on validation set
- [x] API functional (scan, report, health endpoints)
- [x] Blog post drafted
- [x] All tests passing (pytest green)
- [x] Claim strength tags on all quantitative claims
- [x] Hypothesis resolutions table in FINDINGS.md
- [x] Negative / unexpected results documented
- [x] Claims on synthetic data section

## CS 7641 Connection
- [x] UL methods directly applied (GMM, PCA, ICA, UMAP, RP)
- [x] Comparison matrix mirrors UL Report methodology
- [x] Dimensionality reduction findings replicated or extended (FALSIFIED: DR hurts)

## v3.0 Governance Documents
- [x] CONTENT_PLAN.md (publication pipeline, channel mapping)
- [x] FIGURES_TABLES_CONTRACT.md (4 figures documented)
- [x] STATISTICAL_ANALYSIS_SPEC.md (5-seed status, formal test plan)
- [x] CLAIM_STRENGTH_SPEC.md (11 claims registered)
- [x] Content hooks table in FINDINGS.md
- [x] Artifact registry with SHA-256 placeholders

## v3.0 Conference / Publication Section
- [x] Conference abstract (blog/conference_abstract.md)
- [x] Blog draft (~1,200 words)
- [x] LinkedIn post
- [x] Substack intro
- [ ] BSides CFP submission
- [ ] Slide deck (15-20 slides)
- [ ] Speaker notes
- [ ] Demo video (trust score walkthrough, 3-5 minutes)

## Completion Score

**Checked: 25 / 31 = 81%**

### Priority Upgrades (to reach 90%)
1. Compute formal p-values for paired comparisons (adds statistical tests)
2. Populate SHA-256 hashes in Artifact Registry (adds provenance)
3. Submit BSides CFP
4. Record demo video
