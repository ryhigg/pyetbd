import tkinter as tk
from tkinter import ttk


class DarkModeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Dark Mode App")

        # Configure a custom style for dark mode
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use the "clam" theme as a base
        self.style.configure(
            "Treeview",
            background="#2E2E2E",
            foreground="#FFFFFF",
            fieldbackground="#2E2E2E",
        )
        self.style.map("Treeview", background=[("selected", "#007ACC")])

        self.tree = ttk.Treeview(self.master, style="Treeview")
        self.tree["columns"] = (
            "Column1",
            "Column2",
            "Column3",
        )  # Customize columns as needed

        # Define column headings
        self.tree.heading("#0", text="Row")
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)

        self.tree.column("#0", width=50)  # Width of the row number column
        for column in self.tree["columns"]:
            self.tree.column(column, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill=tk.BOTH)

        self.add_data_button = ttk.Button(
            self.master, text="Add Data", command=self.add_data
        )
        self.add_data_button.pack(pady=10)

    def add_data(self):
        # Example: Insert a new row with data
        row_values = ("Data1", "Data2", "Data3")  # Replace with your data
        self.tree.insert("", "end", values=row_values)


def main():
    root = tk.Tk()
    app = DarkModeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
