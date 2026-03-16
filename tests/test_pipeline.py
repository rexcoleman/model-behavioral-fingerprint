"""End-to-end pipeline tests: extract -> reduce -> detect."""

from __future__ import annotations

import numpy as np
import pytest

from src.extraction.activation_extractor import ActivationExtractor
from src.extraction.output_distribution import OutputDistributionExtractor
from src.extraction.gradient_norms import GradientNormExtractor
from src.reduction.reducers import PCAReducer
from src.detectors.isolation_forest import IsolationForestDetector
from src.detectors.gmm_detector import GMMDetector
from src.trust_score import TrustScorer


class TestEndToEndPipeline:
    def test_extract_reduce_detect(self):
        """Full pipeline: synthetic extraction -> PCA reduction -> IF detection."""
        # Extract
        act = ActivationExtractor.extract_synthetic(100, 512, seed=42)
        out = OutputDistributionExtractor.extract_synthetic(100, 10, seed=42)
        grad = GradientNormExtractor.extract_synthetic(100, 3, seed=42)
        X = np.hstack([act, out, grad])
        assert X.shape == (100, 518)

        # Split: 70 train, 30 test
        X_train, X_test = X[:70], X[70:]

        # Reduce
        reducer = PCAReducer(n_components=50, random_state=42)
        X_train_r = reducer.fit_transform(X_train)
        X_test_r = reducer.transform(X_test)
        assert X_train_r.shape == (70, 50)
        assert X_test_r.shape == (30, 50)

        # Detect
        det = IsolationForestDetector(random_state=42)
        det.fit(X_train_r)
        scores = det.score(X_test_r)
        assert scores.shape == (30,)
        assert np.isfinite(scores).all()

    def test_multi_detector_pipeline(self):
        """Run multiple detectors and aggregate via TrustScorer."""
        X = ActivationExtractor.extract_synthetic(80, 64, seed=42)
        X_train, X_test = X[:60], X[60:]

        # Fit two detectors
        det_if = IsolationForestDetector(random_state=42)
        det_if.fit(X_train)
        det_gmm = GMMDetector(n_components=2, random_state=42)
        det_gmm.fit(X_train)

        # Score
        ref_scores = {
            "if": det_if.score(X_train),
            "gmm": det_gmm.score(X_train),
        }
        test_scores = {
            "if": det_if.score(X_test),
            "gmm": det_gmm.score(X_test),
        }

        # Aggregate
        scorer = TrustScorer()
        scorer.fit(ref_scores)
        trust = scorer.score(test_scores)
        assert trust.shape == (20,)
        assert (trust >= 0).all()
        assert (trust <= 100).all()

    def test_pipeline_different_seeds_vary(self):
        """Different seeds produce different (but valid) results."""
        X = ActivationExtractor.extract_synthetic(50, 32, seed=42)
        X_train, X_test = X[:40], X[40:]

        scores_list = []
        for seed in [42, 123, 456]:
            det = IsolationForestDetector(random_state=seed)
            det.fit(X_train)
            scores_list.append(det.score(X_test))

        # Different seeds should produce different scores
        assert not np.allclose(scores_list[0], scores_list[1])
        assert not np.allclose(scores_list[0], scores_list[2])
