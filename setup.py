#!/usr/bin/env python3

from distutils.core import setup

setup(name="Python-Scripts",
      version="0.1",
      description="Some useful scripts I created over the years",
      author="Maximilian Schiller",
      author_email="manimax3@hotmail.de",
      url="https://github.com/manimax3/Python-Scripts",
      py_modules=[],
      scripts=['RecursiveFileLogger.py', 'TaskManager.py', 'TwitchOnlineChecker.py', 'gitbetterinit.py'],
      install_requires=["github3.py", "Click",
                        "license", "keyring", "requests", "beautifulsoup4"]
      )
