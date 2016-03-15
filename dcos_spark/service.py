from dcos import config, util


def app_id():
    try:
        return util.get_config()["spark.app_id"]
    except KeyError:
        return "spark"


def set_app_id(app_id):
    config.set_val("spark.app_id", app_id)
