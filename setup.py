import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hortee",
    version = "0.1",
    url = "http://github.com/bne/hortee",
    license = "Apache2",
    description = "Event driven django plant tracking thing",
    long_description = read('README.rst'),
    author = "Ben Miller",
    author_email = "ben@hyl.co.uk",
    packages = find_packages("src"),
    package_dir = {"": "src"},
    install_requires = ["setuptools"],
)
