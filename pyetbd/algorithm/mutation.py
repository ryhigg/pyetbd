import numpy as np
from numba import njit
from pyetbd.utils import bin_converter as bc


@njit
def mutate_population(children_genos, mut_rate):
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

    new_population = convert_genos_to_phenos(mutated_population)

    return new_population


### HELPER FUNCTIONS ###


@njit
def convert_genos_to_phenos(genos):
    """Converts an array of genotypes to an array of phenotypes.

    Args:
        genos (np.ndarray): an array of genotypes

    Returns:
        np.ndarray: an array of phenotypes
    """
    phenos = np.empty(len(genos), dtype=np.int64)
    for i in range(len(genos)):
        phenos[i] = bc.bin_to_dec(genos[i])

    return phenos
