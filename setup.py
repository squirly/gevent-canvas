#!/usr/bin/env python
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='gevent-canvas',
    version='0.1.0',
    url='',
    license='',
    author='Tyler Jones',
    author_email='tyler@squirly.ca',
    description='Gevent workflow management inspired by Celery\'s Canvas.',
    long_description=open('README').read(),
    packages=['gevent_canvas'],
    install_requires=['gevent'],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
)
