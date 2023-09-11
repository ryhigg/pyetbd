import numpy as np


class AnOrganism:
    def __init__(
        self,
        pop_size,
        mut_rate,
        low_pheno,
        high_pheno,
        fdf_type,
        fitness_landscape,
        recombination_method,
    ):
        self.pop_size = pop_size
        self.mut_rate = mut_rate
        self.low_pheno = low_pheno
        self.high_pheno = high_pheno
        self.fdf_type = fdf_type
        self.fitness_landscape = fitness_landscape
        self.recombination_method = recombination_method

        self.bin_length = len(bin(self.high_pheno)[2:])

        self.init_population()
        self.emit()

    def init_population(self):
        self.population = np.random.randint(
            self.low_pheno, self.high_pheno + 1, self.pop_size
        )

    def emit(self):
        self.emitted = np.random.choice(self.population)

    def replace_population(self, new_population):
        self.population = new_population
