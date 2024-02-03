from pyetbd.experiment_runner import ExperimentRunner

input_files = [
    "example_inputs/test.json",
]


output_dir = "outputs"

for input_file in input_files:
    runner = ExperimentRunner(input_file, output_dir)
    runner.giddyup()
