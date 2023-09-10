from pyETBD.organisms import an_organism
from pyETBD.algorithm import selection
from pyETBD.algorithm import recombination
from pyETBD.algorithm import mutation
import numpy as np


class ConcRI:
    def __init__(
        self,
        organism_params: tuple,
        left_mean: int,
        right_mean: int,
        left_fdf: int,
        right_fdf: int,
        left_lower: int,
        left_upper: int,
        right_lower: int,
        right_upper: int,
    ):
        self.organism = an_organism.AnOrganism(*organism_params)
        self.left_mean = left_mean
        self.right_mean = right_mean
        self.left_fdf = left_fdf
        self.right_fdf = right_fdf
        self.left_lower = left_lower
        self.left_upper = left_upper
        self.right_lower = right_lower
        self.right_upper = right_upper

        self.set_up()

    def set_up(self):
        self.left_schedule = np.random.exponential(self.left_mean)
        self.right_schedule = np.random.exponential(self.right_mean)

        self.emissions = []
        self.R1 = []
        self.B1 = []
        self.R2 = []
        self.B2 = []

        self.left_counter = 0
        self.right_counter = 0

    def return_data(self):
        return {
            "Emissions": self.emissions,
            "R1": self.R1,
            "B1": self.B1,
            "R2": self.R2,
            "B2": self.B2,
        }

    def run(self):
        self.organism.emit()
        self.emissions.append(self.organism.emitted)

        self.left_counter += 1
        self.right_counter += 1

        if self.left_lower <= self.organism.emitted <= self.left_upper:
            self.B1.append(1)
            self.B2.append(0)

            if self.left_counter >= self.left_schedule:
                self.left_counter = 0
                self.R1.append(1)
                self.R2.append(0)
                self.left_schedule = np.random.exponential(self.left_mean)

                parents = selection.fitness_search_selection(
                    self.organism.population,
                    self.organism.fdf_type,
                    self.left_fdf,
                    "circular",
                    self.organism.high_pheno,
                    self.organism.emitted,
                )
                children_genos = recombination.recombine_parents(
                    parents, self.organism.bin_length, "bitwise"
                )
                self.organism.replace_population(
                    mutation.mutate_population(children_genos, self.organism.mut_rate)
                )

            else:
                self.R1.append(0)
                self.R2.append(0)

                parents = selection.randomly_select_parents(self.organism.population)
                children_genos = recombination.recombine_parents(
                    parents, self.organism.bin_length, "bitwise"
                )
                self.organism.replace_population(
                    mutation.mutate_population(children_genos, self.organism.mut_rate)
                )

        elif self.right_lower <= self.organism.emitted <= self.right_upper:
            self.B1.append(0)
            self.B2.append(1)

            if self.right_counter >= self.right_schedule:
                self.right_counter = 0
                self.R1.append(0)
                self.R2.append(1)
                self.right_schedule = np.random.exponential(self.right_mean)

                parents = selection.fitness_search_selection(
                    self.organism.population,
                    self.organism.fdf_type,
                    self.right_fdf,
                    "circular",
                    self.organism.high_pheno,
                    self.organism.emitted,
                )
                children_genos = recombination.recombine_parents(
                    parents, self.organism.bin_length, "bitwise"
                )
                self.organism.replace_population(
                    mutation.mutate_population(children_genos, self.organism.mut_rate)
                )

            else:
                self.R1.append(0)
                self.R2.append(0)

                parents = selection.randomly_select_parents(self.organism.population)
                children_genos = recombination.recombine_parents(
                    parents, self.organism.bin_length, "bitwise"
                )
                self.organism.replace_population(
                    mutation.mutate_population(children_genos, self.organism.mut_rate)
                )

        else:
            self.B1.append(0)
            self.B2.append(0)
            self.R1.append(0)
            self.R2.append(0)

            parents = selection.randomly_select_parents(self.organism.population)
            children_genos = recombination.recombine_parents(
                parents, self.organism.bin_length, "bitwise"
            )
            self.organism.replace_population(
                mutation.mutate_population(children_genos, self.organism.mut_rate)
            )
