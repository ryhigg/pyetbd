import numpy as np
from numba import njit


@njit
def sample_linear_fdf(mean):
    """Samples an integer from a linear FDF.

    Args:
        mean (int): mean of the FDF

    Returns:
        int: random value drawn from the linear FDF
    """
    return int(3 * mean * (1 - np.sqrt(1 - np.random.rand())) + 0.5)


@njit
def sample_exponential(mean):
    """Samples an integer from an exponential distribution.

    Args:
        mean (int): mean of the exponential distribution

    Returns:
        float: random value drawn from the exponential distribution
    """
    return np.random.exponential(mean)


@njit
def fixed_value(value):
    """Returns the value passed to it.

        Note: this function is used for fixed schedules since they take a function as an argument.

    Args:
        value (int): value to return

    Returns:
        int: the value
    """
    return value
