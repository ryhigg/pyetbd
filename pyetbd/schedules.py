from abc import ABC, abstractmethod
import numpy as np
from settings_classes import ScheduleData
from utils import equations as eq


class Schedule(ABC):
    def __init__(self, schedule_data: ScheduleData):
        self.data = schedule_data
        self._generate_response_class()

        self.count = 0
        self.current_count_requirement = 0

    def _generate_response_class(self) -> None:
        possible_values = np.arange(
            self.data.response_class_lower_bound,
            self.data.response_class_upper_bound,
            1,
        )

        excluded_values = np.arange(
            self.data.excluded_lower_bound, self.data.excluded_upper_bound, 1
        )

        possible_values = np.setdiff1d(
            possible_values, excluded_values, assume_unique=True
        )

        try:
            self.response_class = np.random.choice(
                possible_values, self.data.response_class_size, replace=False
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
    def update_counter(self, emitted: int) -> None:
        ...

    @abstractmethod
    def set_count_requirement(self) -> None:
        ...


class FixedSchedule(Schedule, ABC):
    def __init__(self, schedule_data: ScheduleData):
        super().__init__(schedule_data)
        self.set_count_requirement()

    def set_count_requirement(self) -> None:
        self.current_count_requirement = self.data.mean


class RandomSchedule(Schedule, ABC):
    def __init__(self, schedule_data: ScheduleData):
        super().__init__(schedule_data)
        self.set_count_requirement()

    def set_count_requirement(self) -> None:
        self.current_count_requirement = eq.sample_exponential(self.data.mean)


class IntervalSchedule(Schedule, ABC):
    def update_counter(self, emitted: int) -> None:
        self.count += 1


class RatioSchedule(Schedule, ABC):
    def update_counter(self, emitted: int) -> None:
        if self.in_response_class(emitted):
            self.count += 1


class FixedIntervalSchedule(FixedSchedule, IntervalSchedule):
    ...


class FixedRatioSchedule(FixedSchedule, RatioSchedule):
    ...


class RandomIntervalSchedule(RandomSchedule, IntervalSchedule):
    ...


class RandomRatioSchedule(RandomSchedule, RatioSchedule):
    ...
