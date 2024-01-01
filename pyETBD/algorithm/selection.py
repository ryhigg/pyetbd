import numpy as np
from numba import njit
from pyetbd.utils import equations


@njit
def randomly_select_parents(population):
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


@njit
def fitness_search_selection(
    population, fdf_type, fdf_mean, fitness_landscape, high_pheno, emitted
):
    """Selects parents from the population based on their fitness using a search method. In this method, fitness values are drawn from the FDF and behaviors with matching fitness values are put into a pool. One parent is then randomly selected from the pool. This process is repeated until two parents are selected. This whole process is repeated until there are the same number of parent pairs as there are individuals in the population.

    Args:
        population (np.ndarray): a population of potential behaviors (comes from organism object)
        fdf_type (string): the FDF form to use
        fdf_mean (int): the mean of the FDF
        fitness_landscape (string): the fitness landscape to use
        high_pheno (int): the maximum possible phenotype
        emitted (int): the emitted behavior

    Raises:
        ValueError: an invalid fitness_landscape was passed
        ValueError: an invalid fdf_type was passed

    Returns:
        np.ndarray: An array of parent pairs that is the same length as the population
    """

    parents = np.empty((len(population), 2), dtype=np.int64)

    if fitness_landscape == "circular":
        fitness_values = get_circular_fitness_values(population, emitted, high_pheno)

    else:
        raise ValueError("fitness_landscape not implemented")

    for i in range(len(population)):
        j = 0
        while j < 2:
            if fdf_type == "linear":
                drawn_fitness = equations.sample_linear_fdf(fdf_mean)

                matching_indices = np.where(fitness_values == drawn_fitness)[0]

                if len(matching_indices) > 0:
                    parents[i][j] = population[np.random.choice(matching_indices)]
                    j += 1

            else:
                raise ValueError("fdf_type not implemented")

    return parents


### HELPER FUNCTIONS ###


@njit
def get_circular_fitness_values(population, emitted, high_pheno):
    """Calculates the fitness values for a population based on a circular fitness landscape.

    Args:
        population (np.ndarray): a population of potential behaviors (comes from organism object)
        emitted (int): the emitted behavior
        high_pheno (int): the maximum possible phenotypeq

    Returns:
        np.ndarray: an array of fitness values for the population
    """

    fitness_values = np.empty(len(population), dtype=np.int64)

    for i in range(len(population)):
        linear_fitness = np.abs(population[i] - emitted)
        wrapped_fitness = high_pheno - linear_fitness

        fitness_values[i] = np.minimum(linear_fitness, wrapped_fitness)

    return fitness_values
