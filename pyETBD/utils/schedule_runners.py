from pyETBD.schedules import IntervalSchedule
from pyETBD.organisms import AnOrganism
from pyETBD.algorithm import selection, recombination, mutation


class ConcurrentSchedRunner:
    def __init__(
        self, left_sched_params: dict, right_sched_params: dict, organism_params: dict
    ):
        """Initializes the ConcurrentSchRunner class.

        Args:
            left_sch_params (dict): the parameters for the left schedule
            right_sch_params (dict): the parameters for the right schedule
            organism_params (dict): the parameters for the organism
        """

        self.left_sched_params = left_sched_params
        self.right_sched_params = right_sched_params
        self.organism_params = organism_params

        self.set_up()

    def set_up(self):
        """Sets up the concurrent schedule runner."""

        self.left_sched = IntervalSchedule(
            self.left_sched_params["response_class_lower_bound"],
            self.left_sched_params["response_class_upper_bound"],
            self.left_sched_params["interval_mean"],
            self.left_sched_params["interval_type"],
            self.left_sched_params["fdf_mean"],
        )
        self.right_sched = IntervalSchedule(
            self.right_sched_params["response_class_lower_bound"],
            self.right_sched_params["response_class_upper_bound"],
            self.right_sched_params["interval_mean"],
            self.right_sched_params["interval_type"],
            self.right_sched_params["fdf_mean"],
        )
        self.organism = AnOrganism(
            self.organism_params["pop_size"],
            self.organism_params["mut_rate"],
            self.organism_params["low_pheno"],
            self.organism_params["high_pheno"],
            self.organism_params["fdf_type"],
            self.organism_params["fitness_landscape"],
            self.organism_params["recombination_method"],
        )

        # dictionary used to store the data
        self.data_dict = {
            "Emissions": [],
            "R1": [],
            "B1": [],
            "R2": [],
            "B2": [],
        }

    def fitness_based_selection(self, schedule: str):
        """Does fitness-based selection on the organism's population.

        Args:
            schedule (str): which schedule reinforcement was delivered on

        Raises:
            ValueError: if schedule is not either "left" or "right"
        """
        if schedule == "left":
            parents = selection.fitness_search_selection(
                self.organism.population,
                self.organism.fdf_type,
                self.left_sched.fdf_mean,
                self.organism.fitness_landscape,
                self.organism.high_pheno,
                self.organism.emitted,
            )

        elif schedule == "right":
            parents = selection.fitness_search_selection(
                self.organism.population,
                self.organism.fdf_type,
                self.right_sched.fdf_mean,
                self.organism.fitness_landscape,
                self.organism.high_pheno,
                self.organism.emitted,
            )

        else:
            raise ValueError("schedule must be either 'left' or 'right'")

        children_genos = recombination.recombine_parents(
            parents, self.organism.bin_length, self.organism.recombination_method
        )

        children_phenos = mutation.mutate_population(
            children_genos, self.organism.mut_rate
        )

        self.organism.replace_population(children_phenos)

    def random_selection(self):
        """Does random selection on the organism's population."""
        parents = selection.randomly_select_parents(self.organism.population)

        children_genos = recombination.recombine_parents(
            parents, self.organism.bin_length, self.organism.recombination_method
        )

        children_phenos = mutation.mutate_population(
            children_genos, self.organism.mut_rate
        )

        self.organism.replace_population(children_phenos)

    def return_data(self):
        """Returns and resets the data dictionary.

        Returns:
            dict: the data dictionary
        """
        return_data = self.data_dict.copy()

        self.data_dict = {
            "Emissions": [],
            "R1": [],
            "B1": [],
            "R2": [],
            "B2": [],
        }

        return return_data

    def run(self):
        """Runs the concurrent schedules. (1 generation)"""
        self.organism.emit()

        self.data_dict["Emissions"].append(self.organism.emitted)

        self.left_sched.counter += 1
        self.right_sched.counter += 1

        in_left_class = self.left_sched.check_response_class(self.organism.emitted)
        in_right_class = self.right_sched.check_response_class(self.organism.emitted)

        if in_left_class:
            self.data_dict["B1"].append(1)
            self.data_dict["B2"].append(0)

            if self.left_sched.check_reinforcement():
                self.data_dict["R1"].append(1)
                self.data_dict["R2"].append(0)

                self.fitness_based_selection("left")

            else:
                self.data_dict["R1"].append(0)
                self.data_dict["R2"].append(0)

                self.random_selection()

        elif in_right_class:
            self.data_dict["B1"].append(0)
            self.data_dict["B2"].append(1)

            if self.right_sched.check_reinforcement():
                self.data_dict["R1"].append(0)
                self.data_dict["R2"].append(1)

                self.fitness_based_selection("right")

            else:
                self.data_dict["R1"].append(0)
                self.data_dict["R2"].append(0)

                self.random_selection()

        else:
            self.data_dict["B1"].append(0)
            self.data_dict["B2"].append(0)
            self.data_dict["R1"].append(0)
            self.data_dict["R2"].append(0)

            self.random_selection()
