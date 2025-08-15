from setuptools import setup, find_packages
from pathlib import Path

# Long description for PyPI (from README.md)
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="dodo-lookup",
    version="0.2.8",
    description="A minimal and colorful terminal tool to check domain availability across TLDs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Oguzhan Budak",
    url="https://github.com/OggyB/dodo",
    packages=find_packages(),
    install_requires=[
        "python-whois",
        "termcolor",
        "pyfiglet",
        "prettytable",
        "tqdm"
    ],
    package_data={
        "dodo": ["tlds.txt"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dodo = dodo.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Topic :: Internet :: Name Service (DNS)",
    ],
    python_requires=">=3.7",
)
