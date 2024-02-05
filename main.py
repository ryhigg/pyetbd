from pyetbd.experiment_runner import ExperimentRunner

INPUT_FILE = "example_inputs/mcdowell_et_al_2008_phase1.json"
OUTPUT_DIR = ""  # this will save the output in the current directory, if you want to save it in a different directory, specify the path here (e.g. "outputs/") and make sure the directory exists before running the code


def main():
    runner = ExperimentRunner(INPUT_FILE, OUTPUT_DIR)
    runner.giddyup()


if __name__ == "__main__":
    main()
