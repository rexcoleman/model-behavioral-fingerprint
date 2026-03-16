"""Anomaly detectors for model behavioral fingerprinting.

All detectors implement a common interface:
    .fit(X_train)               — fit on reference (clean) feature matrix
    .score(X_test) -> scores    — return anomaly scores (higher = more anomalous)
"""
