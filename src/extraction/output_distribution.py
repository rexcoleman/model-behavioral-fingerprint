"""Extract output (softmax) distributions from a model on reference inputs."""

from __future__ import annotations

import numpy as np


class OutputDistributionExtractor:
    """Extract softmax probability distributions and derived statistics.

    Statistics per input: entropy, max_prob, margin (max - second_max).
    """

    def extract(self, model, reference_inputs: np.ndarray) -> np.ndarray:
        """Extract output distribution features from a real model.

        Returns
        -------
        np.ndarray
            Shape (n_inputs, 3) with columns [entropy, max_prob, margin].
        """
        raise NotImplementedError(
            "Real model extraction requires forward pass. "
            "Use extract_synthetic() for testing."
        )

    @staticmethod
    def softmax(logits: np.ndarray) -> np.ndarray:
        """Compute softmax along last axis."""
        exp = np.exp(logits - logits.max(axis=-1, keepdims=True))
        return exp / exp.sum(axis=-1, keepdims=True)

    @staticmethod
    def compute_stats(probs: np.ndarray) -> np.ndarray:
        """Compute distribution statistics from probability vectors.

        Parameters
        ----------
        probs : np.ndarray
            Probability matrix of shape (n_samples, n_classes).

        Returns
        -------
        np.ndarray
            Shape (n_samples, 3): [entropy, max_prob, margin].
        """
        # Entropy
        log_probs = np.log(probs + 1e-10)
        entropy = -np.sum(probs * log_probs, axis=-1)

        # Max probability
        max_prob = np.max(probs, axis=-1)

        # Margin: difference between top-2 probabilities
        sorted_probs = np.sort(probs, axis=-1)[:, ::-1]
        margin = sorted_probs[:, 0] - sorted_probs[:, 1]

        return np.column_stack([entropy, max_prob, margin]).astype(np.float32)

    @staticmethod
    def extract_synthetic(
        n_samples: int = 100,
        n_classes: int = 10,
        seed: int = 42,
    ) -> np.ndarray:
        """Generate synthetic output distribution features.

        Returns
        -------
        np.ndarray
            Shape (n_samples, 3): [entropy, max_prob, margin].
        """
        rng = np.random.RandomState(seed)
        logits = rng.randn(n_samples, n_classes).astype(np.float32)
        probs = OutputDistributionExtractor.softmax(logits)
        return OutputDistributionExtractor.compute_stats(probs)
