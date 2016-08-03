#!/bin/bash

# env vars
#   VERSION (e.g. 0.5.19)

set -ex -o pipefail

GIT_BRANCH=${GIT_BRANCH:-$(git name-rev --tags --name-only $(git rev-parse HEAD) | sed -e 's/\^[0-9]$//')}
GIT_BRANCH=${GIT_BRANCH/undefined/SNAPSHOT}
export VERSION="${VERSION:-${GIT_BRANCH#refs/tags/}}"
echo -e "version = '${VERSION}'" > dcos_spark/version.py
