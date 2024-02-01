import json
from pyetbd.experiment import Experiment
from pyetbd.schedules import (
    Schedule,
    RandomIntervalSchedule,
    RandomRatioSchedule,
    FixedIntervalSchedule,
    FixedRatioSchedule,
)
from pyetbd.settings_classes import ExperimentSettings, ScheduleSettings


class ExperimentRunner:
    def __init__(self, input_file: str, output_dir: str, print_progress: bool = True):
        self.input_file = input_file
        self.output_file = output_dir

        self._load_input()

    def _load_input(self):
        with open(self.input_file, "r") as f:
            self.settings = json.load(f)

    def _load_experiments(self) -> list[Experiment]:
        experiments = []

        for exp in self.settings["experiments"]:
            exp_settings = ExperimentSettings(**exp)
            schedules = self._load_schedules(exp)
            experiment = Experiment(exp_settings, schedules)
            experiments.append(experiment)

        return experiments

    def _load_schedules(self, exp: dict) -> list[list[Schedule]]:
        schedule_classes = {
            "random": {
                "interval": RandomIntervalSchedule,
                "ratio": RandomRatioSchedule,
            },
            "fixed": {"interval": FixedIntervalSchedule, "ratio": FixedRatioSchedule},
        }
        schedules = []

        for sched_arrangement in exp["schedules"]:
            arrangement = []
            for sched in sched_arrangement:
                sched_settings = ScheduleSettings(**sched)
                try:
                    schedule_class = schedule_classes[sched_settings.schedule_type][
                        sched_settings.schedule_subtype
                    ]
                except KeyError:
                    raise ValueError("Invalid schedule type")
                arrangement.append(schedule_class(sched_settings))
            schedules.append(arrangement)

        return schedules

    def giddyup(self):
        experiments = self._load_experiments()
        for experiment in experiments:
            experiment.run()

        print("Done Giddyupped!")
