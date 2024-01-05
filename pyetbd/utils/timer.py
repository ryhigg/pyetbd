import time


def timer(func):
    """A decorator that times a function.

    Args:
        func (function): a function to be timed

    """

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        total_time = end - start
        print(r"Time elapsed: %.3f" % (total_time))
        return result

    return wrapper
