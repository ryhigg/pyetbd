import pandas as pd
from pyETBD import organisms
from pyETBD.utils import progress_bar, timer


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
        # check that the schedules are formatted correctly
        for schedule_arrangement in schedules:
            if len(schedules[0]) != len(schedule_arrangement):
                raise ValueError("All schedule arrangements must be the same length.")

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
            "emissions": [],
            "gen": [],
            "rep": [],
            "sched": [],
        }

        # create a variable for each schedule
        for i in range(len(schedules[0])):
            self.data_dict[f"R{i}"] = []
            self.data_dict[f"B{i}"] = []
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

                    self.data_dict["emissions"].append(self.organism.emitted)
                    self.data_dict["gen"].append(gen)
                    self.data_dict["rep"].append(rep)
                    self.data_dict["sched"].append(
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

    def get_response_class(self, schedules, emitted):
        """Gets the response class for the emitted response

        Args:
            emitted (int): the phenotype of the emitted response

        Returns:
            int: the response class of the emitted response
        """
        response_class = -1
        for i in range(len(schedules)):
            if schedules[i].check_response_class(emitted):
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
                    self.data_dict[f"R{i}"].append(1)
                    self.data_dict[f"B{i}"].append(1)
                else:
                    self.data_dict[f"R{i}"].append(0)
                    self.data_dict[f"B{i}"].append(1)

            elif i != response_class:
                self.data_dict[f"R{i}"].append(0)
                self.data_dict[f"B{i}"].append(0)

            else:
                raise ValueError("Invalid response class.")

    def output_data(self, output_dir: str = ""):
        """Saves the data to a csv file"""
        # create the dataframe
        data_df = pd.DataFrame(self.data_dict)

        # save the dataframe to a csv
        data_df.to_csv(f"{output_dir}{self.file_stub}.csv", index=False)
