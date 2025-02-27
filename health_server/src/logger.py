import json
import logging.config
import os
import uuid

log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)
with open('logger.json', 'r') as config_file:
    print("load logger config")
    log_config = json.load(config_file)
logging.config.dictConfig(log_config)


class RequestIDFilter(logging.Filter):
    def __init__(self, request_id: uuid.UUID):
        super().__init__()
        self.request_id = str(request_id)

    def filter(self, record):
        record.request_id = self.request_id
        return True
