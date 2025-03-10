import numpy as np
from numba import njit


@njit
def sample_exponential(mean: float) -> float:
    return np.random.exponential(mean)


@njit
def generate_fleshler_hoffman_progression(
    mean: float, num_intervals: int
) -> np.ndarray:
    """
    Generates a Fleshler-Hoffman progression with the given mean and number of intervals."
    """
    progression = np.zeros(num_intervals)
    for i in range(1, num_intervals + 1):
        # Handle the case where (num_intervals - i) is 0
        if (num_intervals - i) == 0:
            term = (
                1
                + np.log(num_intervals)
                + (num_intervals - i) * np.log(1)
                - (num_intervals - i + 1) * np.log(1)
            )
        else:
            term = (
                1
                + np.log(num_intervals)
                + (num_intervals - i) * np.log(num_intervals - i)
                - (num_intervals - i + 1) * np.log(num_intervals - i + 1)
            )
        interval = mean * term
        progression[i - 1] = interval
    return progression
