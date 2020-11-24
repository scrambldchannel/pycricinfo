from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pycricinfo",
    version="0.0.2",
    description="A lightweight wrapper around Cricinfo",
    license="MIT",
    install_requires=["gazpacho"],
    author="Alexander Sutcliffe",
    author_email="sutcliffe.alex@gmail.com",
    url="http://github.com/scrambldchannel/pycricinfo",
    packages=find_packages(),
    keywords="cricket",
    classifiers=["Development Status :: 3 - Alpha"],
)
