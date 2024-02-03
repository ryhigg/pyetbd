from abc import ABC, abstractmethod
from pyetbd.rules import fitness_calculation
from pyetbd.organisms import Organism
from numpy import ndarray


class FitnessCalculationStrategy(ABC):
    """
    An abstract class representing a fitness calculation strategy.

    This abstract class is used to ensure that any fitness calculation strategy that inherits from it will work in the algorithm class.
    """

    def __init__(self, organism: Organism):
        """
        The constructor for the FitnessCalculationStrategy class.

        Parameters:
            organism (Organism): The organism.
        """
        self.organism = organism

    @abstractmethod
    def calculate_fitness(self) -> ndarray:
        """
        An abstract method for calculating fitness.
        """
        pass


class LinearFitnessCalculation(FitnessCalculationStrategy):
    """
    A class representing a linear fitness calculation strategy.
    """

    def calculate_fitness(self) -> ndarray:
        """
        A method for calculating linear fitness.

        Returns:
            ndarray: The fitness values.
        """
        return fitness_calculation.get_linear_fitness_values(
            self.organism.population, self.organism.emitted
        )


class CircularFitnessCalculation(FitnessCalculationStrategy):
    """
    A class representing a circular fitness calculation strategy.
    """

    def calculate_fitness(self) -> ndarray:
        """
        A method for calculating circular fitness.

        Returns:
            ndarray: The fitness values.
        """
        return fitness_calculation.get_circular_fitness_values(
            self.organism.population, self.organism.emitted, self.organism.high_pheno
        )
