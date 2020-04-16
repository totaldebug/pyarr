from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as r:
    readme = r.read()

setup(
    name='PyArr',
    version='0.2',
    install_requires=requirements,
    packages=['PyArr',],
    license='Sonarr and Radarr API Wrapper',
    long_description=readme
)
