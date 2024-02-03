from pyetbd.experiment_runner import ExperimentRunner

input_files = [
    "example_inputs/mcdowell_et_al_2008_phase1.json",
]

# "example_inputs/mcdowell_et_al_2008_phase2.json",
# "example_inputs/mcdowell_et_al_2008_phase3.json",
output_dir = "outputs"

for input_file in input_files:
    runner = ExperimentRunner(input_file, output_dir)
    runner.giddyup()
