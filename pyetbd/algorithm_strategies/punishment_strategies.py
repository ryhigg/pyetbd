from abc import ABC, abstractmethod
from pyetbd.rules import punishment
from pyetbd.organisms import Organism
from pyetbd.settings_classes import ScheduleData
from numpy import ndarray


class PunishmentStrategy(ABC):
    """
    An abstract class representing a punishment strategy.
    """

    def __init__(self, organism: Organism, schedule_data: ScheduleData):
        """
        The constructor for the PunishmentStrategy class.

        Parameters:
            organism (Organism): The organism.
            schedule_data (ScheduleData): The schedule data.
        """
        self.organism = organism
        self.schedule_data = schedule_data

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

        return punishment.rla_punishment()
