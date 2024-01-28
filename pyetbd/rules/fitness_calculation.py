from numba import njit
import numpy as np


@njit
def get_circular_fitness_values(
    population: np.ndarray, emitted: int, high_pheno: int
) -> np.ndarray:
    """Calculates the fitness values for a population based on a circular fitness landscape.

    Args:
        population (np.ndarray): a population of potential behaviors (comes from organism object)
        emitted (int): the emitted behavior
        high_pheno (int): the maximum possible phenotype

    Returns:
        np.ndarray: an array of fitness values for the population
    """

    fitness_values = np.empty(len(population), dtype=np.int64)

    for i in range(len(population)):
        linear_fitness = np.abs(population[i] - emitted)
        wrapped_fitness = high_pheno - linear_fitness

        fitness_values[i] = np.minimum(linear_fitness, wrapped_fitness)

    return fitness_values


@njit
def get_linear_fitness_values(population: np.ndarray, emitted: int) -> np.ndarray:
    """Calculates the fitness values for a population based on a linear fitness landscape.

    Args:
        population (np.ndarray): a population of potential behaviors (comes from organism object)
        emitted (int): the emitted behavior
        high_pheno (int): the maximum possible phenotype

    Returns:
        np.ndarray: an array of fitness values for the population
    """

    fitness_values = np.empty(len(population), dtype=np.int64)

    for i in range(len(population)):
        fitness_values[i] = np.abs(population[i] - emitted)

    return fitness_values
