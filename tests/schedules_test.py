import unittest
from pyetbd.settings_classes import ScheduleSettings
from pyetbd.schedules import (
    FixedIntervalSchedule,
    FixedRatioSchedule,
    RandomIntervalSchedule,
    RandomRatioSchedule,
)


class TestSchedules(unittest.TestCase):
    def setUp(self):
        self.schedule_data = ScheduleSettings(mean=5)

    def test_fixed_interval_schedule(self):
        schedule = FixedIntervalSchedule(self.schedule_data)
        # Add assertions here based on the expected behavior of FixedIntervalSchedule
        emitted = 471
        for i in range(5):
            reinforced = schedule.run(emitted)

            if i < 4:
                self.assertFalse(reinforced)
            else:
                self.assertTrue(reinforced)

        emitted = 300
        for i in range(5):
            reinforced = schedule.run(emitted)

            self.assertFalse(reinforced)
            self.assertTrue(schedule.count == i + 1)

    def test_fixed_ratio_schedule(self):
        schedule = FixedRatioSchedule(self.schedule_data)
        # Add assertions here based on the expected behavior of FixedRatioSchedule
        emitted = 471
        for i in range(5):
            reinforced = schedule.run(emitted)

            if i < 4:
                self.assertFalse(reinforced)
            else:
                self.assertTrue(reinforced)

        emitted = 300
        for i in range(5):
            reinforced = schedule.run(emitted)

            self.assertFalse(reinforced)
            self.assertTrue(schedule.count == 0)

    def test_random_interval_schedule(self):
        schedule = RandomIntervalSchedule(self.schedule_data)

        emitted = 471
        current_count_requirement = schedule.current_count_requirement
        for i in range(int(current_count_requirement) + 1):
            reinforced = schedule.run(emitted)

            if i < current_count_requirement - 1:
                self.assertFalse(reinforced)
            else:
                self.assertTrue(reinforced)

        emitted = 300
        current_count_requirement = schedule.current_count_requirement
        for i in range(int(current_count_requirement) + 1):
            reinforced = schedule.run(emitted)

            self.assertFalse(reinforced)
            self.assertTrue(schedule.count == i + 1)

    def test_random_ratio_schedule(self):
        schedule = RandomRatioSchedule(self.schedule_data)

        emitted = 471
        current_count_requirement = schedule.current_count_requirement
        for i in range(int(current_count_requirement) + 1):
            reinforced = schedule.run(emitted)

            if i < current_count_requirement - 1:
                self.assertFalse(reinforced)
            else:
                self.assertTrue(reinforced)

        emitted = 300
        current_count_requirement = schedule.current_count_requirement
        for i in range(int(current_count_requirement) + 1):
            reinforced = schedule.run(emitted)

            self.assertFalse(reinforced)
            self.assertTrue(schedule.count == 0)


if __name__ == "__main__":
    unittest.main()
