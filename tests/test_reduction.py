"""Tests for dimensionality reduction methods."""

from __future__ import annotations

import numpy as np
import pytest

from src.reduction.reducers import PCAReducer, ICAReducer, RandomProjectionReducer, get_reducer


class TestPCAReducer:
    def test_reduces_dimensions(self, synthetic_features):
        X, _ = synthetic_features
        reducer = PCAReducer(n_components=50, random_state=42)
        X_reduced = reducer.fit_transform(X)
        assert X_reduced.shape == (100, 50)

    def test_transform_consistent(self, synthetic_features):
        X, _ = synthetic_features
        reducer = PCAReducer(n_components=50, random_state=42)
        reducer.fit_transform(X[:80])
        X_new = reducer.transform(X[80:])
        assert X_new.shape == (20, 50)


class TestICAReducer:
    def test_reduces_dimensions(self, synthetic_features):
        X, _ = synthetic_features
        reducer = ICAReducer(n_components=50, random_state=42)
        X_reduced = reducer.fit_transform(X)
        assert X_reduced.shape == (100, 50)


class TestRandomProjectionReducer:
    def test_reduces_dimensions(self, synthetic_features):
        X, _ = synthetic_features
        reducer = RandomProjectionReducer(n_components=50, random_state=42)
        X_reduced = reducer.fit_transform(X)
        assert X_reduced.shape == (100, 50)


class TestGetReducer:
    def test_known_reducer(self):
        reducer = get_reducer("pca", n_components=10, random_state=42)
        assert isinstance(reducer, PCAReducer)

    def test_unknown_reducer(self):
        with pytest.raises(ValueError, match="Unknown reducer"):
            get_reducer("nonexistent")
