import unittest
from numpy.testing import assert_array_equal
from numpy import ndarray
from pyetbd.algorithm_strategies.recombination_strategies import BitwiseRecombination
from pyetbd.organisms import Organism
from pyetbd.rules.selection import randomly_select_parents
import logging

# Create a custom logger
logger = logging.getLogger(__name__)
fh = logging.FileHandler("logs/recombination_strat_test.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class TestBitwiseRecombination(unittest.TestCase):
    def setUp(self):
        # Create a BitwiseRecombination instance
        # You'll need to replace this with your actual organism
        self.organism = Organism(pop_size=10)
        self.organism.parents = randomly_select_parents(self.organism.population)
        self.bitwise_recombination = BitwiseRecombination(self.organism)

    def test_recombine(self):
        logger.debug(f"Population: {self.organism.population}")
        logger.debug(f"Parents: {self.organism.parents}")

        result = self.bitwise_recombination.recombine()

        logger.debug(f"Result: {result}")

        # Check that the result is an ndarray
        self.assertIsInstance(result, ndarray)

        # Check the shape of the result
        # Replace (100, 10) with the expected shape
        self.assertEqual(
            result.shape, (self.organism.pop_size, self.organism.bin_length)
        )


if __name__ == "__main__":
    unittest.main()
