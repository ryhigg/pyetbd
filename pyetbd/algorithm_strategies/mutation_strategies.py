from abc import ABC, abstractmethod
from pyetbd.rules import mutation
from pyetbd.organisms import Organism
from pyetbd.settings_classes import ScheduleData
from numpy import ndarray


class MutationStrategy(ABC):
    """
    An abstract class representing a mutation strategy.
    """

    def __init__(self, organism: Organism, schedule_data: ScheduleData):
        """
        The constructor for the MutationStrategy class.

        Parameters:
            organism (Organism): The organism.
            schedule_data (ScheduleData): The schedule data.
        """
        self.organism = organism
        self.schedule_data = schedule_data

    @abstractmethod
    def mutate(self) -> ndarray:
        """
        An abstract method for mutating an organism.
        """
        pass


class BitFlipMutation(MutationStrategy):
    """
    A class representing a bit flip mutation strategy.
    """

    def mutate(self) -> ndarray:
        """
        A method for mutating an organism using bit flip mutation.
        """
        return mutation.bit_flip_mutate(
            self.organism.offspring_genos, self.schedule_data.mut_rate
        )
