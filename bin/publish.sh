#!/bin/bash

# required env vars
#   VERSION (e.g. 0.5.2)
#   S3_URL (e.g. s3://<bucket>/<path>)

set -eux -o pipefail

export VERSION=${GIT_BRANCH#refs/tags/}
export S3_URL=s3://mgummelt-mesos/

echo -e "version = '${VERSION}'\n" > dcos_spark/version.py
make clean binary
aws s3 cp dist/dcos-spark "${S3_URL}"
