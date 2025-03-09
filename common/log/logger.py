import json
import logging.config
import os


def init(config_file: str):
    log_dir = "/app/logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(config_file, 'r') as config_file:
        print("load logger config")
        log_config = json.load(config_file)
    logging.config.dictConfig(log_config)
