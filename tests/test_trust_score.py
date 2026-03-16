"""Tests for trust score aggregation."""

from __future__ import annotations

import numpy as np
import pytest

from src.trust_score import TrustScorer


class TestTrustScorer:
    def test_score_in_range(self):
        """Trust scores must be in [0, 100]."""
        rng = np.random.RandomState(42)
        ref_scores = {
            "det_a": rng.randn(100),
            "det_b": rng.randn(100),
        }
        test_scores = {
            "det_a": rng.randn(20),
            "det_b": rng.randn(20),
        }
        scorer = TrustScorer()
        scorer.fit(ref_scores)
        trust = scorer.score(test_scores)
        assert trust.shape == (20,)
        assert (trust >= 0).all()
        assert (trust <= 100).all()

    def test_higher_means_more_suspicious(self):
        """Models with higher anomaly scores should get higher trust scores."""
        ref_scores = {
            "det_a": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
        }
        # Normal sample (low anomaly score)
        normal = {"det_a": np.array([1.5])}
        # Suspicious sample (high anomaly score)
        suspicious = {"det_a": np.array([10.0])}

        scorer = TrustScorer()
        scorer.fit(ref_scores)

        score_normal = scorer.score(normal)[0]
        score_suspicious = scorer.score(suspicious)[0]
        assert score_suspicious > score_normal

    def test_single_score(self):
        """score_single returns a float in [0, 100]."""
        ref_scores = {
            "det_a": np.linspace(0, 10, 50),
            "det_b": np.linspace(0, 5, 50),
        }
        scorer = TrustScorer()
        scorer.fit(ref_scores)
        result = scorer.score_single({"det_a": 5.0, "det_b": 2.5})
        assert isinstance(result, float)
        assert 0 <= result <= 100
