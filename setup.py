from setuptools import setup, find_packages
from typing import List


def find_packages(requirments:str) -> list:
    with open(requirments, 'r') as f:
        packages = f.readlines()
    packages = [pkg.strip() for pkg in packages]   
    return packages

    
setup(
    name='my_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
    include_package_data=True,
    description='A simple Flask web application',
    author='PathFinder Team',
    entrypoints={
        'console_scripts': [
            'run-app=app:app.run',
        ],
    },
)
