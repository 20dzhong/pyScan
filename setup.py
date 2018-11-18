from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="pyScan",
    version="1.0.0",
    author="20dzhong",
    description="Python wrapper to recreate a scanner app",
    url="https://github.com/20dzhong",
    install_requires=requirements,
    packages=find_packages(),
)