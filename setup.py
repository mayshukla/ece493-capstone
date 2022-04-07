#!/usr/bin/env python3

from distutils.core import setup

setup(name='Code-to-Kill',
      version='1.0',
      description='Programming-based game',
      author='ECE 493 Group 3',
      packages=['src', 'test'],
     )

package_dir = {
    'src': 'src',
    'test': 'test',
}
