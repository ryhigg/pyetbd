from abc import ABC, abstractmethod
from pyetbd.rules import recombination
from pyetbd.organisms import Organism
from numpy import ndarray


class RecombinationStrategy(ABC):
    """
    An abstract class representing a recombination strategy.

    This abstract class is used to ensure that any recombination strategy that inherits from it will work in the algorithm class.
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
            self.organism.bin_length,
            recombination.bitwise_combine,
        )
