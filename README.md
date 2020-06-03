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

* Fangraphs leaderboards

The following are planned for a future release:

* Statcast play-by-play data

* Retrosheet event data

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

This package is available on github. 

You can install directly from the repo using
`pip`,

```python
 pip install git+https://github.com/bdilday/pybbda.git
```

or download the source,

```bash
$ git clone git@github.com:bdilday/pybbda.git
$ cd pybbda
$ pip install -e .
```

### Requirements

This package explicitly 
supports `Python 3.6` and`Python 3.7`. It aims
to support `Python 3.8` but this is not guaranteed.
It explicitly *does not* support any versions 
prior to `Python 3.6`, including`Python 2.7`.


### Package vs module name

In the tradition of `scikit-learn`, the `pybbda` *package*
provides a *module* `pybaseballdatana`. This means imports work in
the following way,

```python
from pybaseballdatana.data import LahmanData
``` 

This also means the installation directory is `pybaseballdatana`
and not `pybbda`.

### Environment variables

The package uses the following environment variables

* `PYBBDA_DATA_ROOT` 

The root directory for storing data 
(See [Installing data](#Installing-data)). Defaults to `${INSTALLATION_ROOT}/data/assets` 
where `${INSTALLATION_ROOT}` is the path the the `pybbda` installation. 
The code location is typically a path to the `Python` installation
plus `site-packages/pybaseballdatana`. 

This can cause a problem with write permissions 
if you're using a system `Python` instead of a user-controlled
[virtual environment](https://docs.python.org/3.7/library/venv.html). 
For this reason, and to avoid duplication if the package is 
installed into multiple virtual environments, it's 
recommended to use a custom path for `PYBBDA_DATA_ROOT`, for example,

```bash
export PYBBDA_DATA_ROOT=${HOME}/.pybbda/data
```

* PYBBDA_LOG_LEVEL

This sets the [logging level](https://docs.python.org/3.7/library/logging.html) for the package at runtime.
The default is `INFO`.


### Installing data

This package ships without any data. Instead it provides tools 
to fetch and store data from a variety of sources. To install
data you can use the `update` tool in the `pybaseballdatana.data.tools`
sub-module. 

Example, 

```bash
$ python -m pybaseballdatana.data.tools.update -h
usage: update.py [-h] [--data-root DATA_ROOT] --data-source
                 {Lahman,BaseballReference,Fangraphs,all} [--make-dirs]
                 [--overwrite] [--min-year MIN_YEAR] [--max-year MAX_YEAR]
                 [--num-threads NUM_THREADS]

optional arguments:
  -h, --help            show this help message and exit
  --data-root DATA_ROOT
                        Root directory for data storage
  --data-source {Lahman,BaseballReference,Fangraphs,all}
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

The `min-year` and `max-year` arguments refer only
to Fangraphs leaderboards as of now. 


Example to download Lahman data

```bash
$ python -m pybaseballdatana.data.tools.update --data-source Lahman 
INFO:pybaseballdatana.data.sources.lahman._update:_update:downloading file from https://github.com/chadwickbureau/baseballdatabank/archive/master.zip
```

By default the script will expect the target 
directory to exist and raise a `ValueError` and exit if it does not, example, 

```bash
$ python -m pybaseballdatana.data.tools.update --data-source Lahman --data-root /tmp/missing
CRITICAL:root:update:The target path /tmp/missing does not exist. You can create it or pass option --make-dirs to update to create it automatically
ValueError: missing target path /tmp/missing. You can create it or pass option --make-dirs to update to create it automatically
```

Use the `--make-dirs` flag to allow the script to make missing
directories,

```bash
$ python -m pybaseballdatana.data.tools.update --data-source Lahman --data-root /tmp/missing --make-dirs
INFO:pybaseballdatana.data.sources.lahman._update:_update:downloading file from https://github.com/chadwickbureau/baseballdatabank/archive/master.zip

$ ls /tmp/missing/
Lahman
```


Example to download Baseball Reference WAR

```bash
$ python -m pybaseballdatana.data.tools.update --data-source BaseballReference
INFO:pybaseballdatana.data.sources.baseball_reference._update:_update:downloading file from https://www.baseball-reference.com/data/war_daily_bat.txt
INFO:pybaseballdatana.data.sources.baseball_reference._update:_update:saving file to /home/bdilday/.pybbda/data/BaseballReference/war_daily_bat.txt.gz
INFO:pybaseballdatana.data.sources.baseball_reference._update:_update:downloading file from https://www.baseball-reference.com/data/war_daily_pitch.txt
INFO:pybaseballdatana.data.sources.baseball_reference._update:_update:saving file to /home/bdilday/.pybbda/data/BaseballReference/war_daily_pitch.txt.gz
```

Example Fangraphs guts constants and leaderboards. Note that because downloading the full set of
leaderboard data starting from 1871 takes 5-10 minutes, 
by default the years downloaded are 2018 - 2019 only. To get them all
use `--min-year 1871`

```bash
$ python -m pybaseballdatana.data.tools.update --data-source Fangraphs --min-year 2019
INFO:pybaseballdatana.data.sources.fangraphs._update:_update:saving file to /home/bdilday/.pybbda/data/Fangraphs/fg_guts_constants.csv.gz
INFO:pybaseballdatana.data.sources.fangraphs._update:_update:saving file to /home/bdilday/.pybbda/data/Fangraphs/fg_bat_2019.csv.gz
INFO:pybaseballdatana.data.sources.fangraphs._update:_update:saving file to /home/bdilday/.pybbda/data/Fangraphs/fg_pit_2019.csv.gz
```

Example to download all sources,

```bash
$ python -m pybaseballdatana.data.tools.update --data-source all --min-year 2019
```

## Example Usage

After installing some or all of the data, you can start using the 
package.

Following are a few minimal examples, more extensive documentation,
including examples, is a work in progress.

### Lahman data

```python
>>> from pybaseballdatana.data import LahmanData
>>> lahman_data = LahmanData()
>>> batting_df= lahman_data.batting
INFO:pybaseballdatana.data.sources.lahman.data:data:searching for file /home/bdilday/.pybbda/data/Lahman/Batting.csv
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

### Baseball Reference WAR

```python
>>> from pybaseballdatana.data import BaseballReferenceData
>>> bbref_data = BaseballReferenceData()
>>> bbref_data.war_bat
INFO:pybaseballdatana.data.sources.baseball_reference.data:data:searching for file /home/bdilday/.pybbda/data/BaseballReference/war_daily_bat.txt
           name_common   age    mlb_ID  player_ID  year_ID  ... waa_win_perc_def  waa_win_perc_rep  OPS_plus   TOB_lg    TB_lg
0        David Aardsma  22.0  430911.0  aardsda01     2004  ...           0.5000            0.5000       NaN    0.000    0.000
1        David Aardsma  24.0  430911.0  aardsda01     2006  ...           0.5000            0.4998 -100.0000    0.694    0.896
2        David Aardsma  25.0  430911.0  aardsda01     2007  ...           0.5000            0.5000       NaN    0.000    0.000
3        David Aardsma  26.0  430911.0  aardsda01     2008  ...           0.5000            0.4992 -100.0000    0.345    0.434
4        David Aardsma  27.0  430911.0  aardsda01     2009  ...           0.5000            0.5000       NaN    0.000    0.000
...                ...   ...       ...        ...      ...  ...              ...               ...       ...      ...      ...
107352  Dutch Zwilling  26.0  124791.0  zwilldu01     1915  ...           0.5000            0.4919  141.9576  199.168  188.348
107353  Dutch Zwilling  27.0  124791.0  zwilldu01     1916  ...           0.4952            0.4934    7.3266   18.514   18.757
107354       Tony Zych  24.0  543964.0   zychto01     2015  ...              NaN               NaN       NaN    0.000    0.000
107355       Tony Zych  25.0  543964.0   zychto01     2016  ...              NaN               NaN       NaN    0.000    0.000
107356       Tony Zych  26.0  543964.0   zychto01     2017  ...           0.5000            0.5000       NaN    0.000    0.000

[107357 rows x 49 columns]
>>> bbref_data.war_bat.sort_values("WAR", ascending=False).head(6)
             name_common   age    mlb_ID  player_ID  year_ID  ... waa_win_perc_def  waa_win_perc_rep  OPS_plus   TOB_lg    TB_lg
84460          Babe Ruth  28.0  121578.0   ruthba01     1923  ...           0.5080            0.4834  239.0187  252.578  211.149
84458          Babe Ruth  26.0  121578.0   ruthba01     1921  ...           0.4996            0.4841  238.4715  253.759  229.230
84464          Babe Ruth  32.0  121578.0   ruthba01     1927  ...           0.5032            0.4840  225.0409  242.569  220.158
106270  Carl Yastrzemski  27.0  124650.0  yastrca01     1967  ...           0.5118            0.4835  193.2196  219.724  219.557
44652     Rogers Hornsby  28.0  116156.0  hornsro01     1924  ...           0.5085            0.4863  221.8809  214.748  214.614
8817         Barry Bonds  36.0  111188.0  bondsba01     2001  ...           0.4930            0.4865  258.7176  219.120  202.824

[6 rows x 49 columns]
>>> bbref_data.war_pitch.query("year_ID >= 1911").sort_values("WAR", ascending=False).head(6)
          name_common   age    mlb_ID  player_ID  year_ID  ... pyth_exponent_rep  waa_win_perc_rep WAR_rep    ERA_plus    ER_lg
21163  Walter Johnson  25.0  116635.0  johnswa01     1913  ...             1.843            0.4294  3.5162  258.925000  113.927
21162  Walter Johnson  24.0  116635.0  johnswa01     1912  ...             1.915            0.4257  3.7861  242.798246  138.395
15490   Dwight Gooden  20.0  114947.0  goodedw01     1985  ...             1.857            0.4293  2.5333  228.665957  107.473
6474    Steve Carlton  27.0  112008.0  carltst01     1972  ...             1.835            0.4288  3.0028  182.243421  138.505
7745    Roger Clemens  34.0  112388.0  clemero02     1997  ...             1.971            0.4188  2.6641  221.573333  132.944
525    Pete Alexander  33.0  110127.0  alexape01     1920  ...             1.832            0.4380  2.9949  166.094805  127.893

[6 rows x 42 columns]
```

### Fangraphs guts

```python
>>> from pybaseballdatana.data import FangraphsData
>>> fg_data = FangraphsData()
>>> fg_data.fg_guts_constants
     Season   wOBA  wOBAScale    wBB   wHBP    w1B    w2B    w3B    wHR  runSB  runCS   R/PA     R/W   cFIP
0      2019  0.320      1.157  0.690  0.719  0.870  1.217  1.529  1.940    0.2 -0.435  0.126  10.296  3.214
1      2018  0.315      1.226  0.690  0.720  0.880  1.247  1.578  2.031    0.2 -0.407  0.117   9.714  3.161
2      2017  0.321      1.185  0.693  0.723  0.877  1.232  1.552  1.980    0.2 -0.423  0.122  10.048  3.158
3      2016  0.318      1.212  0.691  0.721  0.878  1.242  1.569  2.015    0.2 -0.410  0.118   9.778  3.147
4      2015  0.313      1.251  0.687  0.718  0.881  1.256  1.594  2.065    0.2 -0.392  0.113   9.421  3.134
..      ...    ...        ...    ...    ...    ...    ...    ...    ...    ...    ...    ...     ...    ...
144    1875  0.261      1.274  0.730  0.761  0.927  1.309  1.654  2.045    0.2 -0.531  0.156  12.231  2.370
145    1874  0.282      1.145  0.760  0.789  0.938  1.281  1.591  1.886    0.2 -0.629  0.179  14.227  2.808
146    1873  0.303      1.025  0.788  0.814  0.947  1.255  1.531  1.739    0.2 -0.741  0.207  16.482  2.932
147    1872  0.297      1.020  0.791  0.816  0.949  1.255  1.530  1.725    0.2 -0.763  0.213  16.926  3.508
148    1871  0.312      0.909  0.797  0.820  0.938  1.211  1.456  1.584    0.2 -0.863  0.237  18.954  3.580

[149 rows x 14 columns]
```

### Fangraphs leaderboards

```python
>>> from pybaseballdatana.data import FangraphsData
>>> fg_data = FangraphsData()
>>> fg_data.fg_batting_2019.sort_values("WAR", ascending=False).head(6)
     #              Name          Team  Season  Age    G   AB   PA    H  ...  GB%+  FB%+  HR/FB%+  Pull%+  Cent%+  Oppo%+  Soft%+  Med%+  Hard%+
20  21        Mike Trout        Angels    2019   27  134  470  600  137  ...    58   135      169     102      98      98      78     95     116
28  29      Alex Bregman        Astros    2019   25  156  554  690  164  ...    75   126      122     110     107      74      89     89     118
32  33    Cody Bellinger       Dodgers    2019   23  156  558  660  170  ...    73   119      159     118      94      79      78     85     126
19  20  Christian Yelich       Brewers    2019   27  130  489  580  161  ...   101   101      212      97     109      93      86     79     130
83  84     Marcus Semien     Athletics    2019   28  162  657  747  187  ...    97   107      100     107      93      99      89     96     110
39  40       Ketel Marte  Diamondbacks    2019   25  144  569  628  187  ...   101    98      123     108     103      83      93     96     108

[6 rows x 306 columns]
>>> fg_data.fg_pitching_2019.sort_values("WAR", ascending=False).head(6)
       #              Name       Team  Season  Age   W   L   ERA   G  ...  GB%+  FB%+  HR/FB%+  Pull%+  Cent%+  Oppo%+  Soft%+  Med%+  Hard%+
93    94       Gerrit Cole     Astros    2019   28  20   5  2.50  33  ...    95   108      110      90     101     114     115    103      89
84    85      Jacob deGrom       Mets    2019   31  11   8  2.43  32  ...   102    99       73      96      96     112     127    108      78
213  214        Lance Lynn    Rangers    2019   32  16  11  3.67  33  ...    95   105       65      93     100     111      93    100     103
123  124      Max Scherzer  Nationals    2019   34  11   7  2.92  27  ...    94   109       76     103      90     108     110    102      94
95    96  Justin Verlander     Astros    2019   36  21   6  2.58  34  ...    85   124      105     108     104      82     101     91     110
141  142    Charlie Morton       Rays    2019   35  16   6  3.05  33  ...   114    82       68      95      99     110      98    110      89

[6 rows x 323 columns]
```

### Marcel projections 

```python
>>> from pybaseballdatana.analysis.projections import MarcelProjectionsBatting, MarcelProjectionsPitching
>>> batting_marcels = MarcelProjectionsBatting()
>>> batting_marcels.projections(projected_season=2020).sort_values("HR", ascending=False).head(5)
                         1B         2B        3B         HR         BB        HBP         SB        CS          SO        SH        SF
playerID  yearID                                                                                                                      
alonspe01 2020    61.835746  24.424880  1.776910  36.479123  55.530717  13.808065   2.380606  0.634653  134.823677  0.268709  2.740424
martijd02 2020    88.221199  30.439315  2.178894  35.774207  61.850212   3.273532   4.228616  0.703440  133.531288  0.176546  5.085481
troutmi01 2020    68.296501  24.724267  2.726739  35.413694  98.294393  10.368346  15.968754  2.492124  110.910443  0.177973  3.910907
bellico01 2020    78.348910  28.931966  4.151507  34.120187  73.574174   2.929709  12.346877  2.957267  121.966159  0.180862  3.481480
suareeu01 2020    80.978952  21.878351  1.930468  33.101862  64.662073   8.582563   3.132271  2.358739  146.982596  0.173745  5.240382

[635 rows x 11 columns]
>>> pitching_marcels = MarcelProjectionsPitching()
>>> pitching_marcels.projections(projected_season=2020).sort_values("SO", ascending=False).head(5)
                           H         HR         ER         BB          SO        HBP          R
playerID  yearID                                                                               
colege01  2020    145.190329  23.916119  66.034603  53.325072  242.445196   4.835923  71.164678
verlaju01 2020    145.192833  28.656685  65.550935  47.145311  233.046279   6.302306  68.739815
degroja01 2020    147.740156  17.419418  55.997757  47.226040  214.747754   5.515039  61.433772
scherma01 2020    134.729027  19.137910  57.718204  43.170277  212.630013   8.205640  61.732141
bauertr01 2020    162.130978  23.420415  79.459799  67.396411  210.995752  11.851444  87.746950

[775 rows x 7 columns]
```

### Batted ball trajectories

```python
>>> from pybaseballdatana.analysis.trajectories import BattedBallTrajectory
>>> trajectory_calc = BattedBallTrajectory()
>>> trajectory = trajectory_calc.get_trajectory(initial_speed=100, launch_angle=20, launch_direction_angle=0, initial_spin=2500, spin_angle=-10)
>>> trajectory
            t             x           y         z        vx          vy         vz
0    0.000449  4.489077e-07    2.061907  3.022532  0.001999  137.830861  50.163946
1    0.004940  5.425019e-05    2.680435  3.247593  0.021947  137.610786  50.059854
2    0.014940  4.947793e-04    4.054102  3.747033  0.066097  137.123263  49.828060
3    0.024940  1.374979e-03    5.422911  4.244154  0.109882  136.639159  49.596236
4    0.034940  2.691216e-03    6.786897  4.738957  0.153305  136.158444  49.364384
..        ...           ...         ...       ...       ...         ...        ...
450  4.494940  1.882760e+01  387.451152  1.638192  5.647055   62.372619 -46.643721
451  4.504940  1.888407e+01  388.074671  1.170890  5.647418   62.331176 -46.816578
452  4.514940  1.894054e+01  388.697776  0.701861  5.647756   62.289952 -46.989108
453  4.524940  1.899702e+01  389.320470  0.231109  5.648070   62.248948 -47.161310
454  4.534940  1.905351e+01  389.942756 -0.241364  5.648359   62.208161 -47.333182

[455 rows x 7 columns]
>>> trajectory.z.max()
57.57010079059938
```

### Run expectancies from Markov chains

There is a cli tool for computing run expectancies from 
Markov chains. 

```bash
$ python -m pybaseballdatana.analysis.run_expectancy.markov.cli --help
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
$ python -m pybaseballdatana.analysis.run_expectancy.markov.cli -b 0 0.08 0.15 0.05 0.005 0.03 --running-probs 0 0 0 0 
mean score per 27 outs = 3.5227
std. score per 27 outs = 2.8009
```

**Example**: Use a default set of probabilities for all 9 slots with default probabilities for taking extra bases

```bash
$ python -m pybaseballdatana.analysis.run_expectancy.markov.cli -b 0 0.08 0.15 0.05 0.005 0.03
mean score per 27 outs = 4.2242
std. score per 27 outs = 3.0161
```
**Example**: Use a default set of probabilities for all 9 slots but let 
Rickey Henderson 1982 bat leadoff (using 27 outs, instead of 3)

```bash
$ PYBBDA_MAX_OUTS=27  python -m pybaseballdatana.analysis.run_expectancy.markov.cli -b 0 0.08 0.15 0.05 0.005 0.03 -i 1 henderi01_1982
WARNING:pybaseballdatana:__init__:Environment variable PYBBDA_DATA_ROOT is not set, defaulting to /home/bdilday/github/pybbda/pybaseballdatana/data/assets
INFO:pybaseballdatana.data.sources.lahman.data:data:searching for file /home/bdilday/github/pybbda/pybaseballdatana/data/assets/Lahman/Batting.csv
mean score per 27 outs = 4.3628
std. score per 27 outs = 3.0999
```

**Example**: Use a default set of probabilities for all 9 slots but let 
Rickey Henderson 1982 bat leadoff and Babe Ruth 1927 bat clean-up (using 27 outs, instead of 3)

```bash
$ PYBBDA_MAX_OUTS=27  python -m pybaseballdatana.analysis.run_expectancy.markov.cli -b 0 0.08 0.15 0.05 0.005 0.03 -i 1 henderi01_1982 -i 4 ruthba01_1927 
WARNING:pybaseballdatana:__init__:Environment variable PYBBDA_DATA_ROOT is not set, defaulting to /home/bdilday/github/pybbda/pybaseballdatana/data/assets
INFO:pybaseballdatana.data.sources.lahman.data:data:searching for file /home/bdilday/github/pybbda/pybaseballdatana/data/assets/Lahman/Batting.csv
mean score per 27 outs = 5.1420
std. score per 27 outs = 3.3996
```


## License

[MIT](https://choosealicense.com/licenses/mit/)
