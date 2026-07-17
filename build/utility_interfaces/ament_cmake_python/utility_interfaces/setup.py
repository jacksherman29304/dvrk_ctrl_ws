from setuptools import find_packages
from setuptools import setup

setup(
    name='utility_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('utility_interfaces', 'utility_interfaces.*')),
)
