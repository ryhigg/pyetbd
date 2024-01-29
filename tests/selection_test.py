import unittest
import numpy as np
import logging
from pyetbd.rules.selection import fitness_search_selection, randomly_select_parents
from pyetbd.rules.fitness_calculation import get_circular_fitness_values
from pyetbd.rules.fdfs import sample_linear_fdf

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("logs/selection_test.log")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)


class TestSelection(unittest.TestCase):
    def setUp(self):
        self.population = np.array([1, 2, 5, 10, 12, 14, 16, 17, 20])
        self.emitted = 5
        self.fitness_values = get_circular_fitness_values(
            self.population, self.emitted, 20
        )
        self.fdf_mean = 2
        self.sample_func = sample_linear_fdf

    def test_fitness_search_selection(self):
        parents = fitness_search_selection(
            self.population, self.fitness_values, self.fdf_mean, self.sample_func
        )

        logger.debug(f"population: {self.population}")
        logger.debug(f"fitness_values: {self.fitness_values}")
        logger.debug(f"parents: {parents}")

        self.assertEqual(parents.shape, (len(self.population), 2))

        expected_possible_parents = np.array([1, 2, 5, 10, 20])
        for i in range(len(parents)):
            # check that all the parents are in the population and that they are in the expected possible parents
            self.assertIn(parents[i][0], self.population)
            self.assertIn(parents[i][1], self.population)
            self.assertIn(parents[i][0], expected_possible_parents)
            self.assertIn(parents[i][1], expected_possible_parents)

    def test_randomly_select_parents(self):
        parents = randomly_select_parents(self.population)
        self.assertEqual(parents.shape, (len(self.population), 2))
        # check that all the parents are in the population
        for i in range(len(parents)):
            self.assertIn(parents[i][0], self.population)
            self.assertIn(parents[i][1], self.population)


if __name__ == "__main__":
    unittest.main()
