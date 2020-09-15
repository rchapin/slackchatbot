#!/bin/bash

export TWINE_DEV_REPO=pypi-dev
export TWINE_RELEASE_REPO=pypi-release
export PYPI_HOST=nexus.dmz-svcs.mootley.local
export PYPI_REPO_BASE=https://nexus.dmz-svcs.mootley.local:8443/repository
export PYPI_DEV_INDEX_URL=${PYPI_REPO_BASE}/pypi-dev/simple
export PYPI_RELEASE_INDEX_URL=${PYPI_REPO_BASE}/pypi-release/simple

export DOCKER_HOST=nexus.dmz-svcs.mootley.local
export DOCKER_DEV_REPO=${DOCKER_HOST}:8446
export DOCKER_RELEASE_REPO=${DOCKER_HOST}:8445

