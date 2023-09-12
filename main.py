# this is an example script for running an experiment

# import the ExperimentRunner class from the utils module
from pyETBD.utils.experiment_runner import ExperimentRunner


# define the main function
def main():
    # define the input file and output directory
    input_file_path = "example_experiment_inputs/mcdowell_et_al_2008_phase1.json"

    # putting an empty string will output the same directory as the main.py file
    output_dir = ""
    # if you wanted to output to an 'outputs' directory in the same directory as main.py you would write:
    # output_dir = "outputs/" (be sure to include the trailing slash)
    # Note: the code will not create the directory for you, you must create it yourself

    # create an instance of the ExperimentRunner class
    runner = ExperimentRunner(input_file_path, output_dir)

    # call the giddyup method to run the experiments
    runner.giddyup()


# call the main function
if __name__ == "__main__":
    main()
