from abc import ABC, abstractmethod
from pyetbd.rules import punishment
from pyetbd.organisms import Organism
from pyetbd.settings_classes import ScheduleSettings
from numpy import ndarray


class PunishmentStrategy(ABC):
    """
    An abstract class representing a punishment strategy.

    This abstract class is used to ensure that any punishment strategy that inherits from it will work in the algorithm class.
    """

    def __init__(self, organism: Organism, schedule_settings: ScheduleSettings):
        """
        The constructor for the PunishmentStrategy class.

        Parameters:
            organism (Organism): The organism.
            schedule_settings (ScheduleSettings): The schedule data.
        """
        self.organism = organism
        self.schedule_settings = schedule_settings

    @abstractmethod
    def punish(self) -> ndarray:
        """
        An abstract method for punishing an organism.
        """
        pass


class RLAPunishment(PunishmentStrategy):
    """
    A class representing a reinforcement learning algorithm punishment strategy.
    """

    def punish(self) -> ndarray:
        """
        A method for punishing an organism using the RL algorithm.
        """

        pass
