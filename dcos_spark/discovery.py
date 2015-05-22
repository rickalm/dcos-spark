from __future__ import print_function

import os
import sys

import requests
import toml

from dcos import marathon

def get_spark_tasks():
    client = marathon.create_client()
    return client.get_tasks("spark")


def get_spark_webui():
    tasks = get_spark_tasks()

    if len(tasks) == 0:
        print("Spark cluster task is not running yet.")
        sys.exit(1)

    return "http://" + tasks[0]["host"] + ":" + str(tasks[0]["ports"][1])


def get_spark_dispatcher():
    dcos_spark_url = os.getenv("DCOS_SPARK_URL")
    if dcos_spark_url is not None:
        return dcos_spark_url

    tasks = get_spark_tasks()

    if len(tasks) == 0:
        print("Spark cluster task is not running yet.")
        sys.exit(1)

    return tasks[0]["host"] + ":" + str(tasks[0]["ports"][0])
