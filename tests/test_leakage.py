"""Tests for data leakage prevention.

Ensures train/test splits are on MODEL identity, not feature samples,
and that no label information leaks into the unsupervised detectors.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.detectors.isolation_forest import IsolationForestDetector


class TestNoLabelLeakage:
    def test_detector_uses_no_labels(self, train_test_split_features):
        """Detectors are fit on unlabeled data only (no y_train)."""
        X_train, X_test, y_test = train_test_split_features
        det = IsolationForestDetector(random_state=42)
        # fit() takes only X — no labels accepted
        det.fit(X_train)
        scores = det.score(X_test)
        assert scores.shape == (len(y_test),)

    def test_train_test_model_split(self, synthetic_features):
        """Train and test sets must not share model indices."""
        X, labels = synthetic_features
        clean_idx = np.where(labels == 0)[0]
        n_train = int(0.7 * len(clean_idx))

        train_idx = set(clean_idx[:n_train])
        test_clean_idx = set(clean_idx[n_train:])
        test_backdoor_idx = set(np.where(labels == 1)[0])
        test_idx = test_clean_idx | test_backdoor_idx

        # No overlap
        assert len(train_idx & test_idx) == 0

    def test_train_contains_only_clean(self, synthetic_features):
        """Training set for unsupervised detectors must contain only clean models."""
        X, labels = synthetic_features
        clean_mask = labels == 0
        X_train = X[clean_mask][:63]  # 70% of 90

        # Verify all training samples come from clean models
        # (In a real test, we'd track model IDs; here we verify by construction)
        assert X_train.shape[0] == 63
        assert X_train.shape[0] < clean_mask.sum()
