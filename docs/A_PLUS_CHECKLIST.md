# A+ Checklist — FP-13 Model Behavioral Fingerprinting

## Quality Gates

- [ ] G0: Hypotheses pre-registered before any experiments
- [ ] G1: Experiment contract complete (6 detectors x 5 representations x 5 seeds)
- [ ] G2: Adversarial evaluation documented (threat model, ACA, adaptive scenarios)
- [ ] G3: UL breadth demonstrated (6 anomaly methods + 4 DR methods from 3 families)
- [ ] G4: Reproducibility verified (`reproduce.sh` generates identical results)
- [ ] G5: Publication-ready (blog post, findings doc, figures)

## Deliverables

- [ ] All 150 experiment runs completed
- [ ] FINDINGS.md with RQ1-RQ4 answers
- [ ] Trust score calibrated on validation set
- [ ] API functional (scan, report, health endpoints)
- [ ] Blog post drafted
- [ ] All tests passing (pytest green)

## CS 7641 Connection

- [ ] UL methods directly applied (GMM, PCA, ICA, UMAP, RP)
- [ ] Comparison matrix mirrors UL Report methodology
- [ ] Dimensionality reduction findings replicated or extended
