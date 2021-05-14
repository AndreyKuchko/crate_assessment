# This document describes how to insert the VBB transit dataset into CrateDB

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
$ docker run -d --publish=4200:4200 crate
```
**Note:** you can choose other ports, but make sure that you change it in script parameters too.
3. Prepare dataset
```shell
$ wget https://www.vbb.de/media/download/2029
$ unzip 2029 -d datasource
$ rm -f 2029
```

## Start inserting process

## Verifying