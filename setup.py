from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().split('\n')


extras_require = {
    'tests': [
        'flake8>=3.2.1, <3.999.0',
        'pytest>5.4.0, <5.999.0'
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
    install_requires=requirements,
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
