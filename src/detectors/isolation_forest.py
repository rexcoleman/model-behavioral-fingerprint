"""Isolation Forest anomaly detector wrapper."""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import IsolationForest as _IsolationForest


class IsolationForestDetector:
    """Isolation Forest anomaly detector.

    Anomaly score: higher = more anomalous (negated sklearn convention).

    Parameters
    ----------
    contamination : float
        Expected proportion of outliers in training data.
    n_estimators : int
        Number of isolation trees.
    random_state : int
        Random seed.
    """

    def __init__(
        self,
        contamination: float = 0.1,
        n_estimators: int = 100,
        random_state: int = 42,
    ):
        self.model = _IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=random_state,
        )

    def fit(self, X_train: np.ndarray) -> "IsolationForestDetector":
        """Fit on reference feature matrix."""
        self.model.fit(X_train)
        return self

    def score(self, X_test: np.ndarray) -> np.ndarray:
        """Return anomaly scores (higher = more anomalous).

        sklearn returns negative scores for anomalies, so we negate.
        """
        return -self.model.score_samples(X_test)
