#!/usr/bin/env python
import sys

from distutils.core import setup

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        default_args = [
            '--cov', 'optimoveapi',
            '--cov-report', 'term-missing',
        ]
        pytest_args = self.pytest_args.split()
        errno = pytest.main(default_args + pytest_args)
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
