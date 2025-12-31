"""Setup script for ChipaPocketOptionData."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="ChipaPocketOptionData",
    version="1.0.0",
    author="ChipaDev Team",
    author_email="",
    description="Multi-process data collection library for PocketOption using BinaryOptionsToolsV2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChipaDevTeam/ChipaPocketOptionData",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "BinaryOptionsToolsV2>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords="pocketoption binary-options trading data-collection multiprocessing proxy",
    project_urls={
        "Bug Reports": "https://github.com/ChipaDevTeam/ChipaPocketOptionData/issues",
        "Source": "https://github.com/ChipaDevTeam/ChipaPocketOptionData",
    },
)
