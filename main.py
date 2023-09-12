# this is an example script for running an experiment

# import the ExperimentRunner class from the utils module
from pyETBD.utils.experiment_runner import ExperimentRunner


# define the main function
def main():
    # define the input file and output directory
    input_file = "example_experiment_inputs/mcdowell_et_al_2008_phase1.json"
    output_dir = ""

    # create an instance of the ExperimentRunner class
    runner = ExperimentRunner(input_file, output_dir)

    # call the giddyup method to run the experiments
    runner.giddyup()


# call the main function
if __name__ == "__main__":
    main()
