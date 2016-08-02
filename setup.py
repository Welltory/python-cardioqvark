#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
    'ujson'
]

test_requirements = [
    'pytest'
]

setup(
    name='python_cardioqvark',
    version='0.1.0',
    description="Python API wrapper for CardioQVARK",
    long_description=readme + '\n\n' + history,
    author="Maxim Smirnoff",
    author_email='smirnoffmg@gmail.com',
    url='https://github.com/budurli/python_cardioqvark',
    packages=[
        'python_cardioqvark',
    ],
    package_dir={'python_cardioqvark':
                 'python_cardioqvark'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='python_cardioqvark',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
