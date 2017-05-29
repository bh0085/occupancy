import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "occupancy",
    version = ".1",
    author = "Ben Holmes",
    author_email = "ben@aeronaut.net",
    description = ("Tools for visualizing reporting on hourlyline data"),
    license = "MIT",
    keywords = "aeronaut",
    url = "http://github.com/bh0085/occupancy",
    install_requires=['Flask','flask-restful','flask_assets','sqlalchemy','flask-sqlalchemy-session','pyscss','dateparser','alembic','babel','numpy'],
    packages=[''],
    long_description=read('README.md')
)
