#!/bin/bash

NEXUS_DOMAIN=nexus.dmz-svcs.mootley.local
NEXUS_PORT=8445

set -u
set -e

VERSION=$1
START_DIR=`pwd`

echo "Bumping version to $VERSION"

#
# Update the version in setup.py and the Dockerfile
#
docker_version="ENV VERSION $VERSION"
docker_version_cmd="sed -i 's/ENV VERSION.*/ENV VERSION $VERSION/' Dockerfile"
eval $docker_version_cmd

setup_version="version='$VERSION',"
setup_version_cmd="sed -i \"s/version=.*/$setup_version/\" slackchatbot/setup.py"
eval $setup_version_cmd

#
# Build the python module and upload to nexus
#
cd slackchatbot
python setup.py clean
python setup.py sdist
twine upload --verbose --repository pypi-dev dist/slackchatbot-${VERSION}.tar.gz

#
# Build and push the docker container
#
cd $START_DIR
docker build --tag slackchatbot:${VERSION} .
docker tag slackchatbot:${VERSION} $NEXUS_DOMAIN:$NEXUS_PORT/slackchatbot:${VERSION}
docker push $NEXUS_DOMAIN:$NEXUS_PORT/slackchatbot:${VERSION}

cd $START_DIR

