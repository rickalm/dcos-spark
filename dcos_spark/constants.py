version = '0.4.0'
"""DCOS Spark version"""

spark_version = "spark-1.5.0-bin-2.4.0-28fb11ce902ca"

spark_executor_uri = (
    "http://downloads.mesosphere.com.s3.amazonaws.com/assets/spark/" +
    spark_version +
    ".tgz")

PATH_ENV = 'PATH'

spark_mesos_image = "mesosphere/spark:1.5.0-hadoop2.4-28fb11ce902ca"
