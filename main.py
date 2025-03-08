from pyetbd.experiment_runner import ExperimentRunner

INPUT_FILE = "example_inputs/test.json"  # can also take a dictionary as input
OUTPUT_DIR = ""  # this will save the output in the current directory, if you want to save it in a different directory, specify the path here (e.g. "outputs/"), the directory will be created if it does not exist


def main():
    runner = ExperimentRunner(INPUT_FILE, OUTPUT_DIR)
    runner.giddyup()


if __name__ == "__main__":
    main()
