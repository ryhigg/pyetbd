import json
from pyetbd.utils import defaults, timer
from pyetbd import organisms, schedules as sched, experiments


class ExperimentHandler:
    def __init__(self, input_file: str, output_dir: str):
        """Initializes the ExperimentBuilder class. This class is used to build an experiment from a JSON file and run it.

        Args:
            input_file (str): the input file path
            output_dir (str): the output directory
        """
        self.input_file = input_file
        self.output_dir = output_dir

        # load the settings and defaults
        with open(self.input_file) as f:
            self.settings = json.load(f)

        self.defaults = defaults.DEFAULTS

        self.experiments = []

    @timer.timer
    def giddyup(self):
        """Builds the experiments from the json input and runs them."""
        self.build_experiments()

        for experiment in self.experiments:
            experiment.run()
            experiment.output_data()

        print("\U0001F434 Done Giddyupped! \U0001F434")

    def build_experiments(self):
        """Builds the experiments from the json input."""
        self.experiment_dictionaries = []

        for experiment in self.settings["experiments"]:
            self.experiment_dictionaries.append(self.build_experiment(experiment))

        for experiment in self.experiment_dictionaries:
            organism = organisms.AnOrganism(
                pop_size=experiment["pop_size"],
                mut_rate=experiment["mut_rate"],
                low_pheno=experiment["low_pheno"],
                high_pheno=experiment["high_pheno"],
                fdf_type=experiment["fdf_type"],
                fitness_landscape=experiment["fitness_landscape"],
                recombination_method=experiment["recombination_method"],
            )

            schedules = []
            for schedule_arrangement in experiment["schedules"]:
                schedule_arrangement_list = []
                for schedule in schedule_arrangement:
                    schedule_arrangement_list.append(
                        sched.Schedule(
                            schedule_type=schedule["schedule_type"],
                            schedule_subtype=schedule["schedule_subtype"],
                            mean=schedule["mean"],
                            fdf_mean=schedule["fdf_mean"],
                            fdf_type=schedule["fdf_type"],
                            response_class_lower_bound=schedule[
                                "response_class_lower_bound"
                            ],
                            response_class_upper_bound=schedule[
                                "response_class_upper_bound"
                            ],
                            response_class_size=schedule["response_class_size"],
                            excluded_lower_bound=schedule["excluded_lower_bound"],
                            excluded_upper_bound=schedule["excluded_upper_bound"],
                        )
                    )
                schedules.append(schedule_arrangement_list)

            experiment = experiments.Experiment(
                schedules,
                experiment["reps"],
                experiment["gens"],
                experiment["reinitialize_population"],
                organism,
                experiment["file_stub"],
            )

            self.experiments.append(experiment)

    def build_experiment(self, experiment: dict):
        """Builds an experiment from a dictionary."""

        built_experiment = {
            "file_stub": experiment["file_stub"],
            "reps": self.defaults["reps"],
            "gens": self.defaults["gens"],
            "pop_size": self.defaults["pop_size"],
            "mut_rate": self.defaults["mut_rate"],
            "low_pheno": self.defaults["low_pheno"],
            "high_pheno": self.defaults["high_pheno"],
            "fdf_type": self.defaults["fdf_type"],
            "fitness_landscape": self.defaults["fitness_landscape"],
            "recombination_method": self.defaults["recombination_method"],
            "fdf_mean": self.defaults["fdf_mean"],
            "reinitialize_population": self.defaults["reinitialize_population"],
            "schedule_type": self.defaults["schedule_type"],
            "schedule_subtype": self.defaults["schedule_subtype"],
            "excluded_lower_bound": self.defaults["excluded_lower_bound"],
            "excluded_upper_bound": self.defaults["excluded_upper_bound"],
            "schedules": [],
        }

        num_schedules_in_arrangement = len(experiment["schedules"][0])
        num_schedules = len(experiment["schedules"])

        for i in range(num_schedules):
            schedule_arrangement = []
            for j in range(num_schedules_in_arrangement):
                schedule_arrangement.append(
                    {
                        "schedule_type": self.defaults["schedule_type"],
                        "schedule_subtype": self.defaults["schedule_subtype"],
                        "mean": self.defaults["mean"],
                        "fdf_mean": self.defaults["fdf_mean"],
                        "fdf_type": self.defaults["fdf_type"],
                        "schedule_type": self.defaults["schedule_type"],
                        "response_class_size": self.defaults["response_class_size"],
                        "response_class_lower_bound": self.defaults[
                            "response_class_lower_bound"
                        ],
                        "response_class_upper_bound": self.defaults[
                            "response_class_upper_bound"
                        ],
                        "excluded_lower_bound": self.defaults["excluded_lower_bound"],
                        "excluded_upper_bound": self.defaults["excluded_upper_bound"],
                    }
                )

            built_experiment["schedules"].append(schedule_arrangement)

        self.check_overrides(experiment, "experiment", built_experiment)

        for i in range(num_schedules):
            for j in range(num_schedules_in_arrangement):
                self.check_overrides(
                    experiment, "experiment", built_experiment["schedules"][i][j]
                )
                self.check_overrides(
                    experiment["schedules"][i][j],
                    "schedule",
                    built_experiment["schedules"][i][j],
                )

        return built_experiment

    def check_overrides(
        self, exp_or_sched: dict, object_type: str, built_experiment: dict
    ):
        """Checks for overrides in a settings dictionary and updates the built_experiment dictionary accordingly.

        Args:
            exp_or_sched (dict): a settings dictionary
            object_type (str): either "experiment" or "schedule"
            built_experiment (dict): the built experiment dictionary
        """

        if object_type == "experiment":
            if "reps" in exp_or_sched:
                built_experiment["reps"] = exp_or_sched["reps"]

            if "gens" in exp_or_sched:
                built_experiment["gens"] = exp_or_sched["gens"]

            if "pop_size" in exp_or_sched:
                built_experiment["pop_size"] = exp_or_sched["pop_size"]

            if "mut_rate" in exp_or_sched:
                built_experiment["mut_rate"] = exp_or_sched["mut_rate"]

            if "low_pheno" in exp_or_sched:
                built_experiment["low_pheno"] = exp_or_sched["low_pheno"]

            if "high_pheno" in exp_or_sched:
                built_experiment["high_pheno"] = exp_or_sched["high_pheno"]

            if "fdf_type" in exp_or_sched:
                built_experiment["fdf_type"] = exp_or_sched["fdf_type"]

            if "fitness_landscape" in exp_or_sched:
                built_experiment["fitness_landscape"] = exp_or_sched[
                    "fitness_landscape"
                ]

            if "recombination_method" in exp_or_sched:
                built_experiment["recombination_method"] = exp_or_sched[
                    "recombination_method"
                ]

            if "reinitialize_population" in exp_or_sched:
                built_experiment["reinitialize_population"] = exp_or_sched[
                    "reinitialize_population"
                ]

            if "fdf_mean" in exp_or_sched:
                built_experiment["fdf_mean"] = exp_or_sched["fdf_mean"]

            if "schedule_type" in exp_or_sched:
                built_experiment["schedule_type"] = exp_or_sched["schedule_type"]

            if "schedule_subtype" in exp_or_sched:
                built_experiment["schedule_subtype"] = exp_or_sched["schedule_subtype"]

            if "excluded_lower_bound" in exp_or_sched:
                built_experiment["excluded_lower_bound"] = exp_or_sched[
                    "excluded_lower_bound"
                ]

            if "excluded_upper_bound" in exp_or_sched:
                built_experiment["excluded_upper_bound"] = exp_or_sched[
                    "excluded_upper_bound"
                ]

        if object_type == "experiment" or "schedule":
            if "fdf_mean" in exp_or_sched:
                built_experiment["fdf_mean"] = exp_or_sched["fdf_mean"]

            if "response_class_lower_bound" in exp_or_sched:
                built_experiment["response_class_lower_bound"] = exp_or_sched[
                    "response_class_lower_bound"
                ]

            if "response_class_upper_bound" in exp_or_sched:
                built_experiment["response_class_upper_bound"] = exp_or_sched[
                    "response_class_upper_bound"
                ]

            if "response_class_size" in exp_or_sched:
                built_experiment["response_class_size"] = exp_or_sched[
                    "response_class_size"
                ]

            if "schedule_type" in exp_or_sched:
                built_experiment["schedule_type"] = exp_or_sched["schedule_type"]

            if "schedule_subtype" in exp_or_sched:
                built_experiment["schedule_subtype"] = exp_or_sched["schedule_subtype"]

            if "fdf_type" in exp_or_sched:
                built_experiment["fdf_type"] = exp_or_sched["fdf_type"]

            if "mean" in exp_or_sched:
                built_experiment["mean"] = exp_or_sched["mean"]

            if "excluded_lower_bound" in exp_or_sched:
                built_experiment["excluded_lower_bound"] = exp_or_sched[
                    "excluded_lower_bound"
                ]

            if "excluded_upper_bound" in exp_or_sched:
                built_experiment["excluded_upper_bound"] = exp_or_sched[
                    "excluded_upper_bound"
                ]
