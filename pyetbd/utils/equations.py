import numpy as np
from numba import njit


@njit
def sample_exponential(mean: float) -> float:
    return np.random.exponential(mean)
