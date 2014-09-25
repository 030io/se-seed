# -*- coding: utf-8 -*-
__author__ = 'chinfeng'

from setuptools import setup

setup(
    name='se-seed',
    author='Chinfeng Chung',
    test_suite = 'tests',

    install_requires=[
        'pymongo',
    ],
)