import numpy as np
from pyetbd.utils import equations as eq


class Schedule:
    """A class for schedules."""

    def __init__(
        self,
        schedule_type: str,
        schedule_subtype: str,
        mean: float,
        fdf_mean: float,
        fdf_type: str,
        response_class_lower_bound: int,
        response_class_upper_bound: int,
        response_class_size: int,
        excluded_lower_bound: int,
        excluded_upper_bound: int,
    ):
        """Initializes a schedule.

        Args:
            schedule_type (str): The type of schedule (fixed, variable, random)
            schedule_subtype (str): The subtype of schedule (interval, ratio)
            mean (float): The mean interval or ratio of the schedule
            fdf_mean (float): The magnitude of the FDF for the schedule (reinforcer magnitude)
            fdf_type (str): The type of FDF (linear, exponential, etc.)
            response_class (list): A list of the behavior phenotypes that are reinforced by this schedule
        """
        self.schedule_type = schedule_type
        self.schedule_subtype = schedule_subtype
        self.mean = mean
        self.fdf_mean = fdf_mean
        self.fdf_type = fdf_type
        self.response_class_lower_bound = response_class_lower_bound
        self.response_class_upper_bound = response_class_upper_bound
        self.response_class_size = response_class_size
        self.excluded_lower_bound = excluded_lower_bound
        self.excluded_upper_bound = excluded_upper_bound

        self.current_count = self.get_schedule_count()
        self.counter = 0
        self.generate_response_class()

    def in_response_class(self, emitted: int):
        """Sets whether the emitted response is in the response class.

        Args:
            emitted (int): The phenotype of the emitted response
        """
        return emitted in self.response_class

    def update_counter(self, emitted: int):
        """Updates the counter for the schedule.

        Args:
            emitted (int): The phenotype of the emitted response
        """

        if self.schedule_subtype == "interval":
            self.counter += 1
        elif self.schedule_subtype == "ratio":
            if emitted in self.response_class:
                self.counter += 1

    def get_schedule_count(self):
        """Gets the interval for the schedule based on the type.

        Raises:
            NotImplementedError: variable schedules are not implemented yet # TODO: implement variable schedules
            ValueError: invalid type for interval schedule

        Returns:
            float: the interval for the schedule
        """
        if self.schedule_type == "fixed":
            return self.mean
        elif self.schedule_type == "variable":
            raise NotImplementedError
        elif self.schedule_type == "random":
            return eq.sample_exponential(self.mean)
        else:
            raise ValueError("Invalid type for interval schedule.")

    def generate_response_class(self):
        """Generates a response class based on the lower bound, upper bound, and size of the response class."""

        possible_values = [
            i
            for i in range(
                self.response_class_lower_bound, self.response_class_upper_bound
            )
        ]

        # remove excluded values
        for value in range(self.excluded_lower_bound, self.excluded_upper_bound):
            possible_values.remove(value)

        self.response_class = np.random.choice(possible_values, self.response_class_size, replace=False)  # type: ignore

    def check_reinforcement(self, emitted: int):
        """Runs the schedule.

        Args:
            emitted (int): The phenotype of the emitted response

        Returns:
            bool: True if the response is reinforced, False otherwise
        """
        # check if the response is in the response class
        if self.in_response_class(emitted):
            # check if the counter has elapsed
            if self.counter >= self.current_count:
                self.counter = 0
                self.current_count = self.get_schedule_count()
                return True

        # if the response is not reinforced, return False
        return False
