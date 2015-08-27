from __future__ import print_function

import os
import sys

import requests
import toml

from dcos import marathon, util

def check_dcos_config():
    if os.getenv("DCOS_CONFIG") is None:
        print("Please set the DCOS_CONFIG environment variable to your DCOS config file path, e.g: ~/.dcos/dcos.toml")
        sys.exit(1)

def get_spark_webui():
    check_dcos_config()
    base_url = util.get_config().get('core.dcos_url')
    return base_url + '/service/spark/'

def get_spark_dispatcher():
    check_dcos_config()
    dcos_spark_url = os.getenv("DCOS_SPARK_URL")
    if dcos_spark_url is not None:
        return dcos_spark_url

    base_url = util.get_config().get('core.dcos_url')
    # Remove http:// prefix.
    return base_url[7:] + '/service/sparkcli/'
