# This file is used for the package creation when uploading to PyPi


from setuptools import setup, find_packages


setup(
    name="pyetbd",
    version="0.1.0",
    author="Ryan Higginbotham",
    author_email="ryanhigginbotham@ufl.edu",
    description="McDowell's (2004) ETBD implemented in Python",
    packages=find_packages(),
    install_requires=[
        "numba==0.57.1",
        "numpy==1.24.4",
        "pandas==2.1.0",
    ],
)
