from settings_classes import ScheduleData
from organisms import Organism
from algorithm_strategies import (
    fdf_sampling_strategies,
    fitness_calculation_strategies,
    mutation_strategies,
    punishment_strategies,
    recombination_strategies,
    selection_strategies,
)
from rules import selection


class Algorithm:
    """The Algorithm class is responsible for running the reinforcement and punishment algorithms.

    Attributes:
        ScheduleData: The settings from the schedule running the algorithm.
        Organism: The organism going through the algorithm.
        StrategyMap: A dictionary that maps the strings from the input '.json' file to the corresponding strategy classes.

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

    def __init__(self, schedule_data: ScheduleData, organism: Organism):
        self.schedule_data = schedule_data
        self.organism = organism
        self._set_strategies()

    def _set_strategies(self) -> None:
        """Sets the strategies for the algorithm based on the schedule data."""

        self.fdf_sampling_strategy = self.strategy_map[self.schedule_data.fdf_type]()
        self.fitness_calculation_strategy = self.strategy_map[
            self.schedule_data.fitness_landscape
        ]()
        self.selection_strategy = self.strategy_map[self.schedule_data.selection_type](
            self.fdf_sampling_strategy.sample
        )
        self.recombination_strategy = self.strategy_map[
            self.schedule_data.recombination_method
        ]()
        self.mutation_strategy = self.strategy_map[self.schedule_data.mutation_method]()
        self.punishment_strategy = self.strategy_map[
            self.schedule_data.punishment_type
        ]()

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
        ...

    def run(self, reinforced: bool, punished: bool) -> None:
        """Runs the reinforcement and punishment algorithms."""
        # run the reinforcement algorithm
        self.run_reinforcement(reinforced)

        # run the punishment algorithm
        self.run_punishment(punished)