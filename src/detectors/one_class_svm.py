"""One-Class SVM anomaly detector wrapper."""

from __future__ import annotations

import numpy as np
from sklearn.svm import OneClassSVM as _OneClassSVM


class OneClassSVMDetector:
    """One-Class SVM anomaly detector.

    Parameters
    ----------
    kernel : str
        Kernel type (rbf, linear, poly).
    nu : float
        Upper bound on the fraction of training errors.
    gamma : str or float
        Kernel coefficient.
    """

    def __init__(
        self,
        kernel: str = "rbf",
        nu: float = 0.1,
        gamma: str = "scale",
    ):
        self.model = _OneClassSVM(kernel=kernel, nu=nu, gamma=gamma)

    def fit(self, X_train: np.ndarray) -> "OneClassSVMDetector":
        """Fit on reference feature matrix."""
        self.model.fit(X_train)
        return self

    def score(self, X_test: np.ndarray) -> np.ndarray:
        """Return anomaly scores (higher = more anomalous).

        sklearn returns negative scores for anomalies, so we negate.
        """
        return -self.model.score_samples(X_test)
