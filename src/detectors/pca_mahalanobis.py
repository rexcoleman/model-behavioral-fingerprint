"""PCA + Mahalanobis distance anomaly detector."""

from __future__ import annotations

import numpy as np
from sklearn.decomposition import PCA


class PCAMahalanobisDetector:
    """Anomaly detector using PCA projection + Mahalanobis distance.

    Projects data into PCA space, then computes Mahalanobis distance
    from the training distribution center.

    Parameters
    ----------
    n_components : int or float
        Number of PCA components. If float < 1, interpreted as variance ratio.
    random_state : int
        Random seed.
    """

    def __init__(self, n_components: int | float = 0.95, random_state: int = 42):
        self.pca = PCA(n_components=n_components, random_state=random_state)
        self._mean = None
        self._cov_inv = None

    def fit(self, X_train: np.ndarray) -> "PCAMahalanobisDetector":
        """Fit PCA and compute training distribution statistics."""
        X_pca = self.pca.fit_transform(X_train)
        self._mean = X_pca.mean(axis=0)

        cov = np.cov(X_pca, rowvar=False)
        # Regularize for numerical stability
        cov += np.eye(cov.shape[0]) * 1e-6
        self._cov_inv = np.linalg.inv(cov)
        return self

    def score(self, X_test: np.ndarray) -> np.ndarray:
        """Return Mahalanobis distance scores (higher = more anomalous)."""
        X_pca = self.pca.transform(X_test)
        diff = X_pca - self._mean
        # Mahalanobis: sqrt(diff @ cov_inv @ diff.T) per sample
        left = diff @ self._cov_inv
        mahal_sq = np.sum(left * diff, axis=1)
        return np.sqrt(np.maximum(mahal_sq, 0))
