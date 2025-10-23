#!/bin/bash

SCRIPT_DIR=$(dirname -- "$(realpath -- "${BASH_SOURCE[0]}")")

python $SCRIPT_DIR/play.py Mjlab-Velocity-Flat-Iit-Kyon "$@"