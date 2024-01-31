from pyetbd.experiment import Experiment
from pyetbd.schedules import RandomIntervalSchedule
from pyetbd.settings_classes import ExperimentSettings, ScheduleSettings


def main():
    alt1_ris = [i for i in range(20, 121, 10)]
    alt2_ris = alt1_ris[::-1]

    schedule_arrangements = []
    for i in range(len(alt1_ris)):
        alt1 = ScheduleSettings(mean=alt1_ris[i])
        alt2 = ScheduleSettings(
            mean=alt2_ris[i],
            response_class_lower_bound=512,
            response_class_upper_bound=553,
        )

        alt1_schedule = RandomIntervalSchedule(alt1)
        alt2_schedule = RandomIntervalSchedule(alt2)

        schedule_arrangements.append([alt1_schedule, alt2_schedule])

    exp_settings = ExperimentSettings(file_stub="test", gens=20500, reps=10)
    exp = Experiment(exp_settings, schedule_arrangements)

    exp.run()


if __name__ == "__main__":
    main()
