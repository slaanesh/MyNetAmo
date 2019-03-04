# MyNetAtmo tools

This little python script is going to fetch your Netatmo data every 10 minutes and will dump them into a [RRDTool](https://oss.oetiker.ch/rrdtool/) database

## Setup

Copy `dotenv-dist` to `.env` and fill in the required values. If you don't have created a Netatmo app already, you should by visiting https://dev.netatmo.com/myaccount/

## Run

You need python3 and [pipenv](https://pipenv.readthedocs.io/en/latest/) and RRDTool.
Then run:
```shell
$ pipenv install
$ pipenv run ./collect.py
```

## Generating graphs

Make sure you edit `GRAPH_DIR` environment variable, otherwise if left empty the graphs are gooing to be generate in the current directory. To generate graphs:
```shell
$ pipenv run ./graph.py
```

## Todo

Support for Thermostats
