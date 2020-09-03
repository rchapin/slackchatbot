#!/bin/bash

set -u
set -e

VERSION=$1

# Update the version in setup.py and the Dockerfile
docker_version="ENV VERSION $VERSION"
docker_version_cmd="sed -i 's/ENV VERSION.*/ENV VERSION $VERSION/' Dockerfile"
eval $docker_version_cmd



