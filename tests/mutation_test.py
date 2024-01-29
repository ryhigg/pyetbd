import unittest
import numpy as np
from pyetbd.rules.mutation import bit_flip_mutate
from pyetbd.utils import binary_converter

# set up logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("logs/mutation_test.log")
fh.setLevel(logging.DEBUG)

# add the handlers to the logger
logger.addHandler(fh)


class TestMutation(unittest.TestCase):
    def test_bit_flip_mutate(self):
        children_genos = np.random.randint(0, 2, size=(100, 10))
        children_phenos = binary_converter.convert_binary_to_decimal(children_genos)
        mut_rate = 0.1
        num_mutations_list = []

        for _ in range(10000):
            mutated_children = bit_flip_mutate(children_genos, mut_rate)

            # get how many children have been mutated
            num_mutations = np.sum(mutated_children != children_phenos)
            num_mutations_list.append(num_mutations)

        logger.debug(f"Mutation Rate: {mut_rate}")
        logger.debug(f"Mean Number of Mutations: {np.mean(num_mutations_list)}")
        # check that the number of mutations is approximately equal to the mutation rate
        self.assertAlmostEqual(
            np.mean(num_mutations_list), mut_rate * children_genos.shape[0], delta=0.05
        )


if __name__ == "__main__":
    unittest.main()
