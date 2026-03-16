"""Shared test fixtures for model behavioral fingerprinting tests.

Generates synthetic feature matrices simulating clean + 10% backdoored models.
"""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def rng():
    """Fixed random state for reproducibility."""
    return np.random.RandomState(42)


@pytest.fixture
def synthetic_features(rng):
    """Synthetic feature matrix: 100 samples x 512 features.

    90 clean models (drawn from N(0, 1)) + 10 backdoored models
    (drawn from N(0, 1) with a shifted mean on a subset of features
    to simulate behavioral anomalies).
    """
    n_clean = 90
    n_backdoor = 10
    n_features = 512

    X_clean = rng.randn(n_clean, n_features).astype(np.float32)

    # Backdoored models: shift mean on first 50 features
    X_backdoor = rng.randn(n_backdoor, n_features).astype(np.float32)
    X_backdoor[:, :50] += 3.0  # Detectable shift

    X = np.vstack([X_clean, X_backdoor])
    labels = np.zeros(n_clean + n_backdoor, dtype=int)
    labels[n_clean:] = 1

    return X, labels


@pytest.fixture
def train_test_split_features(synthetic_features):
    """Split synthetic features into train (70% clean only) and test (all)."""
    X, labels = synthetic_features
    clean_mask = labels == 0

    # Train on 70% of clean models
    n_train = int(0.7 * clean_mask.sum())
    X_train = X[clean_mask][:n_train]

    # Test on remaining clean + all backdoored
    X_test = np.vstack([X[clean_mask][n_train:], X[~clean_mask]])
    y_test = np.concatenate([
        np.zeros(clean_mask.sum() - n_train, dtype=int),
        np.ones((~clean_mask).sum(), dtype=int),
    ])

    return X_train, X_test, y_test


@pytest.fixture
def small_features(rng):
    """Small feature matrix for fast tests: 30 samples x 20 features."""
    n_clean = 25
    n_backdoor = 5
    n_features = 20

    X_clean = rng.randn(n_clean, n_features).astype(np.float32)
    X_backdoor = rng.randn(n_backdoor, n_features).astype(np.float32)
    X_backdoor[:, :5] += 3.0

    X = np.vstack([X_clean, X_backdoor])
    labels = np.zeros(n_clean + n_backdoor, dtype=int)
    labels[n_clean:] = 1

    return X, labels


@pytest.fixture
def mock_activation_data(rng):
    """Mock activation data: 50 samples x 256 features."""
    return rng.randn(50, 256).astype(np.float32)
