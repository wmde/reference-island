from setuptools import setup, find_packages


extras_require = {
    'tests': [
        'flake8>=3.2.1',
    ],
}

setup(
    name="wikidatarefisland",
    version="0.0.1",
    author="The Wikidata team",
    description="Data pipieline to extract reference for Wikidata",
    license="GPLv3",
    url="https://github.com/wmde/reference-island",
    long_description='',
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GPLv3 License"
    ],
    extras_require=extras_require,
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
    package_dir={'wikidatarefisland': 'wikidatarefisland'},
    python_requires='>=3.7.0',
)
