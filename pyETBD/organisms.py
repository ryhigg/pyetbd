import numpy as np
from pyETBD.algorithm import selection, recombination, mutation


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

    def reinforcement_delivered(self, fdf_mean, fdf_type):
        parents = selection.fitness_search_selection(
            self.population,
            fdf_type,
            fdf_mean,
            self.fitness_landscape,
            self.high_pheno,
            self.emitted,
        )
        children = recombination.recombine_parents(
            parents, self.bin_length, self.recombination_method
        )
        new_population = mutation.mutate_population(children, self.mut_rate)

        self.replace_population(new_population)

    def no_reinforcement_delivered(self):
        parents = selection.randomly_select_parents(self.population)
        children = recombination.recombine_parents(
            parents, self.bin_length, self.recombination_method
        )
        new_population = mutation.mutate_population(children, self.mut_rate)

        self.replace_population(new_population)
