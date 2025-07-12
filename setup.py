"""Set up the Pirate Weather library."""

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


def read(fname):
    """Read the specified file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="python-pirateweather",
    version="1.1.2",
    author="cloneofghosts",
    description=("A thin Python Wrapper for the Pirate Weather API"),
    license="BSD 2-clause",
    keywords="weather API wrapper pirateweather location",
    url="https://github.com/cloneofghosts/python-pirate-weather",
    packages=["pirateweather"],
    package_data={"pirateweather": ["LICENSE.txt", "README.md"]},
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["requests==2.32.4"],
)
