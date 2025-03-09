import logging
import uuid


class RequestIDFilter(logging.Filter):
    def __init__(self, request_id: uuid.UUID):
        super().__init__()
        self.request_id = str(request_id)

    def filter(self, record):
        record.request_id = self.request_id
        return True
