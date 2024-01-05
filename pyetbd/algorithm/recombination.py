import numpy as np
from numba import njit
from pyetbd.utils import bin_converter as bc


@njit
def recombine_parents(parents, bin_length, recombination_method):
    """Takes in an array of parent pairs and recombines them to create an array of children.

    Args:
        parents (np.ndarray): an array of parent pairs
        bin_length (int): the length of the genotype
        recombination_method (string): the recombination method to use

    Raises:
        ValueError: an invalid recombination_method was passed

    Returns:
        np.ndarray: an array of children genotypes
    """

    children_genos = np.empty((parents.shape[0], bin_length), dtype=np.int8)

    for i in range(parents.shape[0]):
        mother = parents[i][0]
        father = parents[i][1]

        mother_geno = bc.dec_to_bin(mother, bin_length)
        father_geno = bc.dec_to_bin(father, bin_length)

        if recombination_method == "bitwise":
            children_genos[i] = bitwise_combine(mother_geno, father_geno)

        else:
            raise ValueError("recombination_method not implemented")

    return children_genos


### HELPER FUNCTIONS ###


@njit
def bitwise_combine(mother_geno, father_geno):
    """Takes in two genotypes and recombines them bitwise.

    Args:
        mother_geno (np.ndarray): the mother's genotype
        father_geno (np.ndarray): the father's genotype

    Returns:
        np.ndarray: the child's genotype
    """

    child_geno = np.empty(mother_geno.shape, dtype=np.int8)

    for i in range(child_geno.shape[0]):
        if mother_geno[i] == father_geno[i]:
            child_geno[i] = mother_geno[i]
        else:
            child_geno[i] = np.random.randint(0, 2)

    return child_geno
