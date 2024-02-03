from pyetbd.settings_classes import ScheduleSettings, ExperimentSettings
from pyetbd.organisms import Organism
from pyetbd.rules import selection
from pyetbd.algorithm_strategies import (
    fdf_sampling_strategies,
    fitness_calculation_strategies,
    mutation_strategies,
    punishment_strategies,
    recombination_strategies,
    selection_strategies,
)


class Algorithm:
    """The Algorithm class is responsible for running the reinforcement and punishment algorithms.

    The algorithm class works closely with the modules in the algorithm_strategies package to implement the rules of the ETBD algorithm on the organism.

    Attributes:
        ScheduleData: The settings from the schedule running the algorithm.
        Organism: The organism going through the algorithm.
        strategy_map: A dictionary that maps the strings from the input '.json' file to the corresponding strategy classes.

    """

    strategy_map = {
        "linear_fdf": fdf_sampling_strategies.LinearFDF,
        "exponential_fdf": fdf_sampling_strategies.ExponentialFDF,
        "rla": punishment_strategies.RLAPunishment,
        "fitness_search": selection_strategies.FitnessSearchSelection,
        "circular_landscape": fitness_calculation_strategies.CircularFitnessCalculation,
        "linear_landscape": fitness_calculation_strategies.LinearFitnessCalculation,
        "bitwise": recombination_strategies.BitwiseRecombination,
        "bit_flip": mutation_strategies.BitFlipMutation,
    }

    def __init__(self, organism: Organism):
        self.organism = organism

    def set_schedule(
        self, schedule_settings: ScheduleSettings | ExperimentSettings
    ) -> None:
        """Sets the schedule data for the algorithm."""
        self.schedule_setttings = schedule_settings
        self._set_strategies()

    def _set_strategies(self) -> None:
        """Sets the strategies for the algorithm based on the schedule data."""

        self.fdf_sampling_strategy = self.strategy_map[
            self.schedule_setttings.fdf_type
        ](self.schedule_setttings)
        self.fitness_calculation_strategy = self.strategy_map[
            self.schedule_setttings.fitness_landscape
        ](self.organism)
        self.selection_strategy = self.strategy_map[
            self.schedule_setttings.selection_type
        ](
            self.organism,
            self.schedule_setttings,
            self.fdf_sampling_strategy.get_sample_func(),
        )
        self.recombination_strategy = self.strategy_map[
            self.schedule_setttings.recombination_method
        ](self.organism)
        self.mutation_strategy = self.strategy_map[
            self.schedule_setttings.mutation_method
        ](self.organism, self.schedule_setttings)
        self.punishment_strategy = self.strategy_map[
            self.schedule_setttings.punishment_type
        ](self.organism, self.schedule_setttings)

    def run_reinforcement(self, reinforced: bool) -> None:
        """Runs the reinforcement algorithm."""
        if reinforced:
            # calculate the fitness values for the population
            self.organism.fitness_values = (
                self.fitness_calculation_strategy.calculate_fitness()
            )

            # select the parents based on the selection strategy
            self.organism.parents = self.selection_strategy.select()

        else:
            # select the parents randomly
            self.organism.parents = selection.randomly_select_parents(
                self.organism.population
            )

        # recombine the parents based on the recombination strategy
        self.organism.offspring_genos = self.recombination_strategy.recombine()
        # mutate the offspring based on the mutation strategy and replace the population with the offspring
        self.organism.population = self.mutation_strategy.mutate()

    def run_punishment(self, punished: bool) -> None:
        """Runs the punishment algorithm."""
        # perform the punishment on the population

        # replace the organism's population with the new population from the punishment strategy
        pass

    def run(
        self,
        reinforced: bool,
        punished: bool,
        reinforcement_schedule_settings: ScheduleSettings,
        punishment_schedule_settings: ScheduleSettings,
    ) -> None:
        """Runs the reinforcement and punishment algorithms."""
        # set the schedule
        self.set_schedule(reinforcement_schedule_settings)

        # run the reinforcement algorithm
        self.run_reinforcement(reinforced)

        # set the schedule
        self.set_schedule(punishment_schedule_settings)

        # run the punishment algorithm
        self.run_punishment(punished)
