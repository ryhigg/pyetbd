from pyETBD import experiments, organisms, schedules

# create the organism
organism = organisms.AnOrganism(
    pop_size=100,
    mut_rate=0.5,
    low_pheno=0,
    high_pheno=1023,
    fdf_type="linear",
    fitness_landscape="circular",
    recombination_method="bitwise",
)

# create the schedules
left_intervals = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
right_intervals = [120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20]

input_schedules = []

for i in range(len(left_intervals)):
    input_schedules.append(
        [
            schedules.IntervalSchedule(
                interval=left_intervals[i],
                fdf_mean=20,
                fdf_type="linear",
                type="random",
                response_class_lower_bound=471,
                response_class_upper_bound=512,
                response_class_size=41,
            ),
            schedules.IntervalSchedule(
                interval=right_intervals[i],
                fdf_mean=20,
                fdf_type="linear",
                type="random",
                response_class_lower_bound=512,
                response_class_upper_bound=553,
                response_class_size=41,
            ),
        ]
    )

# create the experiment

experiment = experiments.Experiment(input_schedules, 10, 20500, True, organism, "test")


def main():
    experiment.run()
    experiment.output_data()
    print("done giddyupped!")


if __name__ == "__main__":
    main()
