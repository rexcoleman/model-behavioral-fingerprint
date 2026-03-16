"""Autoencoder anomaly detector using PyTorch.

Anomaly score = reconstruction error (MSE). Higher = more anomalous.
Falls back to a simple sklearn-based approach if torch is unavailable.
"""

from __future__ import annotations

import numpy as np

try:
    import torch
    import torch.nn as nn

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class AutoencoderDetector:
    """Autoencoder-based anomaly detector.

    Uses reconstruction error (MSE) as anomaly score.

    Parameters
    ----------
    encoding_dim : int
        Bottleneck dimension.
    epochs : int
        Training epochs.
    lr : float
        Learning rate.
    random_state : int
        Random seed.
    """

    def __init__(
        self,
        encoding_dim: int = 32,
        epochs: int = 50,
        lr: float = 1e-3,
        random_state: int = 42,
    ):
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.lr = lr
        self.random_state = random_state
        self._model = None
        self._input_dim = None

    def _build_model(self, input_dim: int):
        """Build the autoencoder architecture."""
        if not TORCH_AVAILABLE:
            return None

        torch.manual_seed(self.random_state)

        class AE(nn.Module):
            def __init__(self, in_dim, enc_dim):
                super().__init__()
                mid = max(enc_dim * 2, in_dim // 4)
                self.encoder = nn.Sequential(
                    nn.Linear(in_dim, mid),
                    nn.ReLU(),
                    nn.Linear(mid, enc_dim),
                    nn.ReLU(),
                )
                self.decoder = nn.Sequential(
                    nn.Linear(enc_dim, mid),
                    nn.ReLU(),
                    nn.Linear(mid, in_dim),
                )

            def forward(self, x):
                z = self.encoder(x)
                return self.decoder(z)

        return AE(input_dim, self.encoding_dim)

    def fit(self, X_train: np.ndarray) -> "AutoencoderDetector":
        """Fit autoencoder on reference feature matrix."""
        self._input_dim = X_train.shape[1]

        if not TORCH_AVAILABLE:
            # Fallback: store training mean/std for simple distance scoring
            self._mean = X_train.mean(axis=0)
            self._std = X_train.std(axis=0) + 1e-8
            return self

        self._model = self._build_model(self._input_dim)
        optimizer = torch.optim.Adam(self._model.parameters(), lr=self.lr)
        criterion = nn.MSELoss()

        X_tensor = torch.FloatTensor(X_train)
        self._model.train()
        for _ in range(self.epochs):
            optimizer.zero_grad()
            recon = self._model(X_tensor)
            loss = criterion(recon, X_tensor)
            loss.backward()
            optimizer.step()

        self._model.eval()
        return self

    def score(self, X_test: np.ndarray) -> np.ndarray:
        """Return anomaly scores (reconstruction error, higher = more anomalous)."""
        if not TORCH_AVAILABLE:
            # Fallback: Mahalanobis-like distance from training distribution
            normalized = (X_test - self._mean) / self._std
            return np.mean(normalized**2, axis=1)

        with torch.no_grad():
            X_tensor = torch.FloatTensor(X_test)
            recon = self._model(X_tensor)
            mse = torch.mean((X_tensor - recon) ** 2, dim=1)
        return mse.numpy()
