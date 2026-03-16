"""Dimensionality reduction wrappers: PCA, ICA, UMAP, Random Projection.

All reducers implement a common interface:
    .fit_transform(X) -> X_reduced
    .transform(X) -> X_reduced
"""

from __future__ import annotations

import numpy as np
from sklearn.decomposition import PCA, FastICA
from sklearn.random_projection import GaussianRandomProjection

try:
    from umap import UMAP

    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False


class PCAReducer:
    """PCA dimensionality reduction.

    Parameters
    ----------
    n_components : int or float
        Number of components. Float < 1 = variance ratio to retain.
    random_state : int
        Random seed.
    """

    def __init__(self, n_components: int | float = 50, random_state: int = 42):
        self.model = PCA(n_components=n_components, random_state=random_state)

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.model.fit_transform(X)

    def transform(self, X: np.ndarray) -> np.ndarray:
        return self.model.transform(X)


class ICAReducer:
    """ICA (Independent Component Analysis) dimensionality reduction.

    Parameters
    ----------
    n_components : int
        Number of independent components.
    random_state : int
        Random seed.
    """

    def __init__(self, n_components: int = 50, random_state: int = 42):
        self.model = FastICA(
            n_components=n_components,
            random_state=random_state,
            max_iter=500,
        )

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.model.fit_transform(X)

    def transform(self, X: np.ndarray) -> np.ndarray:
        return self.model.transform(X)


class UMAPReducer:
    """UMAP dimensionality reduction.

    Parameters
    ----------
    n_components : int
        Target dimensionality.
    random_state : int
        Random seed.
    """

    def __init__(self, n_components: int = 50, random_state: int = 42):
        if not UMAP_AVAILABLE:
            raise ImportError("umap-learn is required for UMAPReducer. Install with: pip install umap-learn")
        self.model = UMAP(n_components=n_components, random_state=random_state)

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.model.fit_transform(X)

    def transform(self, X: np.ndarray) -> np.ndarray:
        return self.model.transform(X)


class RandomProjectionReducer:
    """Gaussian Random Projection (JL-lemma) dimensionality reduction.

    Parameters
    ----------
    n_components : int
        Target dimensionality.
    random_state : int
        Random seed.
    """

    def __init__(self, n_components: int = 50, random_state: int = 42):
        self.model = GaussianRandomProjection(
            n_components=n_components,
            random_state=random_state,
        )

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.model.fit_transform(X)

    def transform(self, X: np.ndarray) -> np.ndarray:
        return self.model.transform(X)


# Registry for easy lookup by name
REDUCERS = {
    "pca": PCAReducer,
    "ica": ICAReducer,
    "umap": UMAPReducer,
    "random_projection": RandomProjectionReducer,
}


def get_reducer(name: str, **kwargs):
    """Get a reducer instance by name.

    Parameters
    ----------
    name : str
        One of: pca, ica, umap, random_projection.

    Returns
    -------
    A reducer instance with fit_transform/transform methods.
    """
    if name not in REDUCERS:
        raise ValueError(f"Unknown reducer: {name}. Choose from: {list(REDUCERS.keys())}")
    return REDUCERS[name](**kwargs)
