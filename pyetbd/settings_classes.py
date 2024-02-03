from dataclasses import dataclass, field
from pyetbd.defaults import DEFAULTS


@dataclass
class ScheduleSettings:
    """
    A class representing schedule settings.
    """

    fdf_type: str = field(default_factory=lambda: DEFAULTS["fdf_type"])
    fdf_mean: float = field(default_factory=lambda: DEFAULTS["fdf_mean"])
    selection_type: str = field(default_factory=lambda: DEFAULTS["selection_type"])
    punishment_type: str = field(default_factory=lambda: DEFAULTS["punishment_type"])
    fitness_landscape: str = field(
        default_factory=lambda: DEFAULTS["fitness_landscape"]
    )
    recombination_method: str = field(
        default_factory=lambda: DEFAULTS["recombination_method"]
    )
    mut_rate: float = field(default_factory=lambda: DEFAULTS["mut_rate"])
    mutation_method: str = field(default_factory=lambda: DEFAULTS["mutation_method"])

    schedule_type: str = field(default_factory=lambda: DEFAULTS["schedule_type"])
    schedule_subtype: str = field(default_factory=lambda: DEFAULTS["schedule_subtype"])
    mean: int = field(default_factory=lambda: DEFAULTS["mean"])
    response_class_lower_bound: int = field(
        default_factory=lambda: DEFAULTS["response_class_lower_bound"]
    )
    response_class_upper_bound: int = field(
        default_factory=lambda: DEFAULTS["response_class_upper_bound"]
    )
    response_class_size: int = field(
        default_factory=lambda: DEFAULTS["response_class_size"]
    )
    excluded_lower_bound: int = field(
        default_factory=lambda: DEFAULTS["excluded_lower_bound"]
    )
    excluded_upper_bound: int = field(
        default_factory=lambda: DEFAULTS["excluded_upper_bound"]
    )
    is_reinforcement_schedule: bool = field(
        default_factory=lambda: DEFAULTS["is_reinforcement_schedule"]
    )


@dataclass
class ExperimentSettings(ScheduleSettings):
    """
    A class representing experiment settings. This also includes schedule settings.

    Attributes:
        file_stub (str): The file stub for the output files.
        reps (int): The number of replications.
        pop_size (int): The population size.
        low_pheno (int): The lower bound of the phenotype.
        high_pheno (int): The upper bound of the phenotype.
        schedules (list): A list of schedule settings.
    """

    gens: int = field(default_factory=lambda: DEFAULTS["gens"])
    file_stub: str = field(default_factory=lambda: DEFAULTS["file_stub"])
    reps: int = field(default_factory=lambda: DEFAULTS["reps"])
    pop_size: int = field(default_factory=lambda: DEFAULTS["pop_size"])
    low_pheno: int = field(default_factory=lambda: DEFAULTS["low_pheno"])
    high_pheno: int = field(default_factory=lambda: DEFAULTS["high_pheno"])
    reinitialize_population: bool = field(
        default_factory=lambda: DEFAULTS["reinitialize_population"]
    )
    schedules: list = field(default_factory=list)
