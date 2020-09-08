#!/bin/bash

NEXUS_DOMAIN=nexus.dmz-svcs.mootley.local
NEXUS_PORT=8445

set -u
set -e

version=$1
build=${2:-dev}
START_DIR=`pwd`

pypi_repo="pypi-${build}"
docker_tag=$version
if [ "$build" == "dev" ]
then
  docker_tag=$(git rev-parse HEAD)
elif [ "$build" == "release" ]
then
  docker_tag=$version
fi

#
# Build the python module and upload to nexus
#
cd slackchatbot
python setup.py clean
python setup.py sdist
twine upload --verbose --repository $pypi_repo dist/slackchatbot-${version}.tar.gz

#
# Build and push the docker container
#
cd $START_DIR
docker build --build-arg pypi_repo=$pypi_repo --build-arg version=$version \
--tag slackchatbot:${docker_tag} .
docker tag slackchatbot:${docker_tag} $NEXUS_DOMAIN:$NEXUS_PORT/slackchatbot:${docker_tag}
docker push $NEXUS_DOMAIN:$NEXUS_PORT/slackchatbot:${docker_tag}

cd $START_DIR
