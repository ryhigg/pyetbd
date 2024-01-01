# This file is used for the package creation when uploading to PyPi


from setuptools import setup, find_packages

LONG_DESCRIPTION = "This is an open-source Python package to implement McDowell's (2004) Evolutionary Theory of Behavior Dynamics. The package is currently under development. This version has successfully replicated the results of McDowell et al. (2008). It is not recommended to run experiments for publication until the package has been validated by replicating more results from the literature."

setup(
    name="pyetbd",
    version="0.1.0",
    author="Ryan Higginbotham",
    author_email="ryanhigginbotham@ufl.edu",
    description="McDowell's (2004) ETBD implemented in Python",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "numba==0.57.1",
        "numpy==1.24.4",
        "pandas==2.1.0",
        "openpyxl",
    ],
)
