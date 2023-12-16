import numpy as np
from pyETBD.utils import equations as eq


class IntervalSchedule:
    """A class for interval schedules. Can be fixed or random, variable will be implemented later."""

    def __init__(
        self,
        interval: float,
        fdf_mean: float,
        fdf_type: str,
        type: str,
        response_class_lower_bound: int,
        response_class_upper_bound: int,
        response_class_size: int,
    ):
        """Initializes an interval schedule.

        Args:
            interval (float): The interval or mean interval
            fdf_mean (float): The magnitude of the FDF for the schedule (reinforcer magnitude)
            fdf_type (str): The type of FDF (linear, exponential, etc.)
            type (str): The type of schedule (fixed, variable, random)
            response_class (list): A list of the behavior phenotypes that are reinforced by this schedule
        """
        self.interval = interval
        self.fdf_mean = fdf_mean
        self.fdf_type = fdf_type
        self.type = type
        self.response_class_lower_bound = response_class_lower_bound
        self.response_class_upper_bound = response_class_upper_bound
        self.response_class_size = response_class_size

        # initialize the current interval and interval counter
        self.current_interval = self.get_interval()
        self.interval_counter = 0

        # generate the response class
        self.generate_response_class()

    def generate_response_class(self):
        """Generates a response class based on the lower bound, upper bound, and size of the response class."""

        possible_values = [
            i
            for i in range(
                self.response_class_lower_bound, self.response_class_upper_bound
            )
        ]

        self.response_class = np.random.choice(possible_values, self.response_class_size, replace=False)  # type: ignore

    def check_response_class(self, emitted: int):
        """Checks if the emitted response is in the response class.

        Args:
            emitted (int): The phenotype of the emitted response

        Returns:
            bool: True if the response is in the response class, False otherwise
        """
        # increment the interval counter since this is called each generation
        self.interval_counter += 1

        if emitted in self.response_class:
            return True
        else:
            return False

    def get_interval(self):
        """Gets the interval for the schedule based on the type.

        Raises:
            NotImplementedError: variable schedules are not implemented yet # TODO: implement variable schedules
            ValueError: invalid type for interval schedule

        Returns:
            float: the interval for the schedule
        """
        if self.type == "fixed":
            return self.interval
        elif self.type == "variable":
            raise NotImplementedError
        elif self.type == "random":
            return eq.sample_exponential(self.interval)
        else:
            raise ValueError("Invalid type for interval schedule.")

    def check_reinforcement(self, emitted: int):
        """Checks if the response is reinforced.

        Args:
            emitted (int): The phenotype of the emitted response

        Returns:
            bool: True if the response is reinforced, False otherwise
        """

        # check if the response is in the response class
        if self.check_response_class(emitted):
            # check if the interval has elapsed
            if self.interval_counter >= self.current_interval:
                self.interval_counter = 0
                self.current_interval = self.get_interval()
                return True

        # if the response is not reinforced, return False
        return False
