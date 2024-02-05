import tkinter as tk
from tkinter import ttk
import json
from pyetbd import experiment_runner


class ExperimentGUIData:
    def __init__(self):
        self.experiments = []
        self.current_experiment = {}
        self.schedules = []
        self.defaults = {
            "file_stub": "example_experiment",
            "reps": 1,
            "mut_rate": 0.1,
            "gens": 20500,
            "pop_size": 100,
            "low_pheno": 0,
            "high_pheno": 1023,
            "fdf_type": "linear_fdf",
            "fitness_landscape": "circular_landscape",
            "recombination_method": "bitwise",
            "reinitialize_population": "True",
            "alt1_response_class_lower_bound": 471,
            "alt1_response_class_upper_bound": 512,
            "alt1_response_class_size": 41,
            "alt2_response_class_lower_bound": 512,
            "alt2_response_class_upper_bound": 553,
            "alt2_response_class_size": 41,
            "response_class_excluded_lower_bound": 0,
            "response_class_excluded_upper_bound": 0,
            "schedule_type": "random",
            "schedule_subtype": "interval",
            "mean": 20,
            "fdf_mean": 40,
        }
        self.defaults["alt1_mean(interval/ratio)"] = self.defaults["mean"]
        self.defaults["alt2_mean(interval/ratio)"] = self.defaults["mean"]
        self.defaults["alt1_schedule_type"] = self.defaults["schedule_type"]
        self.defaults["alt1_schedule_subtype"] = self.defaults["schedule_subtype"]
        self.defaults["alt2_schedule_type"] = self.defaults["schedule_type"]
        self.defaults["alt2_schedule_subtype"] = self.defaults["schedule_subtype"]
        self.defaults["alt1_response_class_excluded_lower_bound"] = self.defaults[
            "response_class_excluded_lower_bound"
        ]
        self.defaults["alt1_response_class_excluded_upper_bound"] = self.defaults[
            "response_class_excluded_upper_bound"
        ]
        self.defaults["alt2_response_class_excluded_lower_bound"] = self.defaults[
            "response_class_excluded_lower_bound"
        ]
        self.defaults["alt2_response_class_excluded_upper_bound"] = self.defaults[
            "response_class_excluded_upper_bound"
        ]
        self.defaults["alt1_fdf_mean"] = self.defaults["fdf_mean"]
        self.defaults["alt2_fdf_mean"] = self.defaults["fdf_mean"]

        self.experiment_setting_labels = [
            "file_stub",
            "reps",
            "mut_rate",
            "gens",
            "pop_size",
            "low_pheno",
            "high_pheno",
            "fdf_type",
            "fitness_landscape",
            "recombination_method",
            "reinitialize_population",
        ]

        self.schedule_setting_labels = [
            "alt1_mean(interval/ratio)",
            "alt2_mean(interval/ratio)",
            "alt1_fdf_mean",
            "alt2_fdf_mean",
            "alt1_schedule_type",
            "alt1_schedule_subtype",
            "alt2_schedule_type",
            "alt2_schedule_subtype",
            "alt1_response_class_lower_bound",
            "alt1_response_class_upper_bound",
            "alt1_response_class_size",
            "alt2_response_class_lower_bound",
            "alt2_response_class_upper_bound",
            "alt2_response_class_size",
            "alt1_response_class_excluded_lower_bound",
            "alt1_response_class_excluded_upper_bound",
            "alt2_response_class_excluded_lower_bound",
            "alt2_response_class_excluded_upper_bound",
        ]

    def format_data(self):
        formatted_experiments = []
        for experiment in self.experiments:
            formatted_experiments.append(self.format_experiment(experiment))

        return formatted_experiments

    def format_schedules(self, schedules):
        formatted_schedules = []
        for schedule in schedules:
            alt1_schedule = {}
            alt2_schedule = {}
            alt1_schedule["mean"] = int(schedule["alt1_mean(interval/ratio)"])
            alt1_schedule["fdf_mean"] = int(schedule["alt1_fdf_mean"])
            alt1_schedule["schedule_type"] = schedule["alt1_schedule_type"]
            alt1_schedule["schedule_subtype"] = schedule["alt1_schedule_subtype"]
            alt1_schedule["response_class_lower_bound"] = int(
                schedule["alt1_response_class_lower_bound"]
            )
            alt1_schedule["response_class_upper_bound"] = int(
                schedule["alt1_response_class_upper_bound"]
            )
            alt1_schedule["response_class_size"] = int(
                schedule["alt1_response_class_size"]
            )
            alt1_schedule["excluded_lower_bound"] = int(
                schedule["alt1_response_class_excluded_lower_bound"]
            )
            alt1_schedule["excluded_upper_bound"] = int(
                schedule["alt1_response_class_excluded_upper_bound"]
            )

            alt2_schedule["mean"] = int(schedule["alt2_mean(interval/ratio)"])
            alt2_schedule["fdf_mean"] = int(schedule["alt2_fdf_mean"])
            alt2_schedule["schedule_type"] = schedule["alt2_schedule_type"]
            alt2_schedule["schedule_subtype"] = schedule["alt2_schedule_subtype"]
            alt2_schedule["response_class_lower_bound"] = int(
                schedule["alt2_response_class_lower_bound"]
            )
            alt2_schedule["response_class_upper_bound"] = int(
                schedule["alt2_response_class_upper_bound"]
            )
            alt2_schedule["response_class_size"] = int(
                schedule["alt2_response_class_size"]
            )
            alt2_schedule["excluded_lower_bound"] = int(
                schedule["alt2_response_class_excluded_lower_bound"]
            )
            alt2_schedule["excluded_upper_bound"] = int(
                schedule["alt2_response_class_excluded_upper_bound"]
            )

            formatted_schedules.append([alt1_schedule, alt2_schedule])

        return formatted_schedules

    def format_experiment(self, experiment):
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

    def save(self, filename):
        output = {"experiments": self.format_data()}
        with open(f"{filename}.json", "w") as f:
            json.dump(output, f, indent=4)


