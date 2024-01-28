import numpy as np
from numba import njit


@njit
def sample_linear_fdf(mean: float) -> int:
    return int(3 * mean * (1 - np.sqrt(1 - np.random.rand())) + 0.5)


@njit
def sample_exponential_fdf(mean: float) -> int:
    return int(np.random.exponential(mean) + 0.5)
