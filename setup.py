from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pycricinfo",
    version="0.0.1",
    description="A lightweight wrapper around Cricinfo",
    license="MIT",
    install_requires=["requests", "bs4", "dateparser"],
    author="Alexander Sutcliffe",
    author_email="sutcliffe.alex@gmail.com",
    url="http://github.com/scrambldchannel/pycricinfo",
    keywords="cricket",
    classifiers=["Development Status :: 3 - Alpha"],
)
