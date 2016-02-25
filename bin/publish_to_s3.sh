# required env vars
#   VERSION (e.g. 0.5.2)
#   S3_URL (e.g. s3://<bucket>/<path>)

set -e -x

make clean env
echo -e "version = '${VERSION}'\n" > dcos_spark/config.py
python setup.py bdist_wheel
aws s3 cp dist/*.whl "${S3_URL}"
