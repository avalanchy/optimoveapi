#!/usr/bin/env python
import sys

from distutils.core import setup

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main([
            '--cov', 'optimoveapi',
            '--cov-report', 'term-missing',
        ])
        sys.exit(errno)


test_requirements = [
    'pytest==3.0.2',
    'pytest-cov==2.3.1',
    'httpretty==0.8.14',
    'mock==2.0.0',
]

setup(
    name='OptimoveAPI',
    version='0.1',
    description='Client for Optimove API',
    author='avalanchy',
    author_email='avalanchy@gmail.com',
    url='https://github.com/avalanchy/optimoveapi',
    packages=['optimoveapi'],
    tests_require=test_requirements,
    install_requires=open('requirements.txt').read().splitlines(),
    cmdclass={'test': PyTest},
)
