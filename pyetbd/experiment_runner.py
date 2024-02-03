import json
from pyetbd.experiment import Experiment
from pyetbd.settings_classes import ExperimentSettings, ScheduleSettings
from pyetbd.utils import timer
from pyetbd.schedules import (
    Schedule,
    RandomIntervalSchedule,
    RandomRatioSchedule,
    FixedIntervalSchedule,
    FixedRatioSchedule,
)


class ExperimentRunner:
    """
    Class responsible for running experiments based on the provided input file.

    Args:
        input_file (str): The path to the input file containing experiment settings.
        output_dir (str, optional): The directory where the experiment output will be saved. Defaults to "".
        log_progress (bool, optional): Flag indicating whether to log the progress of the experiments. Defaults to True.
    """

    def __init__(
        self, input_file: str, output_dir: str = "", log_progress: bool = True
    ):
        self.input_file = input_file
        self.output_dir = output_dir
        self.log_progress = log_progress

        self._load_input()

    def _load_input(self):
        """
        Loads the experiment settings from the input file.
        """
        with open(self.input_file, "r") as f:
            self.settings = json.load(f)

    def _load_experiments(self) -> list[Experiment]:
        """
        Loads the experiments based on the experiment settings.

        Returns:
            list[Experiment]: A list of Experiment objects.
        """
        # create list to hold experiment objects
        experiments = []

        for exp in self.settings["experiments"]:
            # create experiment settings object from json
            exp_settings = ExperimentSettings(**exp)
            # create schedule objects from json
            schedules = self._load_schedules(exp)
            # create experiment object
            experiment = Experiment(
                exp_settings, schedules, self.log_progress, self.output_dir
            )
            # add experiment to list of experiments
            experiments.append(experiment)

        # return list of experiment objects
        return experiments

    def _load_schedules(self, exp: dict) -> list[list[Schedule]]:
        """
        Loads the schedules for a given experiment.

        Args:
            exp (dict): The experiment settings.

        Returns:
            list[list[Schedule]]: A nested list of Schedule objects.
        """
        # the schedule_classes dictionary maps the schedule type and subtype to the corresponding Schedule class
        schedule_classes = {
            "random": {
                "interval": RandomIntervalSchedule,
                "ratio": RandomRatioSchedule,
            },
            "fixed": {"interval": FixedIntervalSchedule, "ratio": FixedRatioSchedule},
        }
        schedules = []

        # loop through each schedule arrangement in the experiment settings
        for sched_arrangement in exp["schedules"]:
            # create a list to hold the schedule objects
            arrangement = []
            # loop through each schedule in the arrangement
            for sched in sched_arrangement:
                # create a copy of the experiment settings
                exp_copy = exp.copy()

                # get a list of field names that are unique to ExperimentSettings
                experiment_only_fields = set(
                    ExperimentSettings.__annotations__.keys()
                ) - set(ScheduleSettings.__annotations__.keys())

                # remove these fields from exp_copy
                for field in experiment_only_fields:
                    exp_copy.pop(field, None)

                # create a ScheduleSettings object from the json
                # this will first look at the experiment settings and then override with the schedule settings if they exist
                sched_settings = ScheduleSettings(**exp_copy, **sched)
                try:
                    # create the schedule object based on the schedule type and subtype using the schedule_classes dictionary
                    schedule_class = schedule_classes[sched_settings.schedule_type][
                        sched_settings.schedule_subtype
                    ]
                except KeyError:
                    # raise an error if the schedule type or subtype is invalid
                    raise ValueError("Invalid schedule type")
                # add the schedule object to the arrangement list
                arrangement.append(schedule_class(sched_settings))
            # add the arrangement list to the schedules list
            schedules.append(arrangement)

        return schedules

    @timer.timer
    def giddyup(self) -> None:
        """
        Runs the experiments.

        This method loads the experiments, and then runs each experiment.
        """
        print("Loading experiments...")
        experiments = self._load_experiments()
        for experiment in experiments:
            experiment.run()

        print("\U0001F434 Done Giddyupped! \U0001F434")
