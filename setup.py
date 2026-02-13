from setuptools import setup, find_packages
from typing import List


def get_requirements(requirements_file: str) -> List[str]:
    """Read requirements from file and return as list."""
    with open(requirements_file, 'r') as f:
        packages = f.readlines()
    packages = [pkg.strip() for pkg in packages if pkg.strip() and not pkg.startswith('#')]
    return packages

    
setup(
    name='pathfinder',
    version='0.1.0',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    include_package_data=True,
    description='A Flask-based PathFinder web application',
    author='PathFinder Team',
    author_email='thanushreddy934@gmail.com',
    url='https://github.com/thanush2205/PathFinder',
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'pathfinder=app:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
