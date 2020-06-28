from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


def process_line(line):
    return line.strip().split("=")[0].replace(">", "").replace("~", "")


with open("requirements.txt", "r") as fh:
    install_requires = [process_line(line) for line in fh.readlines() if len(line) > 1]

setup(
    name="pybbda",
    version="0.2.1",
    author="Ben Dilday",
    author_email="ben.dilday.phd@gmail.com",
    description="Baseball data and analysis in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bdilday/pybbda",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    package_data={"pybbda": ["*.csv"]},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "pybbda_data_update=pybbda.data.tools.update:main",
            "pybbda_run_expectancy=pybbda.analysis.run_expectancy.markov.cli:main",
        ]
    },
)
