# Model Behavioral Fingerprinting: Unsupervised Backdoor Detection via Activation Analysis

## BSides / DEF CON Abstract (~200 words)

**Title:** Zero-Label Backdoor Detection: Behavioral Fingerprinting for the AI Model Supply Chain

**Author:** Rex Coleman — Singularity Cybersecurity

**Abstract:**

Organizations increasingly consume pre-trained models from external sources — Hugging Face, model marketplaces, fine-tuning vendors. Static analysis tools like ModelScan catch serialization exploits and known payload patterns, but training-data poisoning backdoors produce no static artifacts. We introduce behavioral fingerprinting: an unsupervised anomaly detection pipeline that analyzes model activations on controlled reference inputs to flag backdoored models without requiring any labeled training data.

We evaluated 6 unsupervised detectors (LOF, Isolation Forest, One-Class SVM, Autoencoder, GMM, PCA+Mahalanobis) across 5 activation representations (raw, PCA, ICA, Random Projection, SimCLR contrastive) over 150 experiment runs with 5-seed validation. Key findings: LOF on raw activations achieves the best mean AUROC (0.622) with 27.5% detection rate at 10% FPR — above chance but below production thresholds. Dimensionality reduction consistently hurts detection, falsifying the hypothesis that compressed representations improve signal. SimCLR contrastive learning scores below chance (AUROC 0.466), while classical non-parametric methods dominate.

We frame results through an Adversarial Controllability Analysis showing defenders hold a structural advantage: they control the probe (reference inputs) while attackers must produce models that behave normally under arbitrary inspection. All code and data are open-source.

**Keywords:** model supply chain security, backdoor detection, unsupervised learning, behavioral fingerprinting, anomaly detection, TrojAI
