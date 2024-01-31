from pyetbd.organisms import Organism
from pyetbd.schedules import Schedule
from pyetbd.settings_classes import ExperimentSettings
from pyetbd.algorithm import Algorithm
import pandas as pd


class Experiment:
    def __init__(
        self,
        settings: ExperimentSettings,
        schedule_arrangements: list[list[Schedule]],
    ):
        self.settings = settings
        self.schedule_arrangements = schedule_arrangements
        self._create_organism()
        self._create_output_dict()
        self._create_algorithm()

    def _create_organism(self):
        self.organism = Organism()

    def _create_algorithm(self):
        self.algorithm = Algorithm(self.organism)

    def _create_output_dict(self):
        self.data_output = {
            "Rep": [],
            "Sch": [],
            "Gen": [],
            "Emissions": [],
        }
        for i in range(len(self.schedule_arrangements[0])):
            self.data_output[f"B{i}"] = []
            self.data_output[f"R{i}"] = []
            self.data_output[f"P{i}"] = []

    def _save_data(self):
        df = pd.DataFrame(self.data_output)
        df.to_csv(f"{self.settings.file_stub}.csv")

    def run(self):
        for rep in range(self.settings.reps):
            for arrangement in self.schedule_arrangements:
                if self.settings.reinitialize_population:
                    self.organism.init_population()

                for gen in range(self.settings.gens):
                    self.organism.emit()
                    self.data_output["Rep"].append(rep)
                    self.data_output["Sch"].append(
                        self.schedule_arrangements.index(arrangement)
                    )
                    self.data_output["Gen"].append(gen)
                    self.data_output["Emissions"].append(self.organism.emitted)

                    reinforcement_available = False
                    schedule_to_deliver_reinforcement = (
                        self.settings
                    )  # default to the experiment settings
                    punishment_available = False
                    schedule_to_deliver_punishment = self.settings

                    for schedule in arrangement:
                        if schedule.in_response_class(self.organism.emitted):
                            self.data_output[f"B{arrangement.index(schedule)}"].append(
                                1
                            )

                        else:
                            self.data_output[f"B{arrangement.index(schedule)}"].append(
                                0
                            )

                        if schedule.settings.is_reinforcement_schedule:
                            self.data_output[f"P{arrangement.index(schedule)}"].append(
                                0
                            )
                            reinforced = schedule.run(self.organism.emitted)

                            if reinforced:
                                schedule_to_deliver_reinforcement = schedule.settings
                                reinforcement_available = True
                                self.data_output[
                                    f"R{arrangement.index(schedule)}"
                                ].append(1)

                            else:
                                self.data_output[
                                    f"R{arrangement.index(schedule)}"
                                ].append(0)

                        else:
                            self.data_output[f"R{arrangement.index(schedule)}"].append(
                                0
                            )
                            punished = schedule.run(self.organism.emitted)

                            if punished:
                                schedule_to_deliver_punishment = schedule.settings
                                punishment_available = True
                                self.data_output[
                                    f"P{arrangement.index(schedule)}"
                                ].append(1)

                            else:
                                self.data_output[
                                    f"P{arrangement.index(schedule)}"
                                ].append(0)

                    self.algorithm.run(
                        reinforcement_available,
                        punishment_available,
                        schedule_to_deliver_reinforcement,
                        schedule_to_deliver_punishment,
                    )

                    if gen % 1000 == 0:
                        print(
                            f"Rep: {rep}, Sch: {self.schedule_arrangements.index(arrangement)}, Gen: {gen}, Emission: {self.organism.emitted}"
                        )

        self._save_data()
