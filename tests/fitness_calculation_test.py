import unittest
import numpy as np
from pyetbd.rules.fitness_calculation import (
    get_circular_fitness_values,
    get_linear_fitness_values,
)


class TestFitnessCalculation(unittest.TestCase):
    def test_get_circular_fitness_values(self):
        population = np.array([1, 2, 3, 4, 5])
        emitted = 2
        high_pheno = 5

        expected_fitness_values = np.array([1, 0, 1, 2, 2])
        actual_fitness_values = get_circular_fitness_values(
            population, emitted, high_pheno
        )

        np.testing.assert_array_equal(actual_fitness_values, expected_fitness_values)

    def test_get_linear_fitness_values(self):
        population = np.array([1, 2, 3, 4, 5])
        emitted = 2

        expected_fitness_values = np.array([1, 0, 1, 2, 3])
        actual_fitness_values = get_linear_fitness_values(population, emitted)

        np.testing.assert_array_equal(actual_fitness_values, expected_fitness_values)


if __name__ == "__main__":
    unittest.main()
