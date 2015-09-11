from setuptools import setup, find_packages
from os import path

with open(path.join(
            path.abspath(path.dirname(__file__)),
            'README.md',
        )) as f:
    long_desc = f.read()

setup(
    name='request',
    version='0.0.1',
    description='Make requests to CouchPotato and others',
    long_description=long_desc,
    author='Jay Vana',
    author_email='jaysvana@gmail.com',
    license='MIT',
    requires=[
        'tabulate',
    ],
)
