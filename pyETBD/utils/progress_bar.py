import sys


class ProgressBar:
    """Class used to create a progress bar in the terminal"""

    def __init__(self, total, prefix="", length=50, fill="█"):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.fill = fill

    def update(self, iteration):
        self.clear_terminal()
        percent = ("{:.1f}").format(100 * (iteration / float(self.total)))
        filled_length = int(self.length * iteration // self.total)
        bar = self.fill * filled_length + "#" * (self.length - filled_length)
        return f"{self.prefix} |{bar}| {percent}% Complete"

    def clear_terminal(self):
        sys.stdout.write("\033[H\033[J")
        sys.stdout.flush()
