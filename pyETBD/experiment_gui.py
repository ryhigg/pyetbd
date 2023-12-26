import tkinter as tk
from tkinter import ttk
import json
from pyETBD import experiment_handler


class ExperimentGUI:
    """Opens a tkinter window that allows the user to build an experiment."""

    def __init__(self, master):
        self.master = master
        self.master.title("pyETBD Experiment Writer")
        self.master.geometry("800x500")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.experiments = []
        self.create_widgets()

        self.experiment_defaults = {
            "file_stub": "example_experiment",
            "reps": 1,
            "mut_rate": 0.1,
            "gens": 20500,
            "pop_size": 100,
            "low_pheno": 0,
            "high_pheno": 1023,
            "fdf_type": "linear",
            "fitness_landscape": "circular",
            "recombination_method": "bitwise",
            "reinitialize_population": "True",
        }

    def create_widgets(self):
        self.master_frame = ttk.Frame(self.master)
        self.master_frame.pack(padx=10, pady=10)

        self.enter_experiment_params_button = ttk.Button(
            self.master_frame,
            text="Enter Experiment Settings",
            command=self.enter_experiment_settings,
        )
        self.enter_experiment_params_button.grid(row=0, column=0, padx=10, pady=10)

        self.save_experiments_button = ttk.Button(
            self.master_frame, text="Save Experiments", command=self.save_experiments
        )
        self.save_experiments_button.grid(row=0, column=1, padx=10, pady=10)

        self.launch_experiment_runner_button = ttk.Button(
            self.master_frame,
            text="Launch Experiment Runner",
            command=self.launch_experiment_runner,
        )
        self.launch_experiment_runner_button.grid(row=0, column=2, padx=10, pady=10)

    def launch_experiment_runner(self):
        self.runner_frame = tk.Toplevel(self.master)
        self.runner_frame.title("Experiment Runner")

        self.experiment_file_label = ttk.Label(
            self.runner_frame, text="Experiment File:"
        )
        self.experiment_file_label.grid(row=0, column=0, sticky=tk.E)

        self.experiment_file_entry = ttk.Entry(self.runner_frame)
        self.experiment_file_entry.grid(row=0, column=1)
        self.experiment_file_entry.insert(0, "experiments.json")

        self.run_experiment_button = ttk.Button(
            self.runner_frame, text="Run Experiment", command=self.run_experiment
        )
        self.run_experiment_button.grid(row=1, column=0, columnspan=2)

    def run_experiment(self):
        experiment_file = self.experiment_file_entry.get()
        runner = experiment_handler.ExperimentHandler(experiment_file, "")
        progress_label = ttk.Label(self.runner_frame, text="Running Experiment...")
        progress_label.grid(row=2, column=0, columnspan=2)
        runner.giddyup()
        progress_label.config(text="Done Giddyupped!")

    def save_experiments(self):
        experiments = {"experiments": self.experiments}
        with open("experiments.json", "w") as outfile:
            json.dump(experiments, outfile, indent=4)

        # add a label to the master frame that says "experiments saved"
        self.experiments_saved_label = ttk.Label(
            self.master_frame, text="Experiments Saved!"
        )
        self.experiments_saved_label.grid(row=1, column=0, columnspan=3)

    def enter_experiment_settings(self):
        self.exp_frame = tk.Toplevel(self.master)
        self.exp_frame.title("Experiment Settings")

        row = 0
        for key, default_value in self.experiment_defaults.items():
            ttk.Label(
                self.exp_frame, text=f"{key.replace('_', ' ').capitalize()}:"
            ).grid(row=row, column=0, sticky=tk.E)
            entry = ttk.Entry(self.exp_frame)
            entry.insert(0, default_value)
            entry.grid(row=row, column=1)
            self.experiment_defaults[key] = entry
            row += 1

        self.schedule_settings_button = ttk.Button(
            self.exp_frame,
            text="Enter Schedule Data",
            command=self.enter_schedule_settings,
        )
        self.schedule_settings_button.grid(row=row, column=0)
        self.save_experiment_button = ttk.Button(
            self.exp_frame, text="Save Experiment", command=self.save_experiment
        )
        self.save_experiment_button.grid(row=row, column=1)

    def save_experiment(self):
        self.current_experiment = self.format_experiment_settings(
            self.current_experiment
        )
        self.experiments.append(self.current_experiment)
        self.experiment_label = ttk.Label(
            self.master, text=self.current_experiment["file_stub"]
        )
        self.experiment_label.pack()

    def format_experiment_settings(self, experiment):
        formatted_experiment = {}
        for key, value in experiment.items():
            if key == "reps":
                formatted_experiment["reps"] = int(value)
            elif key == "mut_rate":
                formatted_experiment["mut_rate"] = float(value)
            elif key == "gens":
                formatted_experiment["gens"] = int(value)
            elif key == "pop_size":
                formatted_experiment["pop_size"] = int(value)
            elif key == "low_pheno":
                formatted_experiment["low_pheno"] = int(value)
            elif key == "high_pheno":
                formatted_experiment["high_pheno"] = int(value)
            elif key == "fdf_type":
                formatted_experiment["fdf_type"] = value
            elif key == "fitness_landscape":
                formatted_experiment["fitness_landscape"] = value
            elif key == "recombination_method":
                formatted_experiment["recombination_method"] = value
            elif key == "reinitialize_population":
                if value == "True":
                    formatted_experiment["reinitialize_population"] = True
                elif value == "False":
                    formatted_experiment["reinitialize_population"] = False
                else:
                    raise ValueError(
                        "reinitialize_population must be either True or False"
                    )
            elif key == "schedules":
                formatted_experiment["schedules"] = self.format_schedules(value)
            else:
                formatted_experiment[key] = value

        return formatted_experiment

    def format_schedules(self, schedules):
        formatted_schedules = []
        for schedule_pair in schedules:
            formatted_schedule_pair = []
            for schedule in schedule_pair:
                formatted_schedule = {}
                for key, value in schedule.items():
                    if key == "fdf_mean":
                        formatted_schedule["fdf_mean"] = int(value)
                    elif key == "response_class_lower_bound":
                        formatted_schedule["response_class_lower_bound"] = int(value)
                    elif key == "response_class_upper_bound":
                        formatted_schedule["response_class_upper_bound"] = int(value)
                    elif key == "response_class_size":
                        formatted_schedule["response_class_size"] = int(value)
                    elif key == "schedule_type":
                        formatted_schedule["schedule_type"] = value
                    elif key == "schedule_subtype":
                        formatted_schedule["schedule_subtype"] = value
                    elif key == "mean":
                        formatted_schedule["mean"] = int(value)
                    elif key == "excluded_lower_bound":
                        formatted_schedule["excluded_lower_bound"] = int(value)
                    elif key == "excluded_upper_bound":
                        formatted_schedule["excluded_upper_bound"] = int(value)
                formatted_schedule_pair.append(formatted_schedule)
            formatted_schedules.append(formatted_schedule_pair)

        return formatted_schedules

    def enter_schedule_settings(self):
        self.schedule_frame = tk.Toplevel(self.exp_frame)
        self.schedule_frame.title("Schedule Settings")
        self.create_schedule_display(self.schedule_frame)
        self.current_experiment = self.get_experiment_settings()

        # first alt response class lower bound
        self.first_alt_response_class_lower_bound_label = ttk.Label(
            self.schedule_frame, text="First Alternative Response Class Lower Bound:"
        )
        self.first_alt_response_class_lower_bound_label.grid(
            row=0, column=0, sticky=tk.E
        )
        self.first_alt_response_class_lower_bound_entry = ttk.Entry(self.schedule_frame)
        self.first_alt_response_class_lower_bound_entry.grid(row=0, column=1)
        self.first_alt_response_class_lower_bound_entry.insert(0, "471")

        # first alt response class upper bound
        self.first_alt_response_class_upper_bound_label = ttk.Label(
            self.schedule_frame, text="First Alternative Response Class Upper Bound:"
        )
        self.first_alt_response_class_upper_bound_label.grid(
            row=1, column=0, sticky=tk.E
        )
        self.first_alt_response_class_upper_bound_entry = ttk.Entry(self.schedule_frame)
        self.first_alt_response_class_upper_bound_entry.grid(row=1, column=1)
        self.first_alt_response_class_upper_bound_entry.insert(0, "512")

        # first alt response class size
        self.first_alt_response_class_size_label = ttk.Label(
            self.schedule_frame, text="First Alternative Response Class Size:"
        )
        self.first_alt_response_class_size_label.grid(row=2, column=0, sticky=tk.E)
        self.first_alt_response_class_size_entry = ttk.Entry(self.schedule_frame)
        self.first_alt_response_class_size_entry.grid(row=2, column=1)
        self.first_alt_response_class_size_entry.insert(0, "41")

        # First Alternative FDF
        self.first_alt_fdf_label = ttk.Label(
            self.schedule_frame, text="First Alternative FDF:"
        )
        self.first_alt_fdf_label.grid(row=3, column=0, sticky=tk.E)
        self.first_alt_fdf_entry = ttk.Entry(self.schedule_frame)
        self.first_alt_fdf_entry.grid(row=3, column=1)
        self.first_alt_fdf_entry.insert(0, "40")

        # First alt schedule type
        self.schedule_type_label = ttk.Label(self.schedule_frame, text="Schedule Type:")
        self.schedule_type_label.grid(row=4, column=0, sticky=tk.E)
        self.schedule_type_entry = ttk.Entry(self.schedule_frame)
        self.schedule_type_entry.grid(row=4, column=1)
        self.schedule_type_entry.insert(0, "random")

        # First alt schedule subtype
        self.schedule_subtype_label = ttk.Label(
            self.schedule_frame, text="Schedule Subtype:"
        )
        self.schedule_subtype_label.grid(row=5, column=0, sticky=tk.E)
        self.schedule_subtype_entry = ttk.Entry(self.schedule_frame)
        self.schedule_subtype_entry.grid(row=5, column=1)
        self.schedule_subtype_entry.insert(0, "interval")

        # First alt mean
        self.mean_label = ttk.Label(
            self.schedule_frame, text="Mean (interval or ratio):"
        )
        self.mean_label.grid(row=6, column=0, sticky=tk.E)
        self.mean_entry = ttk.Entry(self.schedule_frame)
        self.mean_entry.grid(row=6, column=1)

        # first alt excluded lower bound
        self.first_alt_excluded_lower_bound_label = ttk.Label(
            self.schedule_frame, text="First Alternative Excluded Lower Bound:"
        )
        self.first_alt_excluded_lower_bound_label.grid(row=7, column=0, sticky=tk.E)
        self.first_alt_excluded_lower_bound_entry = ttk.Entry(self.schedule_frame)
        self.first_alt_excluded_lower_bound_entry.grid(row=7, column=1)
        self.first_alt_excluded_lower_bound_entry.insert(0, "0")

        # first alt excluded upper bound
        self.first_alt_excluded_upper_bound_label = ttk.Label(
            self.schedule_frame, text="First Alternative Excluded Upper Bound:"
        )
        self.first_alt_excluded_upper_bound_label.grid(row=8, column=0, sticky=tk.E)
        self.first_alt_excluded_upper_bound_entry = ttk.Entry(self.schedule_frame)
        self.first_alt_excluded_upper_bound_entry.grid(row=8, column=1)
        self.first_alt_excluded_upper_bound_entry.insert(0, "0")

        # second alt response class lower bound
        self.second_alt_response_class_lower_bound_label = ttk.Label(
            self.schedule_frame, text="Second Alternative Response Class Lower Bound:"
        )
        self.second_alt_response_class_lower_bound_label.grid(
            row=0, column=2, sticky=tk.E
        )
        self.second_alt_response_class_lower_bound_entry = ttk.Entry(
            self.schedule_frame
        )
        self.second_alt_response_class_lower_bound_entry.grid(row=0, column=3)
        self.second_alt_response_class_lower_bound_entry.insert(0, "512")

        # second alt response class upper bound
        self.second_alt_response_class_upper_bound_label = ttk.Label(
            self.schedule_frame, text="Second Alternative Response Class Upper Bound:"
        )
        self.second_alt_response_class_upper_bound_label.grid(
            row=1, column=2, sticky=tk.E
        )
        self.second_alt_response_class_upper_bound_entry = ttk.Entry(
            self.schedule_frame
        )
        self.second_alt_response_class_upper_bound_entry.grid(row=1, column=3)
        self.second_alt_response_class_upper_bound_entry.insert(0, "553")

        # second alt response class size
        self.second_alt_response_class_size_label = ttk.Label(
            self.schedule_frame, text="Second Alternative Response Class Size:"
        )
        self.second_alt_response_class_size_label.grid(row=2, column=2, sticky=tk.E)
        self.second_alt_response_class_size_entry = ttk.Entry(self.schedule_frame)
        self.second_alt_response_class_size_entry.grid(row=2, column=3)
        self.second_alt_response_class_size_entry.insert(0, "41")

        # second alt fdf
        self.second_alt_fdf_label = ttk.Label(
            self.schedule_frame, text="Second Alternative FDF:"
        )
        self.second_alt_fdf_label.grid(row=3, column=2, sticky=tk.E)
        self.second_alt_fdf_entry = ttk.Entry(self.schedule_frame)
        self.second_alt_fdf_entry.grid(row=3, column=3)
        self.second_alt_fdf_entry.insert(0, "40")

        # second alt schedule type
        self.second_schedule_type_label = ttk.Label(
            self.schedule_frame, text="Schedule Type:"
        )
        self.second_schedule_type_label.grid(row=4, column=2, sticky=tk.E)
        self.second_schedule_type_entry = ttk.Entry(self.schedule_frame)
        self.second_schedule_type_entry.grid(row=4, column=3)
        self.second_schedule_type_entry.insert(0, "random")

        # second alt schedule subtype
        self.second_schedule_subtype_label = ttk.Label(
            self.schedule_frame, text="Schedule Subtype:"
        )
        self.second_schedule_subtype_label.grid(row=5, column=2, sticky=tk.E)
        self.second_schedule_subtype_entry = ttk.Entry(self.schedule_frame)
        self.second_schedule_subtype_entry.grid(row=5, column=3)
        self.second_schedule_subtype_entry.insert(0, "interval")

        # second alt mean
        self.second_mean_label = ttk.Label(
            self.schedule_frame, text="Mean (interval or ratio):"
        )
        self.second_mean_label.grid(row=6, column=2, sticky=tk.E)
        self.second_mean_entry = ttk.Entry(self.schedule_frame)
        self.second_mean_entry.grid(row=6, column=3)

        # second alt excluded lower bound
        self.second_alt_excluded_lower_bound_label = ttk.Label(
            self.schedule_frame, text="Second Alternative Excluded Lower Bound:"
        )
        self.second_alt_excluded_lower_bound_label.grid(row=7, column=2, sticky=tk.E)
        self.second_alt_excluded_lower_bound_entry = ttk.Entry(self.schedule_frame)
        self.second_alt_excluded_lower_bound_entry.grid(row=7, column=3)
        self.second_alt_excluded_lower_bound_entry.insert(0, "0")

        # second alt excluded upper bound
        self.second_alt_excluded_upper_bound_label = ttk.Label(
            self.schedule_frame, text="Second Alternative Excluded Upper Bound:"
        )
        self.second_alt_excluded_upper_bound_label.grid(row=8, column=2, sticky=tk.E)
        self.second_alt_excluded_upper_bound_entry = ttk.Entry(self.schedule_frame)
        self.second_alt_excluded_upper_bound_entry.grid(row=8, column=3)
        self.second_alt_excluded_upper_bound_entry.insert(0, "0")

        # Add schedule button
        self.add_schedule_button = ttk.Button(
            self.schedule_frame, text="Add Schedule", command=self.add_schedule
        )
        self.add_schedule_button.grid(row=9, column=0, columnspan=2)
        self.delete_schedule_button = ttk.Button(
            self.schedule_frame, text="Delete Schedule", command=self.delete_schedule
        )
        self.delete_schedule_button.grid(row=9, column=2, columnspan=2)

        # Done button
        self.done_button = ttk.Button(
            self.schedule_frame, text="Done", command=self.schedule_frame.destroy
        )
        self.done_button.grid(row=10, column=0, columnspan=4)

    def add_schedule(self):
        current_row = self.schedule_display.grid_size()[1]
        # get first alt data
        first_alt_fdf = self.first_alt_fdf_entry.get()
        first_alt_schedule_type = self.schedule_type_entry.get()
        first_alt_schedule_subtype = self.schedule_subtype_entry.get()
        first_alt_mean = self.mean_entry.get()
        first_alt_response_class_lower_bound = (
            self.first_alt_response_class_lower_bound_entry.get()
        )

        first_alt_response_class_upper_bound = (
            self.first_alt_response_class_upper_bound_entry.get()
        )

        first_alt_response_class_size = self.first_alt_response_class_size_entry.get()
        first_alt_excluded_lower_bound = self.first_alt_excluded_lower_bound_entry.get()
        first_alt_excluded_upper_bound = self.first_alt_excluded_upper_bound_entry.get()

        # get second alt data
        second_alt_fdf = self.second_alt_fdf_entry.get()
        second_alt_schedule_type = self.second_schedule_type_entry.get()
        second_alt_schedule_subtype = self.second_schedule_subtype_entry.get()
        second_alt_mean = self.second_mean_entry.get()
        second_alt_response_class_lower_bound = (
            self.second_alt_response_class_lower_bound_entry.get()
        )
        second_alt_response_class_upper_bound = (
            self.second_alt_response_class_upper_bound_entry.get()
        )
        second_alt_response_class_size = self.second_alt_response_class_size_entry.get()
        second_alt_excluded_lower_bound = (
            self.second_alt_excluded_lower_bound_entry.get()
        )

        second_alt_excluded_upper_bound = (
            self.second_alt_excluded_upper_bound_entry.get()
        )

        # add data to schedule display
        self.first_alt_label = ttk.Label(self.schedule_display, text=first_alt_mean)
        self.first_alt_label.grid(row=current_row, column=0)
        self.second_alt_label = ttk.Label(self.schedule_display, text=second_alt_mean)
        self.second_alt_label.grid(row=current_row, column=1)
        self.first_alt_fdf_label = ttk.Label(self.schedule_display, text=first_alt_fdf)
        self.first_alt_fdf_label.grid(row=current_row, column=2)
        self.second_alt_fdf_label = ttk.Label(
            self.schedule_display, text=second_alt_fdf
        )
        self.second_alt_fdf_label.grid(row=current_row, column=3)
        self.first_alt_schedule_type_label = ttk.Label(
            self.schedule_display, text=first_alt_schedule_type
        )
        self.first_alt_schedule_type_label.grid(row=current_row, column=4)
        self.second_alt_schedule_type_label = ttk.Label(
            self.schedule_display, text=second_alt_schedule_type
        )
        self.second_alt_schedule_type_label.grid(row=current_row, column=5)
        self.first_alt_schedule_subtype_label = ttk.Label(
            self.schedule_display, text=first_alt_schedule_subtype
        )
        self.first_alt_schedule_subtype_label.grid(row=current_row, column=6)
        self.second_alt_schedule_subtype_label = ttk.Label(
            self.schedule_display, text=second_alt_schedule_subtype
        )
        self.second_alt_schedule_subtype_label.grid(row=current_row, column=7)
        self.first_alt_resp_class_info_label = ttk.Label(
            self.schedule_display,
            text=f"{first_alt_response_class_lower_bound}-{first_alt_response_class_upper_bound} ({first_alt_response_class_size})",
        )
        self.first_alt_resp_class_info_label.grid(row=current_row, column=8)
        self.second_alt_resp_class_info_label = ttk.Label(
            self.schedule_display,
            text=f"{second_alt_response_class_lower_bound}-{second_alt_response_class_upper_bound} ({second_alt_response_class_size})",
        )
        self.second_alt_resp_class_info_label.grid(row=current_row, column=9)

        self.first_alt_excluded_bounds_label = ttk.Label(
            self.schedule_display,
            text=f"{first_alt_excluded_lower_bound}-{first_alt_excluded_upper_bound}",
        )
        self.first_alt_excluded_bounds_label.grid(row=current_row, column=10)
        self.second_alt_excluded_bounds_label = ttk.Label(
            self.schedule_display,
            text=f"{second_alt_excluded_lower_bound}-{second_alt_excluded_upper_bound}",
        )
        self.second_alt_excluded_bounds_label.grid(row=current_row, column=11)

        # add data to current experiment
        self.current_experiment["schedules"].append(self.get_schedule_settings())

    def delete_schedule(self):
        current_row = self.schedule_display.grid_size()[1]
        num_cols = self.schedule_display.grid_size()[0]
        # delete all columns on the current row
        for column in range(num_cols):
            self.schedule_display.grid_slaves(row=current_row - 1, column=column)[
                0
            ].destroy()

        # delete the most recent item in the current experiment schedules list
        self.current_experiment["schedules"].pop()

    def create_schedule_display(self, parent_frame):
        self.schedule_display = tk.Toplevel(parent_frame)
        self.schedule_display.title("Schedule Display")

        self.first_alt_label = ttk.Label(
            self.schedule_display, text="|1st Alt\nInterval/Ratio|"
        )
        self.first_alt_label.grid(row=0, column=0)
        self.second_alt_label = ttk.Label(
            self.schedule_display, text="|2nd Alt\nInterval/Ratio|"
        )
        self.second_alt_label.grid(row=0, column=1)

        self.first_alt_fdf_label = ttk.Label(
            self.schedule_display, text="|1st\nAlt FDF|"
        )
        self.first_alt_fdf_label.grid(row=0, column=2)
        self.second_alt_fdf_label = ttk.Label(
            self.schedule_display, text="|2nd\nAlt FDF|"
        )
        self.second_alt_fdf_label.grid(row=0, column=3)

        self.first_alt_schedule_type_label = ttk.Label(
            self.schedule_display, text="|1st Alt\nSched Type|"
        )
        self.first_alt_schedule_type_label.grid(row=0, column=4)
        self.second_alt_schedule_type_label = ttk.Label(
            self.schedule_display, text="|2nd Alt\nSched Type|"
        )
        self.second_alt_schedule_type_label.grid(row=0, column=5)

        self.first_alt_schedule_subtype_label = ttk.Label(
            self.schedule_display, text="|1st Alt\nSched Subtype|"
        )
        self.first_alt_schedule_subtype_label.grid(row=0, column=6)
        self.second_alt_schedule_subtype_label = ttk.Label(
            self.schedule_display, text="|2nd Alt\nSched Subtype|"
        )
        self.second_alt_schedule_subtype_label.grid(row=0, column=7)

        self.first_alt_resp_class_info_label = ttk.Label(
            self.schedule_display, text="|1st Alt\nResp Class|"
        )
        self.first_alt_resp_class_info_label.grid(row=0, column=8)
        self.second_alt_resp_class_info_label = ttk.Label(
            self.schedule_display, text="|2nd Alt\nResp Class|"
        )
        self.second_alt_resp_class_info_label.grid(row=0, column=9)

        self.first_alt_excluded_lower_bound_label = ttk.Label(
            self.schedule_display, text="|1st Alt\nExcl. Bounds|"
        )
        self.first_alt_excluded_lower_bound_label.grid(row=0, column=10)
        self.second_alt_excluded_lower_bound_label = ttk.Label(
            self.schedule_display, text="|2nd Alt\nExcl. Bounds|"
        )
        self.second_alt_excluded_lower_bound_label.grid(row=0, column=11)

    def get_experiment_settings(self):
        experiment_settings = {}
        for key, entry in self.experiment_defaults.items():
            experiment_settings[key] = entry.get()

        experiment_settings["schedules"] = []

        return experiment_settings

    def get_schedule_settings(self):
        schedule_settings = []
        first_alt_settings = {}
        second_alt_settings = {}

        first_alt_settings["fdf_mean"] = self.first_alt_fdf_entry.get()
        first_alt_settings[
            "response_class_lower_bound"
        ] = self.first_alt_response_class_lower_bound_entry.get()
        first_alt_settings[
            "response_class_upper_bound"
        ] = self.first_alt_response_class_upper_bound_entry.get()
        first_alt_settings[
            "response_class_size"
        ] = self.first_alt_response_class_size_entry.get()
        first_alt_settings["schedule_type"] = self.schedule_type_entry.get()
        first_alt_settings["schedule_subtype"] = self.schedule_subtype_entry.get()
        first_alt_settings["mean"] = self.mean_entry.get()
        first_alt_settings[
            "excluded_lower_bound"
        ] = self.first_alt_excluded_lower_bound_entry.get()
        first_alt_settings[
            "excluded_upper_bound"
        ] = self.first_alt_excluded_upper_bound_entry.get()

        second_alt_settings["fdf_mean"] = self.second_alt_fdf_entry.get()
        second_alt_settings[
            "response_class_lower_bound"
        ] = self.second_alt_response_class_lower_bound_entry.get()
        second_alt_settings[
            "response_class_upper_bound"
        ] = self.second_alt_response_class_upper_bound_entry.get()
        second_alt_settings[
            "response_class_size"
        ] = self.second_alt_response_class_size_entry.get()
        second_alt_settings["schedule_type"] = self.second_schedule_type_entry.get()
        second_alt_settings[
            "schedule_subtype"
        ] = self.second_schedule_subtype_entry.get()
        second_alt_settings["mean"] = self.second_mean_entry.get()
        second_alt_settings[
            "excluded_lower_bound"
        ] = self.second_alt_excluded_lower_bound_entry.get()
        second_alt_settings[
            "excluded_upper_bound"
        ] = self.second_alt_excluded_upper_bound_entry.get()

        schedule_settings.append(first_alt_settings)
        schedule_settings.append(second_alt_settings)

        return schedule_settings
