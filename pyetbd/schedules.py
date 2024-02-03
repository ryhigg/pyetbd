from abc import ABC, abstractmethod
import numpy as np
from pyetbd.settings_classes import ScheduleSettings
from pyetbd.utils import equations as eq


class Schedule(ABC):
    """
    An abstract class that represents a schedule.

    This abstract class is the parent class for the different schedule types. It contains the common methods and attributes for the different schedule types.
    """

    def __init__(self, settings: ScheduleSettings):
        self.settings = settings
        self._generate_response_class()

        self.count = 0
        self.current_count_requirement = 0

    def _generate_response_class(self) -> None:
        possible_values = np.arange(
            self.settings.response_class_lower_bound,
            self.settings.response_class_upper_bound,
            1,
        )

        excluded_values = np.arange(
            self.settings.excluded_lower_bound, self.settings.excluded_upper_bound, 1
        )

        possible_values = np.setdiff1d(
            possible_values, excluded_values, assume_unique=True
        )

        try:
            self.response_class = np.random.choice(
                possible_values, self.settings.response_class_size, replace=False
            )

        except:
            raise ValueError(
                "Giddydowned: Response class generation failed. Not enough possible values to meet specified 'response_class_size'. Check your 'response_class_lower_bound', 'response_class_upper_bound', 'response_class_size', 'excluded_lower_bound', and 'excluded_upper_bound' settings."
            )

    def in_response_class(self, emitted: int) -> bool:
        return emitted in self.response_class

    def get_availability(self, emitted: int) -> bool:
        return (
            self.in_response_class(emitted)
            and self.count >= self.current_count_requirement
        )

    def run(self, emitted: int) -> bool:
        self.update_counter(emitted)

        if self.get_availability(emitted):
            self.set_count_requirement()
            self.count = 0
            return True

        return False

    @abstractmethod
    def update_counter(self, emitted: int) -> None: ...

    @abstractmethod
    def set_count_requirement(self) -> None: ...


class FixedSchedule(Schedule, ABC):
    """
    An abstract class that represents a fixed schedule.

    This class is a child class of the Schedule class. It contains the methods and attributes for a fixed schedule.
    """

    def __init__(self, schedule_data: ScheduleSettings):
        super().__init__(schedule_data)
        self.set_count_requirement()

    def set_count_requirement(self) -> None:
        self.current_count_requirement = self.settings.mean


class RandomSchedule(Schedule, ABC):
    """
    An abstract class that represents a random schedule.

    This class is a child class of the Schedule class. It contains the methods and attributes for a random schedule.
    """

    def __init__(self, schedule_data: ScheduleSettings):
        super().__init__(schedule_data)
        self.set_count_requirement()

    def set_count_requirement(self) -> None:
        self.current_count_requirement = eq.sample_exponential(self.settings.mean)


class IntervalSchedule(Schedule, ABC):
    """
    An abstract class that represents an interval schedule.

    This class is a child class of the Schedule class. It contains the methods and attributes for an interval schedule.
    """

    def update_counter(self, emitted: int) -> None:
        self.count += 1


class RatioSchedule(Schedule, ABC):
    """
    An abstract class that represents a ratio schedule.

    This class is a child class of the Schedule class. It contains the methods and attributes for a ratio schedule.
    """

    def update_counter(self, emitted: int) -> None:
        if self.in_response_class(emitted):
            self.count += 1


class FixedIntervalSchedule(FixedSchedule, IntervalSchedule):
    """
    A concrete class that represents a fixed interval schedule.

    It is a child class of the FixedSchedule and IntervalSchedule classes, so it inherits the methods and attributes from both parent classes.
    """

    ...


class FixedRatioSchedule(FixedSchedule, RatioSchedule):
    """
    A concrete class that represents a fixed ratio schedule.

    It is a child class of the FixedSchedule and RatioSchedule classes, so it inherits the methods and attributes from both parent classes.
    """

    ...


class RandomIntervalSchedule(RandomSchedule, IntervalSchedule):
    """
    A concrete class that represents a random interval schedule.

    It is a child class of the RandomSchedule and IntervalSchedule classes, so it inherits the methods and attributes from both parent classes.
    """

    ...


class RandomRatioSchedule(RandomSchedule, RatioSchedule):
    """
    A concrete class that represents a random ratio schedule.

    It is a child class of the RandomSchedule and RatioSchedule classes, so it inherits the methods and attributes from both parent classes.
    """

    ...
