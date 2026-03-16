"""Gaussian Mixture Model anomaly detector."""

from __future__ import annotations

import numpy as np
from sklearn.mixture import GaussianMixture


class GMMDetector:
    """GMM-based anomaly detector.

    Anomaly score = negative log-likelihood (higher = more anomalous).

    Parameters
    ----------
    n_components : int
        Number of Gaussian components.
    random_state : int
        Random seed.
    """

    def __init__(self, n_components: int = 3, reg_covar: float = 1e-4, random_state: int = 42):
        self.model = GaussianMixture(
            n_components=n_components,
            reg_covar=reg_covar,
            random_state=random_state,
        )

    def fit(self, X_train: np.ndarray) -> "GMMDetector":
        """Fit GMM on reference feature matrix."""
        self.model.fit(X_train)
        return self

    def score(self, X_test: np.ndarray) -> np.ndarray:
        """Return anomaly scores (higher = more anomalous).

        GMM score_samples returns log-likelihood; negate so higher = worse.
        """
        return -self.model.score_samples(X_test)
