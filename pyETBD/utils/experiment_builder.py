import json
from pyETBD.utils.experiment import Experiment
from pyETBD.utils.defaults import DEFAULTS


class ExperimentBuilder:
    def __init__(self, input_file_path: str, output_dir: str):
        """Initializes the ExperimentBuilder class. This class is used to build an experiment from a JSON file.

        Args:
            input_file (str): the input file
            output_dir (str): the output directory
        """

        self.input_file = input_file_path
        self.output_dir = output_dir

        # load the settings and defaults
        with open(self.input_file) as f:
            self.settings = json.load(f)

        self.defaults = DEFAULTS

    def build_experiments(self):
        """Builds the experiments from the json input."""
        self.experiments = []
        self.schedules = []

        for experiment in self.settings["experiments"]:
            self.build_experiment(experiment)

            self.experiments.append(
                Experiment(
                    self.organism_params,
                    self.schedules,  # type: ignore // Pylance doesn't like this
                    self.gens,
                    self.reps,
                    self.file_stub,
                    self.experiment_type,
                    self.reinitialize_population,
                    self.output_dir,
                )
            )

    def build_experiment(self, experiment: dict):
        """Builds an experiment from a dictionary."""

        self.file_stub = experiment["file_stub"]
        self.reps = self.defaults["reps"]
        self.gens = self.defaults["gens"]
        self.experiment_type = self.defaults["experiment_type"]
        self.pop_size = self.defaults["pop_size"]
        self.mut_rate = self.defaults["mut_rate"]
        self.low_pheno = self.defaults["low_pheno"]
        self.high_pheno = self.defaults["high_pheno"]
        self.fdf_type = self.defaults["fdf_type"]
        self.fitness_landscape = self.defaults["fitness_landscape"]
        self.recombination_method = self.defaults["recombination_method"]
        self.fdf_mean = self.defaults["fdf_mean"]
        self.reinitialize_population = self.defaults["reinitialize_population"]
        self.left_sched_interval_type = self.defaults["left_sched_interval_type"]
        self.right_sched_interval_type = self.defaults["right_sched_interval_type"]
        self.left_sched_response_class_lower_bound = self.defaults[
            "left_sched_response_class_lower_bound"
        ]
        self.left_sched_response_class_upper_bound = self.defaults[
            "left_sched_response_class_upper_bound"
        ]
        self.left_sched_fdf_mean = self.defaults["fdf_mean"]
        self.right_sched_response_class_lower_bound = self.defaults[
            "right_sched_response_class_lower_bound"
        ]
        self.right_sched_response_class_upper_bound = self.defaults[
            "right_sched_response_class_upper_bound"
        ]
        self.right_sched_fdf_mean = self.defaults["fdf_mean"]

        self.check_overrides(experiment, "experiment")

        self.load_organism_params()
        self.load_schedules(experiment)

    def load_organism_params(self):
        """Loads the organism params into a dictionary."""
        self.organism_params = {
            "pop_size": self.pop_size,
            "mut_rate": self.mut_rate,
            "low_pheno": self.low_pheno,
            "high_pheno": self.high_pheno,
            "fdf_type": self.fdf_type,
            "fitness_landscape": self.fitness_landscape,
            "recombination_method": self.recombination_method,
        }

    def load_schedules(self, experiment: dict):
        """Loads the schedules from the experiment dictionary.

        Args:
            experiment (dict): an experiment dictionary
        """
        self.schedules = []
        if self.experiment_type == "concurrent":
            for sched in experiment["schedules"]:
                self.check_overrides(sched, "schedule")

                pair = {}
                pair["left_sched_params"] = {
                    "response_class_lower_bound": self.left_sched_response_class_lower_bound,
                    "response_class_upper_bound": self.left_sched_response_class_upper_bound,
                    "interval_mean": self.left_sched,
                    "interval_type": self.left_sched_interval_type,
                    "fdf_mean": self.left_sched_fdf_mean,
                }
                pair["right_sched_params"] = {
                    "response_class_lower_bound": self.right_sched_response_class_lower_bound,
                    "response_class_upper_bound": self.right_sched_response_class_upper_bound,
                    "interval_mean": self.right_sched,
                    "interval_type": self.right_sched_interval_type,
                    "fdf_mean": self.right_sched_fdf_mean,
                }

                self.schedules.append(pair)

        else:
            raise NotImplementedError(f"{self.experiment_type} is not implemented yet.")

    def check_overrides(self, dictionary: dict, object_type: str):
        """Checks for overrides in a settings dictionary.

        Args:
            dictionary (dict): a settings dictionary
            object_type (str): whether the dictionary is an experiment or schedule
        """
        if object_type == "experiment":
            if "reps" in dictionary:
                self.reps = dictionary["reps"]

            if "gens" in dictionary:
                self.gens = dictionary["gens"]

            if "pop_size" in dictionary:
                self.pop_size = dictionary["pop_size"]

            if "mut_rate" in dictionary:
                self.mut_rate = dictionary["mut_rate"]

            if "low_pheno" in dictionary:
                self.low_pheno = dictionary["low_pheno"]

            if "high_pheno" in dictionary:
                self.high_pheno = dictionary["high_pheno"]

            if "fdf_type" in dictionary:
                self.fdf_type = dictionary["fdf_type"]

            if "fitness_landscape" in dictionary:
                self.fitness_landscape = dictionary["fitness_landscape"]

            if "recombination_method" in dictionary:
                self.recombination_method = dictionary["recombination_method"]

            if "reinitialize_population" in dictionary:
                self.reinitialize_population = dictionary["reinitialize_population"]

            if "fdf_mean" in dictionary:
                self.fdf_mean = dictionary["fdf_mean"]

        if object_type == "experiment" or "schedule":
            if "left_sched_response_class_lower_bound" in dictionary:
                self.left_sched_response_class_lower_bound = dictionary[
                    "left_sched_response_class_lower_bound"
                ]

            if "left_sched_response_class_upper_bound" in dictionary:
                self.left_sched_response_class_upper_bound = dictionary[
                    "left_sched_response_class_upper_bound"
                ]

            if "left_sched" in dictionary:
                self.left_sched = dictionary["left_sched"]

            if "left_sched_interval_type" in dictionary:
                self.left_sched_interval_type = dictionary["left_sched_interval_type"]

            if "left_sched_fdf_mean" in dictionary:
                self.left_sched_fdf_mean = dictionary["left_sched_fdf_mean"]

            if "right_sched_response_class_lower_bound" in dictionary:
                self.right_sched_response_class_lower_bound = dictionary[
                    "right_sched_response_class_lower_bound"
                ]

            if "right_sched_response_class_upper_bound" in dictionary:
                self.right_sched_response_class_upper_bound = dictionary[
                    "right_sched_response_class_upper_bound"
                ]

            if "right_sched" in dictionary:
                self.right_sched = dictionary["right_sched"]

            if "right_sched_interval_type" in dictionary:
                self.right_sched_interval_type = dictionary["right_sched_interval_type"]

            if "right_sched_fdf_mean" in dictionary:
                self.right_sched_fdf_mean = dictionary["right_sched_fdf_mean"]
