import numpy as np
from numba import njit
from pyetbd.utils import binary_converter as bc


@njit
def bit_flip_mutate(children_genos: np.ndarray, mut_rate: float) -> np.ndarray:
    """Takes in an array of children genotypes and applies the mutation rule.

    Args:
        children_genos (np.ndarray): an array of children genotypes
        mut_rate (float): the mutation rates

    Returns:
        np.ndarray: the new population of phenotypes
    """

    children_genos_copy = children_genos.copy()
    mutated_population = np.empty(children_genos.shape, dtype=np.int8)
    for i in range(len(children_genos)):
        if np.random.rand() < mut_rate:
            mutated_population[i] = bc.bit_flip(children_genos_copy[i])

        else:
            mutated_population[i] = children_genos_copy[i]

    new_population = bc.convert_binary_to_decimal(mutated_population)

    return new_population
