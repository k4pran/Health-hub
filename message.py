from enum import Enum
import uuid


class Format(Enum):
    UNKNOWN = "unknown"
    PD_DATAFRAME = "dataframe"
    PD_SEQUENCE = "sequence"


class Request:

    def __init__(self, subject, request_msg, identifier, **additional_info):
        self.subject = subject
        self.request_msg = request_msg
        self.identifier = identifier
        self.additional_info = additional_info


class Response:

    def __init__(self, subject, data, identifier=None, fmt=Format.UNKNOWN):
        self.subject = subject
        self.identifier = identifier
        self.data = data
        self.fmt = fmt

        if not identifier:
            self.identifier = uuid.uuid4()
