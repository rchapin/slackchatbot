#!/bin/bash

export SCB_TWINE_DEV_REPO=pypi-dev
export SCB_TWINE_RELEASE_REPO=pypi-release
export SCB_PYPI_HOST=nexus.dmz-svcs.mootley.local
export SCB_PYPI_REPO_BASE=https://nexus.dmz-svcs.mootley.local:8443/repository
export SCB_PYPI_DEV_INDEX_URL=${SCB_PYPI_REPO_BASE}/pypi-dev/simple
export SCB_PYPI_RELEASE_INDEX_URL=${SCB_PYPI_REPO_BASE}/pypi-release/simple

export SCB_DOCKER_REPO_HOST=nexus.dmz-svcs.mootley.local
export SCB_DOCKER_DEV_REPO=${SCB_DOCKER_REPO_HOST}:8446
export SCB_DOCKER_RELEASE_REPO=${SCB_DOCKER_REPO_HOST}:8445

