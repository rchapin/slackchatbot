#!/bin/bash

set -e
set -u

source slackchatbot-envs.sh

###############################################################################
# A example of how to use getopt to parse command line options.
#
# name:     getopt-example.sh
# author:   Ryan Chapin
# created:  2014-11-11
################################################################################
# USAGE:

function about {
   cat << EOF
build.sh - Builds the slackchatbot python module and docker image
EOF
}

function usage {
   cat << EOF
Usage: build.sh [-vh] --version --build-type

  --version
    The version of the python module and docker image

  --build-type [dev|release]
    Whether the build is a dev build and will be pushed to the development
    pypi repo and docker repo or the release repos.

Options:
  -h help
      Outputs this basic usage information.

  -v verbose
      Output additional feedback/information during runtime.

  --more-help
      Extended help and documentation.
EOF
}

function ddt {
  if [ "$VERBOSE" -eq 1 ];
    then
    echo "$1"
  fi
}

function check_for_help {
  if [ "$MORE_HELP" -eq 1 ];
  then
    about
    usage
    echo ""
    extended_usage
    exit
  fi
  
  if [ "$HELP" -eq 1 ];
  then
    usage
    exit
  fi
}

function validate_args {

  if [ "$VERSION" == "0" ];
  then
    >&2 echo "ERROR: you must specify a --version"
    usage
    exit 1
  fi

  if [ "$BUILD_TYPE" == "0" ];
  then
    >&2 echo "ERROR: you must specify a --build-type [dev|release]"
    usage
    exit 1
  fi
  if [ "$BUILD_TYPE" != "dev" ] && [ "$BUILD_TYPE" != "release" ]
  then
    >&2 echo "ERROR: --build-type must be [dev|release]"
    usage
    exit 1
  fi
}

function get_twine_repo {
  if [ "$BUILD_TYPE" == "dev" ]
  then
    echo $TWINE_DEV_REPO
  else
    echo $TWINE_RELEASE_REPO
  fi
}

function get_pypi_index_url {
  if [ "$BUILD_TYPE" == "dev" ]
  then
    echo $PYPI_DEV_INDEX_URL
  else
    echo $PYPI_RELEASE_INDEX_URL
  fi
}

function get_docker_tag {
  local version=$1
  local build_type=$2
  if [ "$build_type" == "dev" ]
  then
    echo $(git rev-parse HEAD | cut -c 1-10)-${version}
  else
    echo $version
  fi
}

function get_docker_repo {
  if [ "$BUILD_TYPE" == "dev" ]
  then
    echo $DOCKER_DEV_REPO
  else
    echo $TWINE_RELEASE_REPO
    echo $DOCKER_RELEASE_REPO
  fi
}

#
# Build the python module and upload to nexus
#
function build_python_module {
  local version=$1
  local pypi_repo=$2
  local start_dir=`pwd`
  ddt "Building python module version=$version, uploading to pypi_index=$pypi_repo"
  cd slackchatbot
  python setup.py clean
  python setup.py sdist
  twine upload --verbose --repository $pypi_repo dist/slackchatbot-${version}.tar.gz
  cd $start_dir
}

#
# Build and push the docker container
#
function build_docker_image {
  local slackchatbot_version=$1
  local pypi_index_url=$2
  local image_tag=$3
  local docker_repo=$4
  ddt "Building docker image with slackchatbot_version=$slackchatbot_version, pypi_index_url=$pypi_index_url, image_tag=$image_tag, and docker_repo=$docker_repo"
  local start_dir=`pwd`
  cd docker

  echo "docker build --build-arg SLACKCHATBOT_VERSION=$slackchatbot_version --build-arg PYPI_INDEX_URL=$pypi_index_url --build-arg PYPI_HOST=$PYPI_HOST --tag slackchatbot:${image_tag} ."
  docker build --build-arg SLACKCHATBOT_VERSION=$slackchatbot_version --build-arg PYPI_INDEX_URL=$pypi_index_url --build-arg PYPI_HOST=$PYPI_HOST --tag slackchatbot:${image_tag} .

  docker tag slackchatbot:${image_tag} $docker_repo/slackchatbot:${image_tag}
  docker push $docker_repo/slackchatbot:${image_tag}
  cd $start_dir
}


################################################################################
#
# Here we define variables to store the input from the command line arguments as
# well as define the default values.
#
VERSION=0
BUILD_TYPE=0
HELP=0
VERBOSE=0
MORE_HELP=0

PARSED_OPTIONS=`getopt -o hv -l version:,build-type: -- "$@"`

# Check to see if the getopts command failed
if [ $? -ne 0 ];
then
   echo "Failed to parse arguments"
   exit 1
fi

eval set -- "$PARSED_OPTIONS"

# Loop through all of the options with a case statement
while true; do
   case "$1" in
      -h)
         HELP=1
         shift
         ;;

      -v)
         VERBOSE=1
         shift
         ;;

      --version)
         VERSION=$2
         shift 2
         ;;

      --build-type)
         BUILD_TYPE=$2
         shift 2
         ;;

      --)
         shift
         break
         ;;
   esac
done

check_for_help
validate_args
ddt "Building with version=$VERSION build-type=$BUILD_TYPE"

twine_repo=$(get_twine_repo)
build_python_module $VERSION $twine_repo

pypi_index_url=$(get_pypi_index_url)
image_tag=$(get_docker_tag $VERSION $BUILD_TYPE)
docker_repo=$(get_docker_repo)
build_docker_image $VERSION $pypi_index_url $image_tag $docker_repo

