# -*- coding: utf-8; -*-

"""Contenthub application package setup file"""

from setuptools import setup, find_packages

# TODO(): figure a way to mark this package as python3 only
# check `python_version` in setup() params?

setup(name="duel_arena", version="0.1.0",
      description="Runescape-Centric staking simulator.",
      classifiers=["DO NOT PUBLISH :: DO NOT PUBLISH",
                   "Development Status :: 3 - Alpha",
                   "Programming Language :: Python :: 2.7"],
      packages=find_packages(exclude=["tests*", "docs", "contrib", "etc", "bin"]),
)
