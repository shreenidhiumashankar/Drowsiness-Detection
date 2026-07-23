"""Setup configuration for the Drowsiness Detection package."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="drowsiness-detection",
    version="1.0.0",
    author="Shreenidhi",
    description="Real-time driver drowsiness and yawn detection system using MediaPipe Face Mesh, OpenCV, and Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shreenidhi-umashankar/Drowsiness-Detection",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "drowsiness-detection=main:main",
        ],
    },
)
