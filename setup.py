#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='billybob',
      version='0.1',
      description="BillyBob is the really handy deputy sheriff you didn't know you needed",
      url='http://github.com/paraita/billybob',
      author='Paraita Wohler',
      author_email='paraita.wohler@gmail.com',
      license='MIT',
      packages=['billybob'],
      install_requires=[
          'slackclient',
          'wit',
          'python-dateutil',
          'sophiabus230'
      ],
      test_suite='nose.collector',
      tests_require=[
          'mock',
          'nose',
          'coverage',
          'coveralls'
      ],
      zip_safe=False)
