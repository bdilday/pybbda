# pybbda

`pybbda` is a package for 
Python Baseball Data and Analysis. 

### data

`pybbda` aims to provide a uniform framework for
accessing baseball data from various sources. 
The data are exposed as `pandas` `DataFrames`

The data sources it currently supports are:

* Lahman data

* Baseball Reference WAR

* Fangraphs leaderboards and park factors

* Retrosheet event data

* Statcast pitch-by-pitch data


### analysis

`pybbda` also provides analysis tools. 

It currently supports:

* Marcel projections

* Batted ball trajectories

* Run expectancy via Markov chains

The following are planned for a future release:

* Simulations

* and more...!

## Installation

This package is available on PyPI, so you can install it with 
`pip`, 

```bash
$ pip install -U pybbda
```

Or you can install the latest master branch 
directly from the github repo using
`pip`,

```bash
$ pip install git+https://github.com/bdilday/pybbda.git
```

or download the source,

```bash
$ git clone git@github.com:bdilday/pybbda.git
$ cd pybbda
$ pip install .
```

### Requirements

This package explicitly 
supports `Python 3.6` and`Python 3.7`. It aims
to support `Python 3.8` but this is not guaranteed.
It explicitly *does not* support any versions 
prior to `Python 3.6`, including`Python 2.7`.


### Installing data

This package ships without any data. Instead it provides tools 
to fetch and store data from a variety of sources. 

To install data you can use the `update` tool in the `pybbda.data.tools`
sub-module. 

Example, 

```bash
$ python -m pybbda.data.tools.update -h
usage: update.py [-h] [--data-root DATA_ROOT] --data-source
                 {Lahman,BaseballReference,Fangraphs,retrosheet,all} [--make-dirs]
                 [--overwrite] [--min-year MIN_YEAR] [--max-year MAX_YEAR]
                 [--num-threads NUM_THREADS]

optional arguments:
  -h, --help            show this help message and exit
  --data-root DATA_ROOT
                        Root directory for data storage
  --data-source {Lahman,BaseballReference,Fangraphs,retrosheet,all}
                        Update source
  --make-dirs           Make root dir if does not exist
  --overwrite           Overwrite files if they exist
  --min-year MIN_YEAR   Min year to download
  --max-year MAX_YEAR   Max year to download
  --num-threads NUM_THREADS
                        Number of threads to use for downloads

```

The data will be downloaded to `--data-root`, which defaults to the 
`PYBBDA_DATA_ROOT`

