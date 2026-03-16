"""Aggregate anomaly scores from 6 detectors into a single 0-100 trust score.

Higher score = more suspicious (more likely to be backdoored/tampered).
"""

from __future__ import annotations

import numpy as np
from scipy import stats


class TrustScorer:
    """Aggregate multiple detector scores into a unified trust score.

    Algorithm:
    1. Normalize each detector's scores to [0, 1] via percentile rank
       against the reference (training) distribution.
    2. Average normalized scores across detectors.
    3. Scale to 0-100.

    Parameters
    ----------
    detector_names : list[str] | None
        Names of detectors. Used for reporting only.
    """

    def __init__(self, detector_names: list[str] | None = None):
        self.detector_names = detector_names or []
        self._reference_scores: dict[str, np.ndarray] = {}

    def fit(self, reference_scores: dict[str, np.ndarray]) -> "TrustScorer":
        """Store reference score distributions for percentile normalization.

        Parameters
        ----------
        reference_scores : dict[str, np.ndarray]
            Mapping of detector_name -> anomaly scores on reference (training) data.
        """
        self._reference_scores = {k: v.copy() for k, v in reference_scores.items()}
        if not self.detector_names:
            self.detector_names = list(reference_scores.keys())
        return self

    def score(self, test_scores: dict[str, np.ndarray]) -> np.ndarray:
        """Compute trust scores for test samples.

        Parameters
        ----------
        test_scores : dict[str, np.ndarray]
            Mapping of detector_name -> anomaly scores on test data.

        Returns
        -------
        np.ndarray
            Trust scores in [0, 100]. Higher = more suspicious.
        """
        if not self._reference_scores:
            raise RuntimeError("Must call fit() with reference scores first.")

        normalized = []
        for name in self._reference_scores:
            ref = self._reference_scores[name]
            test = test_scores[name]
            # Percentile rank: fraction of reference scores <= each test score
            pct = np.array([
                stats.percentileofscore(ref, s, kind="rank") / 100.0
                for s in test
            ])
            normalized.append(pct)

        # Average across detectors, scale to 0-100
        avg = np.mean(normalized, axis=0)
        trust = np.clip(avg * 100, 0, 100)
        return trust

    def score_single(self, test_scores: dict[str, float]) -> float:
        """Score a single sample.

        Parameters
        ----------
        test_scores : dict[str, float]
            Mapping of detector_name -> single anomaly score.

        Returns
        -------
        float
            Trust score in [0, 100].
        """
        arrays = {k: np.array([v]) for k, v in test_scores.items()}
        return float(self.score(arrays)[0])
