#!/bin/bash

SCRIPT_DIR=$(dirname -- "$(realpath -- "${BASH_SOURCE[0]}")")

python $SCRIPT_DIR/train.py Mjlab-Velocity-Flat-Iit-Kyon --env.scene.num-envs 4096 "$@"