class ExperimentGUI:
    def __init__(self):
        # Create the root window
        root = tk.Tk()
        self.master = root
        self.master.title("pyETBD")
        self.master.geometry("900x900")

        # Set up attributes
        self.data_obj = ExperimentGUIData()
        self.entry_dict = {}

        # Call methods
        self.create_widgets()

    def run(self):
        self.master.mainloop()

    # Widget Creation

    def create_widgets(self):
        # Create the notebook
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True)

        # Create the tabs
        self.create_experiment_tab()
        self.create_runner_tab()

    def create_experiment_tab(self):
        # Create the tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Experiment Builder")

        # Create the widgets
        self.create_schedule_experiment_frame(tab)
        self.create_schedule_tree(tab)

    def create_runner_tab(self):
        # Create the tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Experiment Runner")

        # Create the widgets
        self.create_runner_widgets(tab)

    def create_schedule_experiment_frame(self, tab):
        # Create the frame
        frame = ttk.Frame(tab)
        frame.pack(fill="both", expand=True)

        # Create the widgets
        self.create_experiment_widgets(frame)
        self.create_schedule_widgets(frame)

    def create_runner_widgets(self, tab):
        # Create a widget frame
        frame = ttk.Frame(tab)
        frame.pack()

        # Create the widgets
        runner_entry_label = ttk.Label(frame, text="Experiment File:")
        runner_entry_label.grid(row=0, column=0, sticky="e")
        self.runner_entry = ttk.Entry(frame)
        self.runner_entry.grid(row=0, column=1, sticky="w")

        # Create a button to run the experiments
        run_experiments_button = ttk.Button(
            frame, text="Run", command=self.run_experiments
        )
        run_experiments_button.grid(row=1, column=0, columnspan=2)

        # Create an info frame
        info_frame = ttk.Frame(tab)
        info_frame.pack()

        # Create a label for the info frame
        info_label = ttk.Label(
            info_frame,
            text="Info: Please enter the name of the experiment file to run. Be sure to include the '.json' extension.\nClick the 'Run' button to run the experiments.",
        )
        info_label.pack(fill="both", expand=True)

    def create_experiment_widgets(self, frame):
        # Create the widgets for the experiment settings
        for i, label in enumerate(self.data_obj.experiment_setting_labels):
            self.create_label_entry(
                frame,
                label.replace("_", " ").title(),
                self.data_obj.defaults[label],
                i,
                0,
            )

        row = len(self.data_obj.experiment_setting_labels)
        # Create a button to add an experiment
        self.add_experiment_button = ttk.Button(
            frame, text="Add Experiment", command=self.add_experiment
        )
        self.add_experiment_button.grid(row=row, column=0, columnspan=2)

        # Create an entry for the experiment file
        self.experiment_file_label = ttk.Label(frame, text="File Name:")
        self.experiment_file_label.grid(row=row + 1, column=0, sticky="e")
        self.experiment_file_entry = ttk.Entry(frame)
        self.experiment_file_entry.insert(0, "experiments")
        self.experiment_file_entry.grid(row=row + 1, column=1)

        # Create a listbox to display the experiments
        self.experiments_label = ttk.Label(frame, text="Experiments:")
        self.experiments_label.grid(row=row + 2, column=0, columnspan=2)

        self.experiments_listbox = tk.Listbox(frame)
        self.experiments_listbox.grid(
            row=row + 3, column=0, sticky="nsew", columnspan=2, rowspan=10
        )
        # Create a button to save the experiments
        self.save_experiments_button = ttk.Button(
            frame, text="Save Experiments", command=self.save_experiments
        )
        self.save_experiments_button.grid(row=row + 13, column=0, columnspan=2)

        # Create a button to clear the experiments
        self.clear_experiments_button = ttk.Button(
            frame, text="Clear Experiments", command=self.clear_experiments
        )
        self.clear_experiments_button.grid(row=row + 14, column=0, columnspan=2)

    def create_schedule_widgets(self, frame):
        # Create the widgets for the schedule settings
        for i, label in enumerate(self.data_obj.schedule_setting_labels):
            self.create_label_entry(
                frame,
                label.replace("_", " ").title(),
                self.data_obj.defaults[label],
                i,
                2,
            )

        row = len(self.data_obj.schedule_setting_labels)
        # Create a button to add a schedule
        add_schedule_button = ttk.Button(
            frame, text="Add Schedule", command=self.add_schedule
        )
        add_schedule_button.grid(row=row, column=2, columnspan=2)
        # Create a button to delete a schedule
        delete_schedule_button = ttk.Button(
            frame, text="Delete Schedule", command=self.delete_schedule
        )
        delete_schedule_button.grid(row=row + 1, column=2, columnspan=2)
        # Create a button to clear the schedules
        clear_schedules_button = ttk.Button(
            frame, text="Clear Schedules", command=self.clear_schedules
        )
        clear_schedules_button.grid(row=row + 2, column=2, columnspan=2)

    def create_schedule_tree(self, tab):
        # Create the frame
        frame = ttk.Frame(tab)
        frame.pack(fill="both", expand=True)

        # Create the tree
        tree = ttk.Treeview(
            frame,
            columns=[
                label.replace("_", " ").title()
                for label in self.data_obj.schedule_setting_labels
            ],
            show="headings",
        )
        # Set column headings
        for label in self.data_obj.schedule_setting_labels:
            tree.heading(
                label.replace("_", " ").title(), text=label.replace("_", " ").title()
            )
            tree.column(label.replace("_", " ").title(), width=200)

        # Add a vertical and horizontal scrollbar
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid the Treeview and scrollbar
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure the frame's grid to expand properly
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def create_label_entry(self, frame, label_text, entry_text, row, column):
        label = ttk.Label(frame, text=label_text)
        entry = ttk.Entry(frame)
        entry.insert(0, entry_text)
        label.grid(row=row, column=column, sticky="e")
        entry.grid(row=row, column=column + 1, sticky="w")

        self.entry_dict[label_text] = entry

    # Commands

    def add_schedule(self):
        # Get the values from the entry widgets
        schedule = {}
        for label in self.data_obj.schedule_setting_labels:
            schedule[label] = self.get_entry(label)

        # Add the schedule to the data object
        self.data_obj.schedules.append(schedule)

        # Add the schedule to the tree
        self.add_values_to_tree(
            self.get_tree(),
            [schedule[label] for label in self.data_obj.schedule_setting_labels],
        )

    def delete_schedule(self):
        # Get the tree
        tree = self.get_tree()

        # Delete the last row
        tree.delete(tree.get_children()[-1])

        # Delete the last schedule
        self.data_obj.schedules.pop()

    def clear_schedules(self):
        # Get the tree
        tree = self.get_tree()

        # Delete all rows
        for child in tree.get_children():
            tree.delete(child)

        # Delete all schedules
        self.data_obj.schedules = []

    def add_experiment(self):
        if len(self.data_obj.schedules) == 0:
            frame = tk.Toplevel(self.master)
            frame.title("Error")
            frame.geometry("200x100")
            label = ttk.Label(frame, text="No schedules provided")
            label.pack()

            return

        # Get the values from the entry widgets
        self.data_obj.current_experiment = {}
        for label in self.data_obj.experiment_setting_labels:
            self.data_obj.current_experiment[label] = self.get_entry(label)

        # Add the schedules to the current experiment
        self.data_obj.current_experiment["schedules"] = self.data_obj.schedules

        # Add the current experiment to the data object
        self.data_obj.experiments.append(self.data_obj.current_experiment)

        # Add the current experiment to the listbox
        self.experiments_listbox.insert(
            "end", self.data_obj.current_experiment["file_stub"]
        )

    def save_experiments(self):
        if len(self.data_obj.experiments) == 0:
            frame = tk.Toplevel(self.master)
            frame.title("Error")
            frame.geometry("200x100")
            label = ttk.Label(frame, text="No experiments provided")
            label.pack()

            return
        # Get the filename
        filename = self.experiment_file_entry.get()

        # Save the experiments
        self.data_obj.save(filename)

        # Let the user know the experiments were saved
        frame = tk.Toplevel(self.master)
        frame.title(f"Success")
        frame.geometry("400x100")
        label = ttk.Label(frame, text=f"{filename}.json saved in current directory")
        label.pack()

    def clear_experiments(self):
        # Clear the listbox
        self.experiments_listbox.delete(0, "end")

        # Clear the experiments
        self.data_obj.experiments = []

    def run_experiments(self):
        # Get the filename
        file_name = self.runner_entry.get()

        # Let the user know the experiments are running
        frame = tk.Toplevel(self.master)
        frame.title(f"Running")
        frame.geometry("400x100")
        label = ttk.Label(
            frame, text=f"Running {file_name}... See terminal for progress"
        )
        label.pack()
        self.master.update()

        # Run the experiments
        runner = experiment_runner.ExperimentRunner(file_name, "")
        runner.giddyup()

        # Let the user know the experiments are done
        frame.title("Success")
        label.config(text="\U0001F434 Done Giddyupped! \U0001F434")

    # Helpers

    def add_values_to_tree(self, tree, values):
        tree.insert("", "end", values=values)

    def get_entry(self, label):
        return self.entry_dict[label.replace("_", " ").title()].get()

    def get_tree(self) -> ttk.Treeview:  # type: ignore
        for child in self.master.winfo_children():
            if isinstance(child, ttk.Notebook):
                for tab in child.winfo_children():
                    for frame in tab.winfo_children():
                        for tree in frame.winfo_children():
                            if isinstance(tree, ttk.Treeview):
                                return tree
