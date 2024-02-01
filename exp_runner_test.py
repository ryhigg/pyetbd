from pyetbd.experiment_runner import ExperimentRunner

input_file = "example_inputs/test.json"
output_dir = ""

runner = ExperimentRunner(input_file, output_dir)
runner.giddyup()
