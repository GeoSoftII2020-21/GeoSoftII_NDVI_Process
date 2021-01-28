'''setup.py - ndvi - Magdalena Fischer, Cornelius Zerwas'''

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ndvi", 
    version="0.0.1",
    author="Magdalena Fischer, Cornelius Zerwas",
    author_email="m09fischer@gmail.com, cornelius.zerwas@t-online.de",
    description="A script for calculating the monthly-mean-NDVI ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GeoSoftII2020-21",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='3.8.6',
)
