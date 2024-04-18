import logging.config
import os

import yaml


def read_logging_config(default_path="logging.yml", env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            logging_config = yaml.safe_load(f.read())
        return logging_config
    else:
        return None


def setup_logging(logging_config, default_level=logging.INFO):
    if logging_config:
        logging.config.dictConfig(logging_config)
    else:
        logging.basicConfig(level=default_level)


def rename_event_key(_, __, ed):
    ed["message"] = ed.pop("event")
    return ed


def add_log_prefix_keys(_, __, ed):
    new_ed = {}
    for key in ed.keys():
        new_key = str('log.' + key)
        new_ed[new_key] = ed[key]
    return new_ed


def add_log_meta_data(_, __, ed):
    ed["@metadata.doctype"] = "logs"
    ed["@metadata.teamname"] = "da"
    ed["@metadata.appname"] = "clifind"
    ed["log.appname"] = "clifind"
    ed["log.appversion"] = open('app/version.txt').readline().rstrip()
    return ed
