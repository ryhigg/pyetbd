from typing import Callable
import numpy as np
from numba import njit


@njit
def fitness_search_selection(
    population: np.ndarray,
    fitness_values: np.ndarray,
    fdf_mean: float,
    sample_func: Callable,
) -> np.ndarray:
    """This is a helper function for the fitness search selection strategies. It selects parents from the population based on their fitness using a search method. In this method, fitness values are drawn from the FDF and behaviors with matching fitness values are put into a pool. One parent is then randomly selected from the pool. This process is repeated until two parents are selected. This whole process is repeated until there are the same number of parent pairs as there are individuals in the population.

    Args:
        population (np.ndarray): a population of potential behaviors (comes from organism object)
        fitness_values (np.ndarray): an array of fitness values for the population
        fdf_mean (float): the mean of the FDF
        sample_func (function): the function of the FDF to sample from

    Raises:
        Exception: if the function fails to find valid parents after 1000000 iterations

    Returns:
        np.ndarray: An array of parent pairs that is the same length as the population
    """
    parents = np.empty((len(population), 2), dtype=np.int64)

    for i in range(len(population)):
        j = 0
        iterations = 0
        while j < 2:
            # check for infinite loop
            iterations += 1
            if iterations > 1000000:
                print(
                    "Warning: Giddywhoaed in selection.py, fitness_search_selection ailed to find valid parents after 1,000,000 iterations. Bailing out to random selection. This might be because the FDF mean is too low or the mutation rate is too high."
                )
                return randomly_select_parents(population)

            # draw a fitness value from the FDF
            drawn_fitness = sample_func(fdf_mean)

            # find the indices of the population that match the drawn fitness
            matching_indices = np.where(fitness_values == drawn_fitness)[0]

            # if there are any matches, randomly select one and add it to the parents array
            if len(matching_indices) > 0:
                parents[i][j] = population[np.random.choice(matching_indices)]
                j += 1

    return parents


@njit
def randomly_select_parents(population: np.ndarray) -> np.ndarray:
    """Randomly selects parents from the population.

    Args:
        population (np.ndarray): a population of potential behaviors (comes from organism object)

    Returns:
        np.ndarray: An array of parent pairs that is the same length as the population
    """

    parents = np.empty((len(population), 2), dtype=np.int64)

    for i in range(len(population)):
        parents[i] = np.random.choice(population, 2)

    return parents
