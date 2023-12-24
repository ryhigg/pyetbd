# this is an example script for running an experiment

# import the ExperimentRunner class from the utils module
from pyETBD.experiment_handler import ExperimentHandler

# the folder containing the input file(s)
INPUT_FILE_PATH = "example_experiment_inputs/mcdowell_et_al_2008_phase1.json"

# putting an empty string will output the same directory as the main.py file
OUTPUT_DIR = ""

# if you wanted to output to an 'outputs' directory in the same directory as main.py you would write:
# OUTPUT_DIR = "outputs/" (be sure to include the trailing slash)
# Note: the code will not create the directory for you, you must create it yourself


# define the main function
def main():
    # create an instance of the ExperimentHandler class
    runner = ExperimentHandler(INPUT_FILE_PATH, OUTPUT_DIR)

    # call the giddyup method to run the experiments
    runner.giddyup()


# call the main function
if __name__ == "__main__":
    main()
