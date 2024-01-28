import unittest
from pyetbd.organisms import Organism


class TestOrganism(unittest.TestCase):
    def setUp(self):
        self.organism = Organism()

    def test_emit(self):
        self.organism.init_population()
        self.organism.emit()
        self.assertTrue(self.organism.emitted in self.organism.population)

    def test_init_population(self):
        self.organism.init_population()
        self.assertEqual(len(self.organism.population), self.organism.pop_size)
        self.assertTrue(
            all(
                self.organism.low_pheno <= x < self.organism.high_pheno
                for x in self.organism.population
            )
        )


if __name__ == "__main__":
    unittest.main()
