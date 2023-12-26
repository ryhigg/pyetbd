from pyETBD.json_writer import ExperimentGUI
import tkinter as tk


# define the main function
def main():
    root = tk.Tk()
    gui = ExperimentGUI(root)
    root.mainloop()


# call the main function
if __name__ == "__main__":
    main()
