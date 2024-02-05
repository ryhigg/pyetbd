from pyetbd.settings_classes import ExperimentSettings
import pandas as pd


class DataSaver:
    def __init__(self, exp_settings: ExperimentSettings, output_dir: str):
        self.settings = exp_settings
        self.data_output = {
            "Rep": [],
            "Sch": [],
            "Gen": [],
            "Emissions": [],
        }
        self.output_dir = output_dir

    def _format_data(self) -> pd.DataFrame:
        """Formats data_output into 500 generation bins.

        Returns:
            pd.DataFrame: The formatted data output.
        """
        df = pd.DataFrame(self.data_output)

        df["bin"] = df.index // 500

        formatted_df = df.groupby(["Rep", "Sch", "bin"]).sum().reset_index()

        formatted_df.drop(columns=["Gen", "Emissions", "bin"], inplace=True)

        return formatted_df

    def _format_experiment_settings(self) -> pd.DataFrame:
        """
        Formats the experiment settings into a pandas DataFrame.

        Returns:
            pd.DataFrame: The formatted experiment settings DataFrame.
        """

        schedule_dicts = []
        arrangement_index = []
        index_in_arrangement = []
        for i, arrangement in enumerate(self.settings.schedules):
            for j, schedule in enumerate(arrangement):
                schedule_dicts.append(schedule)
                arrangement_index.append(i)
                index_in_arrangement.append(j)

        exp_dict = self.settings.__dict__.copy()
        exp_dict.pop("schedules")

        exp_df = pd.DataFrame([exp_dict])

        exp_df["schedule_arrangement"] = "exp"
        exp_df["schedule_index_in_arrangement"] = "exp"

        schedule_df = pd.DataFrame(schedule_dicts)
        schedule_df["schedule_arrangement"] = arrangement_index
        schedule_df["schedule_index_in_arrangement"] = index_in_arrangement

        formatted_df = pd.concat([exp_df, schedule_df], axis=0)

        return formatted_df

    def add_schedule_outputs(self, num_schedules: int) -> None:
        """
        Adds empty lists for each schedule output.

        Args:
            num_schedules (int): The number of schedules.

        Returns:
            None
        """
        for i in range(num_schedules):
            self.data_output[f"B{i+1}"] = []
            self.data_output[f"R{i+1}"] = []
            self.data_output[f"P{i+1}"] = []

    def save_data(self) -> None:
        """
        Save the data to a CSV file and an Excel file.

        This method saves the data stored in `self.data_output` to a CSV file
        and an Excel file. The CSV file is saved with the file stub specified
        in `self.settings.file_stub`, while the Excel file is saved with the
        same file stub but with the extension '.xlsx'. The data is saved in
        two sheets in the Excel file: 'Data' and 'Settings'.
        """
        df = pd.DataFrame(self.data_output)
        df.to_csv(f"{self.output_dir}{self.settings.file_stub}.csv")

        with pd.ExcelWriter(
            f"{self.output_dir}{self.settings.file_stub}.xlsx"
        ) as writer:
            self._format_data().to_excel(writer, sheet_name="Data", index=False)
            self._format_experiment_settings().to_excel(
                writer, sheet_name="Settings", index=False
            )
