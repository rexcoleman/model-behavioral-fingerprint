"""Extract layer activations from a model on reference inputs.

For the scaffold, this module defines the interface. Real model extraction
(hooking into PyTorch forward passes) is added when TrojAI data is available.
"""

from __future__ import annotations

import numpy as np


class ActivationExtractor:
    """Extract flattened activation vectors from specified model layers.

    Parameters
    ----------
    layer_names : list[str]
        Names of layers to hook (e.g., ["layer2", "layer4", "fc"]).
    """

    def __init__(self, layer_names: list[str] | None = None):
        self.layer_names = layer_names or ["early", "middle", "final"]
        self._activations: dict[str, np.ndarray] = {}

    def extract(self, model, reference_inputs: np.ndarray) -> np.ndarray:
        """Extract activations from model on reference inputs.

        Parameters
        ----------
        model : object
            A model object. For scaffold testing, pass None and use
            ``extract_synthetic`` instead.
        reference_inputs : np.ndarray
            Input array of shape (n_inputs, *input_shape).

        Returns
        -------
        np.ndarray
            Feature matrix of shape (n_inputs, n_features) where n_features
            is the total flattened activation size across all hooked layers.
        """
        raise NotImplementedError(
            "Real model extraction requires PyTorch hooks. "
            "Use extract_synthetic() for testing."
        )

    @staticmethod
    def extract_synthetic(
        n_samples: int = 100,
        n_features: int = 512,
        seed: int = 42,
    ) -> np.ndarray:
        """Generate synthetic activation-like features for testing.

        Parameters
        ----------
        n_samples : int
            Number of reference input samples.
        n_features : int
            Dimensionality of flattened activations.
        seed : int
            Random seed for reproducibility.

        Returns
        -------
        np.ndarray
            Synthetic feature matrix of shape (n_samples, n_features).
        """
        rng = np.random.RandomState(seed)
        return rng.randn(n_samples, n_features).astype(np.float32)
