import sys

version = sys.argv[1].replace('-', '_')
spark_version = sys.argv[2]
spark_mesos_image = sys.argv[3]

contents = """version = '{0}'
spark_version = '{1}'
spark_mesos_image = '{2}'
""".format(
    version,
    spark_version,
    spark_mesos_image)

with open('dcos_spark/config.py', 'w') as f:
    f.write(contents)
