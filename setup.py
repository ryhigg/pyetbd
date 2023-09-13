# This file is used for the package creation when uploading to PyPi


from setuptools import setup, find_packages
import codecs
import os


VERSION = "1.0.0"
DESCRIPTION = "A package for implementing Mcdowell's (2004) ETBD"


# Setting up
setup(
    name="pyetbd",
    version=VERSION,
    author="Ryan Higginbotham (ryhigg)",
    author_email="ryanhigginbotham@ufl.edu",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["numpy", "pandas", "numba"],
    keywords=["python", "ETBD"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: People interested in the ETBD",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
