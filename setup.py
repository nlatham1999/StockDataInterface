import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StockDataInterface", 
    version="1.1.4",
    author="nick latham",
    author_email="nlatham@zagmail.gonzaga.edu",
    description="An API for Yahoo Finance that collects current and historical stock data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nlatham1999/StockAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)