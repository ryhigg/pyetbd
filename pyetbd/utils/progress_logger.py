import sys


class ProgressLogger:
    def __init__(self, exp_name: str):
        self.exp_name = exp_name

    def _clear_terminal(self):
        sys.stdout.write("\033[H\033[J")
        sys.stdout.flush()

    def create_progress_bars(self, reps: int, schs: int, gens: int):
        self.rep_pb = ProgressBar(reps, prefix="Rep", length=50)
        self.sch_pb = ProgressBar(schs, prefix="Sch", length=50)
        self.gen_pb = ProgressBar(gens, prefix="Gen", length=50)

    def log_progress(self, rep: int, sch: int, gen: int, end: str = "\r"):
        self._clear_terminal()
        exp_str = f"Exp: {self.exp_name}"
        rep_str = self.rep_pb.update(rep)
        sch_str = self.sch_pb.update(sch)
        gen_str = self.gen_pb.update(gen)
        print(f"{exp_str}\n{rep_str}\n{sch_str}\n{gen_str}\n", end=end)


class ProgressBar:
    """Class used to create a progress bar in the terminal"""

    def __init__(self, total, prefix="", length=50, fill="█"):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.fill = fill

    def update(self, iteration):
        percent = ("{:.1f}").format(100 * (iteration / float(self.total)))
        filled_length = int(self.length * iteration // self.total)
        bar = self.fill * filled_length + "#" * (self.length - filled_length)
        return f"{self.prefix} |{bar}| {percent}% Complete"
