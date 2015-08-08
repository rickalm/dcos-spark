#!/bin/bash -e

BASEDIR=`dirname $0`/..

if [ ! -d "$BASEDIR/env" ]; then
    virtualenv -q $BASEDIR/env --prompt='(dcos-spark) '
    echo "Virtualenv created."
fi

cd $BASEDIR
source $BASEDIR/env/bin/activate
echo "Virtualenv activated."

if [ ! -f "$BASEDIR/env/updated" -o $BASEDIR/setup.py -nt $BASEDIR/env/updated ]; then
    pip install -e $BASEDIR
    touch $BASEDIR/env/updated
    echo "Requirements installed."
fi

pip install -r $BASEDIR/requirements.txt

SPARK_VERSION=spark-1.4.1-bin-2.2.0

if [ ! -d "$BASEDIR/dcos_spark/data/$SPARK_VERSION" ]; then
    pushd .
    cd $BASEDIR/dcos_spark/data
    wget http://downloads.mesosphere.com.s3.amazonaws.com/assets/spark/$SPARK_VERSION.tgz
    tar xvf $SPARK_VERSION.tgz
    rm $SPARK_VERSION.tgz
    popd
fi
