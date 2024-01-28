from abc import ABC, abstractmethod
from pyetbd.rules import fdfs
from pyetbd.settings_classes import ScheduleData


class SampleFDF(ABC):
    """
    An abstract class representing a sampling strategy for a fitness density function.
    """

    def __init__(self, schedule_data: ScheduleData):
        """
        The constructor for the SampleFDF class.

        Parameters:
            schedule_data (ScheduleData): The schedule data.
        """
        self.schedule_data = schedule_data

    @abstractmethod
    def sample(self) -> float:
        """
        An abstract method for sampling an fdf.
        """
        pass


class LinearFDF(SampleFDF):
    """
    A class representing a linear sampling strategy for a fitness
    density function.
    """

    def sample(self) -> float:
        """
        A method for sampling a linear fdf.

        Returns:
            float: The sampled value.
        """
        return fdfs.sample_linear_fdf(self.schedule_data.fdf_mean)


class ExponentialFDF(SampleFDF):
    """
    A class representing an exponential sampling strategy for a fitness density function.
    """

    def sample(self) -> float:
        """
        A method for sampling an exponential fdf.

        Returns:
            float: The sampled value.
        """
        return fdfs.sample_exponential_fdf(self.schedule_data.fdf_mean)
