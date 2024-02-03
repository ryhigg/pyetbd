from abc import ABC, abstractmethod
from typing import Callable
from pyetbd.rules import fdfs
from pyetbd.settings_classes import ScheduleSettings


class SampleFDF(ABC):
    """
    An abstract class representing a sampling strategy for a fitness density function.

    This abstract class is used to ensure that any sampling strategy that inherits from it will work in the algorithm class.
    """

    def __init__(self, schedule_settings: ScheduleSettings):
        """
        The constructor for the SampleFDF class.

        Parameters:
            schedule_settings
            (ScheduleSettings): The schedule data.
        """
        self.schedule_settings = schedule_settings

    @abstractmethod
    def get_sample_func(self) -> Callable:
        """
        An abstract method for getting the sample function.
        """
        ...


class LinearFDF(SampleFDF):
    """
    A class representing a linear sampling strategy for a fitness
    density function.

    Returns:
        Callable: A function that returns a sample from a linear fdf.
    """

    def get_sample_func(self) -> Callable:
        """
        A method for getting the sampling function to a linear fdf.

        """
        return fdfs.sample_linear_fdf


class ExponentialFDF(SampleFDF):
    """
    A class representing an exponential sampling strategy for a fitness density function.
    """

    def get_sample_func(self) -> Callable:
        """
        A method for getting an exponential fdf.

        Returns:
            Callable: A function that returns a sample from an exponential fdf.
        """
        return fdfs.sample_exponential_fdf
