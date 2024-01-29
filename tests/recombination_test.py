import unittest
import numpy as np
from pyetbd.rules.recombination import recombine_parents, bitwise_combine
import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the level of this logger. DEBUG is the lowest level.
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("logs/recombination_test.log")
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


class TestRecombination(unittest.TestCase):
    def test_bitwise_combine(self):
        mother_geno = np.array([1, 0, 1, 0], dtype=np.int8)
        father_geno = np.array([1, 0, 1, 0], dtype=np.int8)

        expected_child_geno = np.array([1, 0, 1, 0], dtype=np.int8)
        actual_child_geno = bitwise_combine(mother_geno, father_geno)

        np.testing.assert_array_equal(actual_child_geno, expected_child_geno)

    def test_recombine_parents(self):
        parents = np.array([[4, 4], [400, 400]], dtype=np.int64)
        bin_length = 10

        expected_children_genos = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 0, 1, 0, 0, 0, 0]],
            dtype=np.int8,
        )  # based on bitwise_combine
        actual_children_genos = recombine_parents(parents, bin_length, bitwise_combine)
        logger.debug(f"Expected Children Genos: {expected_children_genos}")
        logger.debug(f"Actual Children Genos: {actual_children_genos}")

        np.testing.assert_array_equal(actual_children_genos, expected_children_genos)


if __name__ == "__main__":
    unittest.main()
