#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()

setup(name='wilddog-python',
      version='1.0.1',
      description="Python interface to the Wilddog's REST API.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Natural Language :: English',
      ],
      keywords='wilddog python',
      author='Wilddog Team',
      author_email='lijiale@wilddog.com',
      maintainer='Li Jiale',
      maintainer_email='lijiale@wilddog.com',
      url='http://github.com/WildDogTeam/wilddog-python',
      license='MIT',
      packages=['wilddog'],
      test_suite='tests.all_tests',
      install_requires=['requests>=1.1.0'],
      zip_safe=False,
      )
