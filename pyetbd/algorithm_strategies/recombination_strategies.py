from abc import ABC, abstractmethod
from pyetbd.rules import recombination
from pyetbd.organisms import Organism
from numpy import ndarray


class RecombinationStrategy(ABC):
    """
    An abstract class representing a recombination strategy.
    """

    def __init__(self, organism: Organism):
        """
        The constructor for the RecombinationStrategy class.

        Parameters:
            organism (Organism): The organism.
        """
        self.organism = organism

    @abstractmethod
    def recombine(self) -> ndarray:
        """
        An abstract method for recombining an organism.
        """
        pass


class BitwiseRecombination(RecombinationStrategy):
    """
    A class representing a bitwise recombination strategy.
    """

    def recombine(self) -> ndarray:
        """
        A method for recombining an organism using bitwise recombination.
        """
        return recombination.recombine_parents(
            self.organism.parents,
            self.organism.emitted,
            recombination.bitwise_combine,
        )