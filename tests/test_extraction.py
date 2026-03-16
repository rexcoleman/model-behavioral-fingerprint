"""Tests for feature extraction modules."""

from __future__ import annotations

import numpy as np
import pytest

from src.extraction.activation_extractor import ActivationExtractor
from src.extraction.output_distribution import OutputDistributionExtractor
from src.extraction.gradient_norms import GradientNormExtractor


class TestActivationExtractor:
    def test_synthetic_shape(self):
        """Synthetic activations have correct shape."""
        X = ActivationExtractor.extract_synthetic(n_samples=50, n_features=256)
        assert X.shape == (50, 256)
        assert X.dtype == np.float32

    def test_reproducibility(self):
        """Same seed produces same output."""
        X1 = ActivationExtractor.extract_synthetic(seed=99)
        X2 = ActivationExtractor.extract_synthetic(seed=99)
        np.testing.assert_array_equal(X1, X2)


class TestOutputDistribution:
    def test_softmax_sums_to_one(self):
        """Softmax output probabilities sum to 1 for each sample."""
        logits = np.random.randn(20, 10)
        probs = OutputDistributionExtractor.softmax(logits)
        sums = probs.sum(axis=-1)
        np.testing.assert_allclose(sums, 1.0, atol=1e-6)

    def test_stats_shape(self):
        """Output distribution stats have shape (n_samples, 3)."""
        features = OutputDistributionExtractor.extract_synthetic(n_samples=30, n_classes=5)
        assert features.shape == (30, 3)


class TestGradientNorms:
    def test_synthetic_positive(self):
        """Gradient norms are positive."""
        G = GradientNormExtractor.extract_synthetic(n_samples=40, n_layers=5)
        assert G.shape == (40, 5)
        assert (G > 0).all()
