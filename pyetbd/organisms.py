from dataclasses import dataclass, field
import numpy as np
from pyetbd.defaults import DEFAULTS


@dataclass
class Organism:
    pop_size: int = field(default_factory=lambda: DEFAULTS["pop_size"])
    low_pheno: int = field(default_factory=lambda: DEFAULTS["low_pheno"])
    high_pheno: int = field(default_factory=lambda: DEFAULTS["high_pheno"])

    def __post_init__(self) -> None:
        self.bin_length = len(bin(self.high_pheno)[2:])
        self.init_population()
        # used for keeping track of the fitness values of the population
        self.fitness_values = np.ndarray(self.pop_size)
        # used for keeping track of parents as the algorithm progresses
        self.parents = np.ndarray([self.pop_size, 2])
        # used for keeping track of offspring as the algorithm progresses
        self.offspring_genos = np.ndarray([self.pop_size, self.bin_length])

    def emit(self) -> None:
        self.emitted = np.random.choice(self.population)

    def init_population(self) -> None:
        self.population = np.random.randint(
            self.low_pheno, self.high_pheno, self.pop_size
        )
