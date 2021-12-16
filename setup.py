import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

VERSION = '0.1.1'
DESCRIPTION = 'Python libary for the use of the public transport and carsharing API of the Stadtwerke Ulm / Neu-Ulm (SWU).'

setup(
    name="swu_api",
    version=VERSION,
    author="Cedric Klimt",
    author_email="cekl@gmx.net",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['reptaskorg'],
    license='MIT',
    url="https://github.com/CeKl/swu_api",
    py_modules=["swu_api"],

    keywords=['python', 'publictransport', 'carsharing', 'swu', 'ulm', 'neu-ulm'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
