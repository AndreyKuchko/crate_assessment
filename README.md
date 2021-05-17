# This document describes how to insert the VBB transit dataset into CrateDB

![tests workflow](https://github.com/AndreyKuchko/crate_assessment/actions/workflows/tests.yml/badge.svg)

## Prerequisites

You will need Python 3.7, virtualenv and docker.

## Preparation

1. Create python virtual environment, activate it and install package
```shell
$ python3.7 -m venv env
$ source ./env/bin/activate
$ pip install .
```
2. Run CrateDB image in docker
```shell
$ docker run -d --publish=4200:4200 --publish=5432:5432 crate
```
**Note:** you can choose other ports, but make sure that you change it in script parameters too.
3. Prepare dataset
```shell
$ wget https://www.vbb.de/media/download/2029
$ unzip 2029 -d datasource
$ rm -f 2029
```

## Commands

Following commands are supported in cli interface

### Performs inserting of csv data using sync approach
```shell
$ crate_vbb_importer sync_insert -h
usage: crate_vbb_importer sync_insert [-h] [--host HOST] [-u USER]
                                      [-p PASSWORD] [-s SCHEMA] [-d DATA_DIR]
                                      [-b BATCH_SIZE]
                                      [-l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                                      [--port PORT] [-t TIMEOUT]

Performs sync insert of data from csv files to CrateDB

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           CrateDB host (default: localhost)
  -u USER, --user USER  CrateDB user (default: crate)
  -p PASSWORD, --password PASSWORD
                        CrateDB password (default: None)
  -s SCHEMA, --schema SCHEMA
                        CrateDB schema (default: doc)
  -d DATA_DIR, --data-dir DATA_DIR
                        Directory with csv files (default: datasource)
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        Insert batch size (default: 300)
  -l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}, --log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Log level (default: INFO)
  --port PORT           CrateDB port (default: 4200)
  -t TIMEOUT, --timeout TIMEOUT
                        CrateDB connection timeout (default: 10)
```
Example:
```shell
$ crate_vbb_importer sync_insert
Processing of agency.txt was finished. It took 0.187 seconds, 37 csv lines were processed.
Processing of calendar.txt was finished. It took 0.487 seconds, 2101 csv lines were processed.
Processing of calendar_dates.txt was finished. It took 5.048 seconds, 41709 csv lines were processed.
Processing of frequencies.txt was finished. It took 0.173 seconds, 0 csv lines were processed.
Processing of pathways.txt was finished. It took 0.143 seconds, 0 csv lines were processed.
Processing of routes.txt was finished. It took 0.323 seconds, 1279 csv lines were processed.
Processing of shapes.txt was finished. It took 120.379 seconds, 5030583 csv lines were processed.
Processing of stop_times.txt was finished. It took 585.995 seconds, 5288633 csv lines were processed.
Processing of stops.txt was finished. It took 4.415 seconds, 41733 csv lines were processed.
Processing of transfers.txt was finished. It took 9.370 seconds, 100967 csv lines were processed.
Processing of trips.txt was finished. It took 19.959 seconds, 224268 csv lines were processed.
Finished! It took 746.495 seconds in total
```

### Performs inserting of csv data using async approach
```shell
$ crate_vbb_importer async_insert -h
usage: crate_vbb_importer async_insert [-h] [--host HOST] [-u USER]
                                       [-p PASSWORD] [-s SCHEMA] [-d DATA_DIR]
                                       [-b BATCH_SIZE]
                                       [-l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                                       [--port PORT]

Performs async insert of data from csv files to CrateDB

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           CrateDB host (default: localhost)
  -u USER, --user USER  CrateDB user (default: crate)
  -p PASSWORD, --password PASSWORD
                        CrateDB password (default: None)
  -s SCHEMA, --schema SCHEMA
                        CrateDB schema (default: doc)
  -d DATA_DIR, --data-dir DATA_DIR
                        Directory with csv files (default: datasource)
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        Insert batch size (default: 300)
  -l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}, --log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Log level (default: INFO)
  --port PORT           CrateDB port (default: 5432)
```
Example:
```shell
$ crate_vbb_importer async_insert
Processing of pathways.txt was finished. It took 2.609 seconds, 0 csv lines were processed.
Processing of agency.txt was finished. It took 4.028 seconds, 37 csv lines were processed.
Processing of frequencies.txt was finished. It took 4.223 seconds, 0 csv lines were processed.
Processing of routes.txt was finished. It took 11.641 seconds, 1279 csv lines were processed.
Processing of calendar.txt was finished. It took 15.636 seconds, 2101 csv lines were processed.
Processing of calendar_dates.txt was finished. It took 146.045 seconds, 41709 csv lines were processed.
Processing of stops.txt was finished. It took 148.155 seconds, 41733 csv lines were processed.
Processing of shapes.txt was finished. It took 166.931 seconds, 5030583 csv lines were processed.
Processing of transfers.txt was finished. It took 175.572 seconds, 100967 csv lines were processed.
Processing of trips.txt was finished. It took 199.422 seconds, 224268 csv lines were processed.
Processing of stop_times.txt was finished. It took 752.140 seconds, 5288633 csv lines were processed.
Finished! It took 752.314 seconds in total
```

### Performs database cleaning
```shell
$ crate_vbb_importer clean -h
usage: crate_vbb_importer clean [-h] [--host HOST] [-u USER] [-p PASSWORD]
                                [-s SCHEMA] [-d DATA_DIR] [-b BATCH_SIZE]
                                [-l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                                [--port PORT]

Drops all related tables from database

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           CrateDB host (default: localhost)
  -u USER, --user USER  CrateDB user (default: crate)
  -p PASSWORD, --password PASSWORD
                        CrateDB password (default: None)
  -s SCHEMA, --schema SCHEMA
                        CrateDB schema (default: doc)
  -d DATA_DIR, --data-dir DATA_DIR
                        Directory with csv files (default: datasource)
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        Insert batch size (default: 300)
  -l {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}, --log-level {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
                        Log level (default: INFO)
  --port PORT           CrateDB port (default: 5432)
```
Example:
```shell
$ crate_vbb_importer clean
Finished! It took 0.413 seconds in total
```

## How to run tests
```shell
$ pip install tox
$ tox
```
