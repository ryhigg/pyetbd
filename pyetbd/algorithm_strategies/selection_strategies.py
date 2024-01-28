from abc import ABC, abstractmethod
from typing import Callable
from pyetbd.rules import selection
from pyetbd.organisms import Organism
from pyetbd.settings_classes import ScheduleData
from numpy import ndarray


class SelectionStrategy(ABC):
    """
    An abstract class representing a selection strategy.
    """

    def __init__(
        self, organism: Organism, schedule_data: ScheduleData, sample_func: Callable
    ):
        """
        The constructor for the SelectionStrategy class.

        Parameters:
            organism (Organism): The organism.
            schedule_data (ScheduleData): The schedule data.
            sample_func (Callable): The sample function.
        """
        self.organism = organism
        self.schedule_data = schedule_data
        self.sample_func = sample_func

    @abstractmethod
    def select(self) -> ndarray:
        """
        An abstract method for selecting an organism.
        """
        pass


class FitnessSearchSelection(SelectionStrategy):
    """
    A class representing a fitness search selection strategy.
    """

    def select(self) -> ndarray:
        """
        A method for selecting an organism using fitness search selection.
        """
        return selection.fitness_search_selection(
            self.organism.population,
            self.organism.fitness_values,
            self.schedule_data.fdf_mean,
            self.sample_func,
        )
