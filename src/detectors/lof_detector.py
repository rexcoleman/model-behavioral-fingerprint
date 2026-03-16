"""Local Outlier Factor anomaly detector wrapper."""

from __future__ import annotations

import numpy as np
from sklearn.neighbors import LocalOutlierFactor


class LOFDetector:
    """Local Outlier Factor anomaly detector.

    Parameters
    ----------
    n_neighbors : int
        Number of neighbors for LOF computation.
    contamination : float
        Expected proportion of outliers.
    novelty : bool
        Must be True to use predict/score on new data.
    """

    def __init__(
        self,
        n_neighbors: int = 20,
        contamination: float = 0.1,
    ):
        self.model = LocalOutlierFactor(
            n_neighbors=n_neighbors,
            contamination=contamination,
            novelty=True,
        )

    def fit(self, X_train: np.ndarray) -> "LOFDetector":
        """Fit on reference feature matrix."""
        self.model.fit(X_train)
        return self

    def score(self, X_test: np.ndarray) -> np.ndarray:
        """Return anomaly scores (higher = more anomalous).

        LOF score_samples returns negative scores for anomalies, so we negate.
        """
        return -self.model.score_samples(X_test)
