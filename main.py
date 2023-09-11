# Example script for running concurrent schedules
# This script will run phase 1 from McDowell et al., 2008
from pyETBD.utils import schedule_runners
from pyETBD.utils import equations
from pyETBD.utils.progress_bar import ProgressBar
import pandas as pd

# experiment settings
REPS = 10

# dict containing the organism parameters
ORGANISM_PARAMS = {
    "pop_size": 100,
    "mut_rate": 0.1,
    "low_pheno": 0,
    "high_pheno": 1023,
    "fdf_type": "linear",
    "fitness_landscape": "circular",
    "recombination_method": "bitwise",
}

# schedule parameters
LEFT_RESPONSE_CLASS_LOWER_BOUND = 471
LEFT_RESPONSE_CLASS_UPPER_BOUND = 511
RIGHT_RESPONSE_CLASS_LOWER_BOUND = 512
RIGHT_RESPONSE_CLASS_UPPER_BOUND = 552
LEFT_FDF_MEAN = 40
RIGHT_FDF_MEAN = 40
LEFT_SCHEDS = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
RIGHT_SCHEDS = LEFT_SCHEDS[::-1]  # reverse the list


def main():
    # dictionary used to store the data
    data_dict = {
        "Rep": [],
        "Schedule": [],
        "Gen": [],
        "Emissions": [],
        "R1": [],
        "B1": [],
        "R2": [],
        "B2": [],
    }

    # creating progress bars to track execution in the terminal
    rep_progress_bar = ProgressBar(REPS, "Rep:")
    sched_progress_bar = ProgressBar(len(LEFT_SCHEDS), "Sch:")
    gen_progress_bar = ProgressBar(20500, "Gen:")

    # looping for the number of reps
    for rep in range(REPS):
        # looping for the number of schedules
        for i in range(len(LEFT_SCHEDS)):
            # updating the left and right schedule parameters
            left_sched_params = {
                "response_class_lower_bound": LEFT_RESPONSE_CLASS_LOWER_BOUND,
                "response_class_upper_bound": LEFT_RESPONSE_CLASS_UPPER_BOUND,
                "interval_mean": LEFT_SCHEDS[i],
                "interval_type": "random",
                "fdf_mean": LEFT_FDF_MEAN,
            }
            right_sched_params = {
                "response_class_lower_bound": RIGHT_RESPONSE_CLASS_LOWER_BOUND,
                "response_class_upper_bound": RIGHT_RESPONSE_CLASS_UPPER_BOUND,
                "interval_mean": RIGHT_SCHEDS[i],
                "interval_type": "random",
                "fdf_mean": RIGHT_FDF_MEAN,
            }

            # creating the concurrent schedule runner for the current set of schedules
            sched_runner = schedule_runners.ConcurrentSchedRunner(
                left_sched_params, right_sched_params, ORGANISM_PARAMS
            )

            # looping for the number of generations
            for gen in range(20500):
                # updating the data dictionary
                data_dict["Rep"].append(rep)
                data_dict["Schedule"].append(i)
                data_dict["Gen"].append(gen)

                # running the concurrent schedules
                sched_runner.run()

                # updating the progress bars every 1000 generations
                if gen % 1000 == 0:
                    updates = [
                        gen_progress_bar.update(gen),
                        sched_progress_bar.update(i),
                        rep_progress_bar.update(rep),
                    ]

                    # printing the progress bars to the terminal
                    print("\n".join(updates))

            # getting the data from the schedule runner
            sched_data = sched_runner.return_data()

            # updating the data dictionary
            data_dict["Emissions"].extend(sched_data["Emissions"])
            data_dict["R1"].extend(sched_data["R1"])
            data_dict["B1"].extend(sched_data["B1"])
            data_dict["R2"].extend(sched_data["R2"])
            data_dict["B2"].extend(sched_data["B2"])

    # updating the progress bars when the loop is finished
    updates = [
        gen_progress_bar.update(20500),
        sched_progress_bar.update(len(LEFT_SCHEDS)),
        rep_progress_bar.update(REPS),
    ]
    # printing the progress bars to the terminal
    print("\n".join(updates))

    # outputting the data to a csv using pandas
    df = pd.DataFrame(data_dict)
    df.to_csv("data.csv", index=False)

    # printing the finised message to the terminal
    print("\U0001F40E Done Giddyuped! \U0001F40E")


# running the main function
if __name__ == "__main__":
    main()
