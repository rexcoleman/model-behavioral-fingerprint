"""Compute gradient norms per layer for a model on reference inputs."""

from __future__ import annotations

import numpy as np


class GradientNormExtractor:
    """Extract L2 gradient norms of loss w.r.t. each layer's parameters.

    For the scaffold, provides synthetic gradient norm features.
    Real extraction requires PyTorch autograd.
    """

    def __init__(self, layer_names: list[str] | None = None):
        self.layer_names = layer_names or ["early", "middle", "final"]

    def extract(self, model, reference_inputs: np.ndarray, labels: np.ndarray) -> np.ndarray:
        """Extract gradient norm features from a real model.

        Returns
        -------
        np.ndarray
            Shape (n_inputs, n_layers) with L2 gradient norms.
        """
        raise NotImplementedError(
            "Real gradient extraction requires PyTorch autograd. "
            "Use extract_synthetic() for testing."
        )

    @staticmethod
    def extract_synthetic(
        n_samples: int = 100,
        n_layers: int = 3,
        seed: int = 42,
    ) -> np.ndarray:
        """Generate synthetic gradient norm features.

        Returns
        -------
        np.ndarray
            Shape (n_samples, n_layers) of positive gradient norms.
        """
        rng = np.random.RandomState(seed)
        # Gradient norms are positive; use lognormal for realistic distribution
        return np.abs(rng.lognormal(mean=0.0, sigma=1.0, size=(n_samples, n_layers))).astype(
            np.float32
        )
