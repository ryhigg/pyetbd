from pyetbd.experiment_runner import ExperimentRunner

INPUT_FILE = "example_inputs/mcdowell_et_al_2008_phase1.json"
OUTPUT_DIR = "outputs"


def main():
    runner = ExperimentRunner(INPUT_FILE, OUTPUT_DIR)
    runner.giddyup()


if __name__ == "__main__":
    main()
