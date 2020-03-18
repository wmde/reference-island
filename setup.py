import os

from setuptools import setup


with open('README.md', 'r') as f:
    readme = f.read()


def requirements(fname):
    return [line.strip()
            for line in open(os.path.join(os.path.dirname(__file__), fname))]


setup(
    name="wikidatarefisland",
    version="0.0.1",
    author="Wikidata dev team",
    description="A data pipieline to extract reference for Wikidata",
    license="GPLv3",
    url="https://github.com/wmde/reference-island",
    long_description=readme,
    install_requires=requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GPLv3 License"
    ],
    packages=['wikidatarefisland'],
    tests_require=requirements('requirements-dev.txt'),
    package_dir={'wikidatarefisland': 'wikidatarefisland'},
    python_requires='>=2.7.2, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
