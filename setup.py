from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="devflow-ai",
    version="1.0.0",
    author="rud-13",
    description="AI-Powered Code Review & PR Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rud-13/project",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "devflow=devflow.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
