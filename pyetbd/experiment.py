from pyetbd.organisms import Organism
from pyetbd.schedules import Schedule
from pyetbd.settings_classes import ExperimentSettings
from pyetbd.algorithm import Algorithm
from pyetbd.utils import progress_logger, timer
from pyetbd.data_saver import DataSaver


class Experiment:
    """
    Represents an experiment that runs an AO on a set of schedule arrangements.

    Args:
        settings (ExperimentSettings): The settings for the experiment.
        schedule_arrangements (list[list[Schedule]]): The schedule arrangements to run the organism on.
        log_progress (bool): Flag indicating whether to log the progress of the experiment.
        output_dir (str): The directory to save the experiment data.

    Attributes:
        settings (ExperimentSettings): The settings for the experiment.
        schedule_arrangements (list[list[Schedule]]): The schedule arrangements to run the algorithm on.
        log_progress (bool): Flag indicating whether to log the progress of the experiment.
        output_dir (str): The directory to save the experiment data.
        organism (Organism): The organism used in the experiment.
        algorithm (Algorithm): The algorithm object used to implement the rules on the AO.
        progress_logger (ProgressLogger): The progress logger used in the experiment.
        data_saver (DataSaver): The data saver used in the experiment.

    Methods:
        run: Runs the experiment.
    """

    def __init__(
        self,
        settings: ExperimentSettings,
        schedule_arrangements: list[list[Schedule]],
        log_progress: bool,
        output_dir: str,
    ):
        self.settings = settings
        self.schedule_arrangements = schedule_arrangements
        self.log_progress = log_progress
        self.output_dir = output_dir
        self._create_organism()
        self._create_data_saver()
        self._create_algorithm()
        self._create_progress_logger()

    def _create_organism(self) -> None:
        """
        Creates a new organism and assigns it to the `organism` attribute.
        """
        self.organism = Organism()

    def _create_algorithm(self) -> None:
        """
        Creates an instance of the Algorithm class using the current organism. The algorithm class is responsible for implementing the rules of the ETBD algorithm on the organism.
        """
        self.algorithm = Algorithm(self.organism)

    def _create_progress_logger(self) -> None:
        """
        Creates a progress logger object and initializes progress bars.

        The progress logger is responsible for tracking the progress of the experiment.
        It creates progress bars based on the number of repetitions, schedule arrangements,
        and generations specified in the settings.
        """
        self.progress_logger = progress_logger.ProgressLogger(self.settings.file_stub)
        self.progress_logger.create_progress_bars(
            self.settings.reps, len(self.schedule_arrangements), self.settings.gens
        )

    def _create_data_saver(self) -> None:
        """
        Creates a DataSaver object and assigns it to the `data_saver` attribute.
        The DataSaver object is initialized with the experiment settings and output directory.
        The DataSaver object is responsible for storing and saving the data from each experiment.
        """
        self.data_saver = DataSaver(self.settings, self.output_dir)
        self.data_saver.add_schedule_outputs(len(self.schedule_arrangements[0]))

    @timer.timer
    def run(self) -> None:
        """
        Runs the experiment.

        The experiment runs the genetic algorithm on each schedule arrangement for the specified number of repetitions
        and generations. It logs the progress if enabled and saves the experiment data at the end.
        """

        for rep in range(self.settings.reps):
            for arrangement in self.schedule_arrangements:
                if self.settings.reinitialize_population:
                    self.organism.init_population()

                for gen in range(self.settings.gens):
                    # emit the response
                    self.organism.emit()

                    # update the data_output with the current repetition, schedule arrangement, generation, and emitted response
                    self.data_saver.data_output["Rep"].append(rep)
                    self.data_saver.data_output["Sch"].append(
                        self.schedule_arrangements.index(arrangement)
                    )
                    self.data_saver.data_output["Gen"].append(gen)
                    self.data_saver.data_output["Emissions"].append(
                        self.organism.emitted
                    )

                    # initialize reinforcement and punishment flags and schedules
                    reinforcement_available = False
                    schedule_to_deliver_reinforcement = (
                        self.settings
                    )  # default to the experiment settings
                    punishment_available = False
                    schedule_to_deliver_punishment = self.settings

                    # run each schedule in the arrangement
                    for schedule in arrangement:
                        # update whether the emitted response is in the response class
                        if schedule.in_response_class(self.organism.emitted):
                            self.data_saver.data_output[
                                f"B{arrangement.index(schedule)+1}"
                            ].append(1)

                        else:
                            self.data_saver.data_output[
                                f"B{arrangement.index(schedule)+1}"
                            ].append(0)

                        # run the schedule and update the data_output if the schedule is a reinforcement schedule
                        if schedule.settings.is_reinforcement_schedule:
                            # update the data_output to indicate that punishment was not delivered because the schedule is not a punishment schedule
                            self.data_saver.data_output[
                                f"P{arrangement.index(schedule)+1}"
                            ].append(0)
                            # run the schedule and find out if reinforcement is available
                            reinforced = schedule.run(self.organism.emitted)

                            if reinforced:
                                # update the schedule to deliver reinforcement
                                schedule_to_deliver_reinforcement = schedule.settings
                                # update the reinforcement flag to indicate to the algorithm that reinforcement should be delivered
                                reinforcement_available = True
                                # update the data_output to indicate that reinforcement was delivered
                                self.data_saver.data_output[
                                    f"R{arrangement.index(schedule)+1}"
                                ].append(1)

                            else:
                                # update the data_output to indicate that reinforcement was not delivered
                                self.data_saver.data_output[
                                    f"R{arrangement.index(schedule)+1}"
                                ].append(0)

                        # run the schedule and update the data_output if the schedule is a punishment schedule
                        else:
                            # update the data_output to indicate that reinforcement was not delivered because the schedule is not a reinforcement schedule
                            self.data_saver.data_output[
                                f"R{arrangement.index(schedule)+1}"
                            ].append(0)
                            # run the schedule and find out if punishment is available
                            punished = schedule.run(self.organism.emitted)

                            if punished:
                                # update the schedule to deliver punishment
                                schedule_to_deliver_punishment = schedule.settings
                                # update the punishment flag to indicate to the algorithm that punishment should be delivered
                                punishment_available = True
                                # update the data_output to indicate that punishment was delivered
                                self.data_saver.data_output[
                                    f"P{arrangement.index(schedule)+1}"
                                ].append(1)

                            else:
                                # update the data_output to indicate that punishment was not delivered
                                self.data_saver.data_output[
                                    f"P{arrangement.index(schedule)+1}"
                                ].append(0)

                    # run the algorithm on the organism
                    self.algorithm.run(
                        reinforcement_available,
                        punishment_available,
                        schedule_to_deliver_reinforcement,
                        schedule_to_deliver_punishment,
                    )

                    # update the progress of the experiment
                    if gen % 1000 == 0 and self.log_progress:
                        self.progress_logger.log_progress(
                            rep, self.schedule_arrangements.index(arrangement), gen
                        )

        # update the progress of the experiment
        if self.log_progress:
            self.progress_logger.log_progress(
                self.settings.reps,
                len(self.schedule_arrangements),
                self.settings.gens,
                end="\n",
            )

        # save the experiment data
        print("Saving data...")
        self.data_saver.save_data()
