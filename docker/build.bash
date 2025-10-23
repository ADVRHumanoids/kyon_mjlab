#!/bin/bash
set -e 

NETRC_CONTENT=$(cat ~/.netrc) docker buildx bake --allow=fs.read=.. -f bake.hcl "$@"
