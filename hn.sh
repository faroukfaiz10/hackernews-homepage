#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

source $BASEDIR/.venv/bin/activate
python $BASEDIR/src/main.py | tee ~/.hn/$(date +%F_%T).txt