Detailed instructions are [provided in the documentation](https://pybbda.readthedocs.io/en/stable/)


## Example Usage

After installing some or all of the data, you can start using the 
package.

Following is an example of accessing Lahman data. 
More [examples are included in the documentation](https://pybbda.readthedocs.io/en/stable/examples.html)

### Lahman data

```python
>>> from pybbda.data import LahmanData
>>> lahman_data = LahmanData()
>>> batting_df= lahman_data.batting
INFO:pybbda.data.sources.lahman.data:data:searching for file /home/bdilday/.pybbda/data/Lahman/Batting.csv
>>> batting_df.head()
    playerID  yearID  stint teamID lgID   G   AB   R   H  2B  3B  HR   RBI   SB   CS  BB   SO  IBB  HBP  SH  SF  GIDP
0  abercda01    1871      1    TRO  NaN   1    4   0   0   0   0   0   0.0  0.0  0.0   0  0.0  NaN  NaN NaN NaN   0.0
1   addybo01    1871      1    RC1  NaN  25  118  30  32   6   0   0  13.0  8.0  1.0   4  0.0  NaN  NaN NaN NaN   0.0
2  allisar01    1871      1    CL1  NaN  29  137  28  40   4   5   0  19.0  3.0  1.0   2  5.0  NaN  NaN NaN NaN   1.0
3  allisdo01    1871      1    WS3  NaN  27  133  28  44  10   2   2  27.0  1.0  1.0   0  2.0  NaN  NaN NaN NaN   0.0
4  ansonca01    1871      1    RC1  NaN  25  120  29  39  11   3   0  16.0  6.0  2.0   2  1.0  NaN  NaN NaN NaN   0.0
>>> batting_df.groupby("playerID").HR.sum().sort_values(ascending=False)
playerID
bondsba01    762
aaronha01    755
ruthba01     714
rodrial01    696
mayswi01     660
            ... 
mcconra01      0
mccolal01      0
mccluse01      0
mcclula01      0
aardsda01      0
Name: HR, Length: 19689, dtype: int64
```


### CLI tools

#### Run expectancies 

There is a cli tool for computing run expectancies from 
Markov chains. 

```bash
$ python -m pybbda.analysis.run_expectancy.markov.cli --help
```

This Markov chain uses a lineup of 
9 batters instead of assuming each batter has the same characteristics.
You can also assign running probabilities, although they apply to 
all batters equally.

You can assign batting-event probabilities using a sequence of 
probabilities, or by referencing a player-season with the 
format `{playerID}_{season}`, where playerID is the 
Lahman ID and season is a 4-digit year. For example, to
refer to Rickey Henderson's 1982 season, use `henderi01_1982`.

The lineup is assigned by giving the lineup slot followed by either 
5 probabilities, or a player-season id. The lineup-slot 0 is a code
to assign all nine batters to this value. Any other specific slots 
will be filled in as noted.

The number of outs to model is 3 by default. It can be changed by setting the 
environment variable `PYBBDA_MAX_OUTS`.

**Example**: Use a default set of probabilities for all 9 slots with no taking extra bases

```bash
$ python -m pybbda.analysis.run_expectancy.markov.cli -b 0 0.08 0.15 0.05 0.005 0.03 --running-probs 0 0 0 0 
mean score per 27 outs = 3.5227
std. score per 27 outs = 2.8009
```

**Example**: Use a default set of probabilities for all 9 slots with default probabilities for taking extra bases

```bash
$ python -m pybbda.analysis.run_expectancy.markov.cli -b 0 0.08 0.15 0.05 0.005 0.03
mean score per 27 outs = 4.2242
std. score per 27 outs = 3.0161
```
**Example**: Use a default set of probabilities for all 9 slots but let 
Rickey Henderson 1982 bat leadoff (using 27 outs, instead of 3)

```bash
$ PYBBDA_MAX_OUTS=27  python -m pybbda.analysis.run_expectancy.markov.cli -b 0 0.08 0.15 0.05 0.005 0.03 -i 1 henderi01_1982
WARNING:pybbda:__init__:Environment variable PYBBDA_DATA_ROOT is not set, defaulting to /home/bdilday/github/pybbda/pybbda/data/assets
INFO:pybbda.data.sources.lahman.data:data:searching for file /home/bdilday/github/pybbda/pybbda/data/assets/Lahman/Batting.csv
mean score per 27 outs = 4.3628
std. score per 27 outs = 3.0999
```

**Example**: Use a default set of probabilities for all 9 slots but let 
Rickey Henderson 1982 bat leadoff and Babe Ruth 1927 bat clean-up (using 27 outs, instead of 3)

```bash
$ PYBBDA_MAX_OUTS=27  python -m pybbda.analysis.run_expectancy.markov.cli -b 0 0.08 0.15 0.05 0.005 0.03 -i 1 henderi01_1982 -i 4 ruthba01_1927 
WARNING:pybbda:__init__:Environment variable PYBBDA_DATA_ROOT is not set, defaulting to /home/bdilday/github/pybbda/pybbda/data/assets
INFO:pybbda.data.sources.lahman.data:data:searching for file /home/bdilday/github/pybbda/pybbda/data/assets/Lahman/Batting.csv
mean score per 27 outs = 5.1420
std. score per 27 outs = 3.3996
```

## Contributing

Contributions from the community are welcome. 
See the [contributing guide](CONTRIBUTING.md).

## License

[GPLv2](https://choosealicense.com/licenses/gpl-2.0/)
