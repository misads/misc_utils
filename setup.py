import re
import setuptools
from setuptools import setup

with open('misc_utils/version.py') as fid:
    try:
        __version__, = re.findall( '__version__ = "(.*)"', fid.read() )
    except:
        raise ValueError("could not find version number")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='utils-misc',
    version=__version__,
    description='Misc_Utils - Misc system and time utilities for python projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/misads/misc_utils',
    author='Haoyu Xu',
    author_email='xuhaoyu@tju.edu.cn',
    license='MIT',
    install_requires=[
        "numpy",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.5',
)
