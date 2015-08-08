version = '0.2.0'
"""DCOS Spark version"""

spark_version = "spark-1.4.1-bin-2.2.0"

spark_executor_uri = (
    "http://downloads.mesosphere.com.s3.amazonaws.com/assets/spark/" +
    spark_version +
    ".tgz")

PATH_ENV = 'PATH'

spark_mesos_image = "mesosphere/spark:1.4.0-rc4-hdfs"
