"""This module provides a Python wrapper for Radarr and Sonarr"""

import setuptools

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md") as r:
    readme = r.read()

setuptools.setup(
    name="PyArr",
    version="0.8.1",
    author="marksie1988",
    description="A Sonarr and Radarr API Wrapper",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/marksie1988/PyArr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    packages=["PyArr",],
    license="MIT",
)
