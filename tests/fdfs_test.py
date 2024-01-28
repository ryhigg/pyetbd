from pyetbd.rules import fdfs
import unittest
import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest, linregress


# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# set up logging to file
fh = logging.FileHandler("logs/fdfs_test.log", mode="w")
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)


class TestFDFs(unittest.TestCase):
    def test_sample_linear_fdf_distribution(self):
        mean = 10.0
        samples = np.array([fdfs.sample_linear_fdf(mean) for _ in range(100000)])

        # check that the mean is close to the expected value
        sample_mean = float(np.mean(samples))
        logger.debug(f"sample_mean: {sample_mean}")
        self.assertLess(abs(sample_mean - mean), 0.05)
        # check that no values are greater than 3*mean
        self.assertLessEqual(max(samples), 3 * mean)
        # check that no values are less than 0
        self.assertGreaterEqual(min(samples), 0)

        plt.hist(samples, bins=100, density=True, histtype="step")
        plt.show()

    def test_sample_exponential_fdf_distribution(self):
        mean = 10.0
        samples = np.array([fdfs.sample_exponential_fdf(mean) for _ in range(10000)])

        # Check if the distribution is exponential using a linear regression on the log of the histogram
        hist, bins = np.histogram(samples, bins=100, density=True)
        log_hist = np.log(hist[hist > 0])
        slope, intercept, r_value, p_value, std_err = linregress(
            range(len(log_hist)), log_hist
        )
        self.assertLess(
            abs(slope + 1 / mean), 0.05
        )  # Fail if the slope is not close to -1/mean

        # Optional: plot the empirical cumulative distribution function (CDF)
        plt.hist(samples, bins=100, density=True, histtype="step")
        plt.show()
