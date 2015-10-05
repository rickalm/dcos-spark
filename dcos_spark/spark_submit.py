from __future__ import print_function
import json
import os
import os.path
import re
import subprocess

import pkg_resources
from dcos_spark import constants

def partition(args, pred):
    ain = []
    aout = []
    for x in args:
        if pred(x):
            ain.append(x)
        else:
            aout.append(x)
    return (ain, aout)

def show_help():
    submit_file = pkg_resources.resource_filename(
        'dcos_spark',
        'data/' + constants.spark_version + '/bin/spark-submit')

    command = [submit_file, "--help"]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    for line in stderr.decode("utf-8").split("\n"):
        if line.startswith("Usage:"):
            continue
        print(line)

    return 0


def submit_job(master, args, docker_image, verbose = False):
    (props, args) = partition(args.split(" "), lambda a: a.startswith("-D"))
    props = props + ["-Dspark.mesos.executor.docker.image=" + docker_image]
    response = run(master, args, verbose, props)
    if response[0] is not None:
        print("Run job succeeded. Submission id: " +
              response[0]['submissionId'])
    return response[1]


def job_status(master, submissionId, verbose = False):
    response = run(master, ["--status", submissionId], verbose)
    if response[0] is not None:
        print("Submission ID: " + response[0]['submissionId'])
        print("Driver state: " + response[0]['driverState'])
        if 'message' in response[0]:
            print("Last status: " + response[0]['message'])
    elif response[1] == 0:
        print("Job id '" + submissionId + "' is not found")
    return response[1]


def kill_job(master, submissionId, verbose = False):
    response = run(master, ["--kill", submissionId], verbose)
    if response[0] is not None:
        if bool(response[0]['success']):
            success = "succeeded."
        else:
            success = "failed."
        print("Kill job " + success)
        print("Message: " + response[0]['message'])
    return response[1]


def which(program):
    """Returns the path to the named executable program.

    :param program: The program to locate:
    :type program: str
    :rtype: str
    """

    def is_exe(file_path):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    file_path, filename = os.path.split(program)
    if file_path:
        if is_exe(program):
            return program
    elif constants.PATH_ENV in os.environ:
        for path in os.environ[constants.PATH_ENV].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def check_java_version(java_path):
    process = subprocess.Popen(
        [java_path, "-version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    lines = stderr.decode('utf8').split(os.linesep)
    if len(lines) == 0:
        print("Unable to check java version, error: no output detected from " + java_path + " -version")
        return False

    match = re.search("1\.(\d+)", lines[0])
    if match and int(match.group(1)) < 7:
        print("DCOS Spark requires Java 1.7.x or greater to be installed, found " + lines[0])
        return False

    return True


def check_java():
    # Check if JAVA is in the PATH
    if which('java') is not None:
        return check_java_version('java')

    # Check if JAVA_HOME is set and find java
    java_home = os.environ.get('JAVA_HOME')

    if java_home is not None:
        java_path = os.path.join(java_home, "bin", "java")
        if os.path.isfile(java_path):
            return check_java_version(java_path)

    print("DCOS Spark requires Java 1.7.x to be installed, please install JRE")
    return False


def run(master, args, verbose, props = []):
    """
    This method runs spark_submit with the passed in parameters.
    ie: ./bin/spark-submit --deploy-mode cluster --class
    org.apache.spark.examples.SparkPi --master mesos://10.127.131.174:8077
    --executor-memory 1G --total-executor-cores 100 --driver-memory 1G
    http://10.127.131.174:8000/spark-examples_2.10-1.3.0-SNAPSHOT.jar 30
    """
    if not check_java():
        return (None, 1)

    submit_file = pkg_resources.resource_filename(
        'dcos_spark',
        'data/' + constants.spark_version + '/bin/spark-submit')

    command = [submit_file, "--deploy-mode", "cluster", "--master",
               "mesos://" + master] + args

    process = subprocess.Popen(
        command,
        env = dict(os.environ, **{"SPARK_JAVA_OPTS": ' '.join(props)}),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    if verbose is True:
        print("Ran command: " + " ".join(command))
        print("Stdout:")
        print(stdout)
        print("Stderr:")
        print(stderr)

    err = stderr.decode("utf-8")
    if process.returncode != 0:
        if "502 Bad Gateway" in err:
            print("Spark service is not found in your DCOS cluster.")
            return (None, process.returncode)

        if "500 Internal Server Error" in err:
            print("Error reaching Spark cluster endpoint. Please make sure Spark service is in running state in Marathon.")
            return (None, process.returncode)

        print("Spark submit failed:")
        print(stderr)
        return (None, process.returncode)
    else:
        if "{" in err:
            lines = err.split(os.linesep)
            jsonStr = ""
            startScan = False
            for l in lines:
                if l.startswith("}") and startScan:
                    jsonStr += l + os.linesep
                    startScan = False
                elif startScan:
                    jsonStr += l + os.linesep
                elif l.startswith("{"):
                    startScan = True
                    jsonStr += l + os.linesep

            response = json.loads(jsonStr)
            return (response, process.returncode)
        return (None, process.returncode)
