"""Tests for all 6 anomaly detectors on synthetic data."""

from __future__ import annotations

import numpy as np
import pytest

from src.detectors.isolation_forest import IsolationForestDetector
from src.detectors.one_class_svm import OneClassSVMDetector
from src.detectors.gmm_detector import GMMDetector
from src.detectors.autoencoder import AutoencoderDetector
from src.detectors.pca_mahalanobis import PCAMahalanobisDetector
from src.detectors.lof_detector import LOFDetector


class TestIsolationForest:
    def test_fit_score(self, train_test_split_features):
        X_train, X_test, y_test = train_test_split_features
        det = IsolationForestDetector(random_state=42)
        det.fit(X_train)
        scores = det.score(X_test)
        assert scores.shape == (len(X_test),)
        assert np.isfinite(scores).all()


class TestOneClassSVM:
    def test_fit_score(self, small_features):
        X, labels = small_features
        X_train = X[labels == 0][:20]
        X_test = X
        det = OneClassSVMDetector()
        det.fit(X_train)
        scores = det.score(X_test)
        assert scores.shape == (len(X_test),)
        assert np.isfinite(scores).all()


class TestGMM:
    def test_fit_score(self, small_features):
        X, labels = small_features
        X_train = X[labels == 0][:20]
        X_test = X
        det = GMMDetector(n_components=2, random_state=42)
        det.fit(X_train)
        scores = det.score(X_test)
        assert scores.shape == (len(X_test),)
        assert np.isfinite(scores).all()


class TestAutoencoder:
    def test_fit_score(self, small_features):
        X, labels = small_features
        X_train = X[labels == 0][:20]
        X_test = X
        det = AutoencoderDetector(encoding_dim=8, epochs=5, random_state=42)
        det.fit(X_train)
        scores = det.score(X_test)
        assert scores.shape == (len(X_test),)
        assert np.isfinite(scores).all()


class TestPCAMahalanobis:
    def test_fit_score(self, train_test_split_features):
        X_train, X_test, y_test = train_test_split_features
        det = PCAMahalanobisDetector(n_components=10, random_state=42)
        det.fit(X_train)
        scores = det.score(X_test)
        assert scores.shape == (len(X_test),)
        assert np.isfinite(scores).all()
        assert (scores >= 0).all()  # Mahalanobis distance is non-negative


class TestLOF:
    def test_fit_score(self, train_test_split_features):
        X_train, X_test, y_test = train_test_split_features
        det = LOFDetector(n_neighbors=10)
        det.fit(X_train)
        scores = det.score(X_test)
        assert scores.shape == (len(X_test),)
        assert np.isfinite(scores).all()
