import pandas as pd
from pyetbd import organisms
from pyetbd.utils import progress_bar, timer


class Experiment:
    """Class for running an experiment"""

    def __init__(
        self,
        schedules: list,
        repetitions: int,
        generations: int,
        reinit_pop: bool,
        organism: organisms.AnOrganism,
        file_stub: str,
    ):
        """Initializes an experiment

        Important note: it is possible to have more than 2 schedules in an experiment, but all the arrangements must be the same length (e.g., [[left_sched, right_sched], [left_sched, right_sched]], [[left_sched, right_sched, middle_sched], [left_sched, right_sched, middle_sched]]).

        Also, schedules should not have overlapping response classes.

        Args:
            schedules (list): nested list of schedule objects (e.g., [[left_sched, right_sched], [left_sched, right_sched]])
            repetitions (int): number of times to repeat the experiment
            generations (int): number of generations to run the experiment
            reinit_pop (bool): whether or not to reinitialize the population between schedule arrangements
            organism (object): the organism object to use for the experiment
        """

        self.schedule_arrangement_length = len(schedules[0])

        # store the experiment parameters
        self.schedules = schedules
        self.repetitions = repetitions
        self.generations = generations
        self.reinit_pop = reinit_pop
        self.organism = organism
        self.file_stub = file_stub

        # dictionary to store the data
        self.data_dict = {
            "Emissions": [],
            "Gen": [],
            "Rep": [],
            "Schedule": [],
        }

        # create a variable for each schedule
        for i in range(len(schedules[0])):
            self.data_dict[f"R{i+1}"] = []
            self.data_dict[f"B{i+1}"] = []
            # need to add punishment eventually # TODO: add punishment

        # create a progress bar
        self.rep_progress_bar = progress_bar.ProgressBar(self.repetitions, prefix="Rep")
        self.sched_progress_bar = progress_bar.ProgressBar(len(schedules), prefix="Sch")
        self.gen_progress_bar = progress_bar.ProgressBar(self.generations, prefix="Gen")

    @timer.timer
    def run(self):
        """Runs the experiment"""
        for rep in range(self.repetitions):
            for schedule_arrangement in self.schedules:
                if self.reinit_pop:
                    self.organism.init_population()

                for gen in range(self.generations):
                    self.organism.emit()
                    self.update_schedule_counters(schedule_arrangement)

                    self.data_dict["Emissions"].append(self.organism.emitted)
                    self.data_dict["Gen"].append(gen)
                    self.data_dict["Rep"].append(rep)
                    self.data_dict["Schedule"].append(
                        self.schedules.index(schedule_arrangement)
                    )

                    response_class = self.get_response_class(
                        schedule_arrangement, self.organism.emitted
                    )

                    if response_class == -1:
                        self.organism.no_reinforcement_delivered()
                        self.update_data_dict(response_class, False)
                        continue

                    if schedule_arrangement[response_class].check_reinforcement(
                        self.organism.emitted
                    ):
                        self.organism.reinforcement_delivered(
                            schedule_arrangement[response_class].fdf_mean,
                            schedule_arrangement[response_class].fdf_type,
                        )
                        self.update_data_dict(response_class, True)

                    else:
                        self.organism.no_reinforcement_delivered()
                        self.update_data_dict(response_class, False)

                    if gen % 100 == 0:
                        self.update_progress_bar(
                            rep, self.schedules.index(schedule_arrangement), gen
                        )

        self.update_progress_bar(
            self.repetitions, len(self.schedules), self.generations
        )

    def update_progress_bar(self, rep, schedule_arrangement, gen):
        """Updates the progress bar

        Args:
            rep (int): the current repetition
            schedule_arrangement (list): the current schedule arrangement
            gen (int): the current generation
        """
        self.rep_progress_bar.clear_terminal()

        print(
            f"Exp: {self.file_stub}\n{self.rep_progress_bar.update(rep)}\n{self.sched_progress_bar.update(schedule_arrangement)}\n{self.gen_progress_bar.update(gen)}"
        )

    def update_schedule_counters(self, schedules):
        """Updates the counters for each schedule in the schedule arrangement

        Args:
            schedules (list): the current schedule arrangement
        """
        for schedule in schedules:
            schedule.update_counter(self.organism.emitted)

    def get_response_class(self, schedules, emitted):
        """Gets the response class for the emitted response

        Args:
            emitted (int): the phenotype of the emitted response

        Returns:
            int: the response class of the emitted response
        """
        response_class = -1
        for i in range(len(schedules)):
            if schedules[i].in_response_class(emitted):
                response_class = i
                break

        return response_class

    def update_data_dict(self, response_class, reinforced):
        """Updates the data dictionary with the response class and reinforcement

        Args:
            response_class (int): the response class of the emitted response
            reinforced (bool): whether or not the response was reinforced
        """
        for i in range(self.schedule_arrangement_length):
            if i == response_class:
                if reinforced:
                    self.data_dict[f"R{i+1}"].append(1)
                    self.data_dict[f"B{i+1}"].append(1)
                else:
                    self.data_dict[f"R{i+1}"].append(0)
                    self.data_dict[f"B{i+1}"].append(1)

            elif i != response_class:
                self.data_dict[f"R{i+1}"].append(0)
                self.data_dict[f"B{i+1}"].append(0)

            else:
                raise ValueError("Invalid response class.")

    def output_data(self, output_dir: str = ""):
        """Saves the data to a csv file"""
        print("Saving data...")

        # create the dataframe
        data_df = pd.DataFrame(self.data_dict)

        # save the dataframe to a csv
        data_df.to_csv(f"{output_dir}{self.file_stub}.csv", index=False)

        self.format_data()

    def format_data(self):
        """Formats the data into bins of 500 generations and outputs to an excel file with the parameters"""
        df = pd.DataFrame(self.data_dict)

        df["bin"] = df.index // 500

        formatted_df = df.groupby(["Rep", "Schedule", "bin"]).sum().reset_index()

        formatted_df.drop(columns=["Gen", "Emissions", "bin"], inplace=True)

        param_df = pd.DataFrame(self.get_experiment_param_dict())

        # save the data to a .xlsx file where the first sheet is the parameters and the second sheet is the data
        with pd.ExcelWriter(f"{self.file_stub}.xlsx") as writer:
            param_df.to_excel(writer, sheet_name="params", index=False)
            formatted_df.to_excel(writer, sheet_name="data", index=False)

    def get_experiment_param_dict(self):
        """Returns a dictionary of the experiment parameters"""

        param_dict = {
            "file_stub": self.file_stub,
            "repetitions": self.repetitions,
            "generations": self.generations,
            "reinit_pop": self.reinit_pop,
            "population_size": self.organism.pop_size,
            "low_pheno": self.organism.low_pheno,
            "high_pheno": self.organism.high_pheno,
            "mut_rate": self.organism.mut_rate,
            "fitness_landscape": self.organism.fitness_landscape,
            "fdf_type": self.organism.fdf_type,
            "recombination_method": self.organism.recombination_method,
            "schedule_arrangement": [],
            "schedule_index_in_arrangement": [],
            "schedule_fdf_mean": [],
            "schedule_fdf_type": [],
            "schedule_type": [],
            "schedule_subtype": [],
            "schedule_mean": [],
            "schedule_response_class_lower_bound": [],
            "schedule_response_class_upper_bound": [],
            "schedule_response_class_size": [],
            "schedule_response_classes": [],
            "schedule_response_class_excluded_values": [],
        }
        for schedule_arrangement in self.schedules:
            for schedule in schedule_arrangement:
                param_dict["schedule_arrangement"].append(
                    self.schedules.index(schedule_arrangement)
                )
                param_dict["schedule_index_in_arrangement"].append(
                    schedule_arrangement.index(schedule)
                )
                param_dict["schedule_type"].append(schedule.schedule_type)
                param_dict["schedule_subtype"].append(schedule.schedule_subtype)
                param_dict["schedule_fdf_type"].append(schedule.fdf_type)
                param_dict["schedule_fdf_mean"].append(schedule.fdf_mean)
                param_dict["schedule_mean"].append(schedule.mean)
                param_dict["schedule_response_class_lower_bound"].append(
                    schedule.response_class_lower_bound
                )
                param_dict["schedule_response_class_upper_bound"].append(
                    schedule.response_class_upper_bound
                )
                param_dict["schedule_response_class_size"].append(
                    schedule.response_class_size
                )
                param_dict["schedule_response_classes"].append(
                    schedule.response_class.tolist()
                )
                param_dict["schedule_response_class_excluded_values"].append(
                    f"{schedule.excluded_lower_bound}-{schedule.excluded_upper_bound}"
                )

        return param_dict
