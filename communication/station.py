import pickle
import pandas as pd
from fuzzywuzzy import process

from communication.producer import producer
from function_registrar import procurable
from message import Request, Response, Format


confidence_threshold = 30


def handle_request(request: Request):
    result, confidence = select_method(request.request_msg)
    if confidence >= confidence_threshold:
        response = process_response(result['description'], result['function'](), request.identifier)
        producer.send('health-out', response)


def process_response(subject, data, identifier) -> Response:
    fmt = Format.UNKNOWN
    if type(data) == pd.Series:
        fmt = Format.PD_SEQUENCE

    elif type(data) == pd.DataFrame:
        fmt = Format.PD_DATAFRAME

    return pickle.dumps(Response(subject, data, identifier, fmt))


def select_method(command):
    method_name, confidence = process.extractOne(command, procurable.all.keys())
    result = procurable.all[method_name]
    return result, confidence
