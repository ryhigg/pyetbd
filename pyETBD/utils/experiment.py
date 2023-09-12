from pyETBD.utils import schedule_runners
from pyETBD.utils.progress_bar import ProgressBar
from pyETBD.utils.timer import timer
import pandas as pd
import csv


class Experiment:
    def __init__(
        self,
        organism_params: dict,
        schedules: dict,
        gens: int,
        reps: int,
        file_stub: str,
        experiment_type: str,
        reinitialize_population: bool,
        output_dir: str,
    ):
        """Initializes the Experiment class.

        Args:
            organism_params (dict): the parameters for the organism
            schedules (dict): the parameters for the schedules
            gens (int): the number of generations
            reps (int): the number of reps
            file_stub (str): the file stub for the data file
            experiment_type (str): the type of experiment
            reinitialize_population (bool): whether or not to reinitialize the population
            output_dir (str): the output directory
        """

        self.organism_params = organism_params
        self.schedules = schedules
        self.gens = gens
        self.reps = reps
        self.file_stub = file_stub
        self.experiment_type = experiment_type
        self.reinitialize_population = reinitialize_population
        self.output_dir = output_dir

        self.set_up()

    def set_up(self):
        """Sets up the experiment.

        Raises:
            NotImplementedError: if the experiment type is not implemented
        """

        self.final_population = None  # used if reinitialize_population is False

        if self.experiment_type == "concurrent":
            self.data_dict = {
                "File": [],
                "Rep": [],
                "Schedule": [],
                "Gen": [],
                "Emissions": [],
                "R1": [],
                "B1": [],
                "R2": [],
                "B2": [],
            }

            self.sched_runners = []

            for sched in self.schedules:
                sched_runner = schedule_runners.ConcurrentSchedRunner(
                    sched["left_sched_params"],
                    sched["right_sched_params"],
                    self.organism_params,
                )

                self.sched_runners.append(sched_runner)

            self.rep_progress_bar = ProgressBar(self.reps, "Rep:")
            self.sched_progress_bar = ProgressBar(len(self.schedules), "Sch:")
            self.gen_progress_bar = ProgressBar(self.gens, "Gen:")

        else:
            raise NotImplementedError

    def update_progress_bars(self, gen, sched_runner_idx, rep):
        """Updates the progress bars.

        Args:
            gen (int): the current generation
            sched_runner_idx (int): the current schedule runner index
            rep (int): the current rep
        """
        updates = [
            f"Experiment: {self.file_stub}",
            self.gen_progress_bar.update(gen),
            self.sched_progress_bar.update(sched_runner_idx),
            self.rep_progress_bar.update(rep),
        ]

        print("\n".join(updates))

    @timer
    def run(self):
        """Runs the experiment."""
        # looping for the number of reps
        for rep in range(self.reps):
            # looping for the number of schedules
            for sched_runner in self.sched_runners:
                # reinitializing the population if necessary
                if (
                    self.reinitialize_population
                    and self.sched_runners.index(sched_runner) != 0
                ):
                    sched_runner.organism.population = self.final_population

                # looping for the number of generations
                for gen in range(self.gens):
                    # running the concurrent schedules
                    sched_runner.run()

                    # updating the data dictionary
                    self.data_dict["File"].append(self.file_stub)
                    self.data_dict["Rep"].append(rep)
                    self.data_dict["Schedule"].append(
                        self.sched_runners.index(sched_runner)
                    )
                    self.data_dict["Gen"].append(gen)

                    # updating the progress bars every 1000 generations
                    if gen % 1000 == 0:
                        self.update_progress_bars(
                            gen, self.sched_runners.index(sched_runner), rep
                        )

                # getting the final population in case it is needed for the next schedule
                self.final_population = sched_runner.organism.population

                # getting the data from the schedule runner
                sched_data = sched_runner.return_data()

                # updating the data dictionary
                self.data_dict["Emissions"].extend(sched_data["Emissions"])
                self.data_dict["R1"].extend(sched_data["R1"])
                self.data_dict["B1"].extend(sched_data["B1"])
                self.data_dict["R2"].extend(sched_data["R2"])
                self.data_dict["B2"].extend(sched_data["B2"])

        # writing the data to a csv file
        self.write_data()
        # updating the progress bars when the loop is finished
        self.update_progress_bars(self.gens, len(self.sched_runners), self.reps)

    def write_data(self):
        """Writes the data to a csv file."""
        output_df = pd.DataFrame(self.data_dict)
        output_df.to_csv(self.output_dir + self.file_stub + ".csv", index=False)

        # self.write_experiment_params()

    # TODO: implement parameter writing

    # def write_experiment_params(self):
    #     with open(
    #         f"{self.output_dir}/{self.file_stub}_params.csv", "w", newline=""
    #     ) as csvfile:
    #         writing_dict = self.return_parameter_data()
    #         concatenated_list = []
    #         writer = csv.writer(csvfile)
    #         writer.writerow(["Parameter", "Value"])
    #         for key, value in writing_dict.items():
    #             if type(value) != list:
    #                 writer.writerow([key, value])
    #             else:
    #                 key_list = [key]
    #                 key_list.extend(value)
    #                 concatenated_list.append(key_list)
    #                 writer.writerow(item for item in key_list)
