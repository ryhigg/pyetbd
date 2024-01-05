# This file is used for the package creation when uploading to PyPi


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name="pyetbd",
    version="0.1.2",
    author="Ryan Higginbotham",
    author_email="ryanhigginbotham@ufl.edu",
    description="McDowell's (2004) ETBD implemented in Python",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numba==0.57.1",
        "numpy==1.24.4",
        "pandas==2.1.0",
        "openpyxl",
    ],
)
