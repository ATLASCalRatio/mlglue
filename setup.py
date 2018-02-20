#!/usr/bin/env python

from setuptools import setup

setup(name='mlglue',
    version='0.24',
    description='Glue between machine learning libraries',
    author='Joosep Pata',
    author_email='pata@phys.ethz.ch',
	maintainer = 'Gordon Watts',
	maintainer_email = 'gwatts@uw.edu',
    url='https://github.com/ATLASCalRatio/mlglue',
    packages=['mlglue'],
    install_requires=['sklearn', 'numpy'],
)

