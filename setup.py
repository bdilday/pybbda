from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="pybbda",
    version="0.1.1",
    author="Ben Dilday",
    author_email="ben.dilday.phd@gmail.com",
    description="Baseball data and analysis in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bdilday/pybbda",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"pybaseballdatana": ["*.csv"]},
    include_package_data=True,
)
