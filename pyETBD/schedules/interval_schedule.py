class IntervalSchedule:
    def __init__(
        self,
        response_class_lower_bound,
        response_class_upper_bound,
        interval_mean,
        interval_func,
        fdf_mean,
    ):
        """Initializes the IntervalSchedule class.

        Args:
            response_class_lower_bound (int): lower bound of the response class
            response_class_upper_bound (int: upper bound of the response class
            interval_mean (int): the mean of the interval schedule
            interval_func (func): the function that generates the intervals
            fdf (func): the function that samples from the FDF
            fdf_args (tuple): arguments for the FDF function
        """
        self.response_class_lower_bound = response_class_lower_bound
        self.response_class_upper_bound = response_class_upper_bound
        self.interval_mean = interval_mean
        self.interval_func = interval_func
        self.fdf_mean = fdf_mean

        self.set_up()

    def set_up(self):
        """Sets up the interval schedule."""

        self.interval = self.interval_func(self.interval_mean)

        # used to keep track of whether reinforcement is available
        self.counter = 0

    def check_response_class(self, emitted):
        """Checks if the emitted value is in the response class.

        Args:
            emitted (int): the emitted behavior (phenotype)

        Returns:
            bool: True if the emitted value is in the response class, False otherwise
        """

        return (
            self.response_class_lower_bound
            <= emitted
            <= self.response_class_upper_bound
        )

    def check_reinforcement(self):
        """Checks if reinforcement is available and resets the counter and generates a new interval if it is.

        Returns:
            bool: True if reinforcement is available, False otherwise
        """

        if self.counter >= self.interval:
            self.counter = 0
            self.interval = self.interval_func(self.interval_mean)
            return True

        return False
