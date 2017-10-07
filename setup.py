#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: setup.py
Author: dhilipsiva <dhilipsiva@gmail.com>
2017
"""

from setuptools import setup, find_packages

long_description = """
prana
========

Loosely translated Sanskrit word for 'Energy'. Just another interview challenge.

DOCS: https://prana.readthedocs.io/

SOURCE: https://github.com/dhilipsiva/prana

"""

setup(
    name='prana',
    version='0.0.1',
    description=(
        " Loosely translated Sanskrit word for 'Energy'. Just another interview challenge."),
    long_description=long_description,
    url='https://github.com/dhilipsiva/prana',
    author='dhilipsiva',
    author_email='dhilipsiva@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],

    keywords='prana dhilipsiva',
    packages=find_packages(),
    py_modules=['prana'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        prana=prana.cli:cli
    ''',
    extras_require={
        'dev': [],
        'test': ['pytest'],
    },
)
