from pyETBD.utils.experiment_builder import ExperimentBuilder


class ExperimentRunner:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        self.Builder = ExperimentBuilder(self.input_file, self.output_dir)

    def giddyup(self):
        self.Builder.build_experiments()

        for experiment in self.Builder.experiments:
            experiment.run()

        print("\U0001F40E Done Giddyuped! \U0001F40E")
