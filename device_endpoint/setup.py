"""
Package setup.py
"""

import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='device_endpoint',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='Public Domain',
    description='Demo IoT device endpoint',
    entry_points={
        'console_scripts': [
            'run-device_endpoint=device_endpoint.__main__:main',
            ]
        },
)
