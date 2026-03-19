# Substack Intro — FP-13 Model Behavioral Fingerprinting

---

**Subject line:** The pre-trained model you just downloaded might be backdoored

ModelScan checks for serialization exploits. But what about training-data poisoning that leaves no static trace?

I built a behavioral fingerprinting pipeline -- probe the model, collect activations, run 6 unsupervised anomaly detectors -- and tested it across 150 experiments. The results challenged three assumptions: dimensionality reduction hurts (does not help), classical methods beat autoencoders at small scale, and contrastive learning (SimCLR) fails below chance.

The takeaway: a zero-label, 6-detector ensemble can flag 22-28% of backdoored models at 10% FPR. Not production-ready yet, but a real signal that static analysis cannot provide.

In this post, I break down what worked, what failed, and what it means for model supply chain security.

[Read the full post]

---

> **Preview text:** "LOF beats autoencoders. DR makes it worse. SimCLR fails below chance. 150 experiments on model backdoor detection."
