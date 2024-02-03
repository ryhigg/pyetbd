from abc import ABC, abstractmethod
from typing import Callable
from pyetbd.rules import selection
from pyetbd.organisms import Organism
from pyetbd.settings_classes import ScheduleSettings
from numpy import ndarray


class SelectionStrategy(ABC):
    """
    An abstract class representing a selection strategy.

    This abstract class is used to ensure that any selection strategy that inherits from it will work in the algorithm class.
    """

    def __init__(
        self,
        organism: Organism,
        schedule_settings: ScheduleSettings,
        sample_func: Callable,
    ):
        """
        The constructor for the SelectionStrategy class.

        Parameters:
            organism (Organism): The organism.
            schedule_settings (ScheduleSettings): The schedule data.
            sample_func (Callable): The sample function.
        """
        self.organism = organism
        self.schedule_settings = schedule_settings
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
            self.schedule_settings.fdf_mean,
            self.sample_func,
        )
