from collections import defaultdict
from http import HTTPStatus

from fastapi import HTTPException


class CustomException(HTTPException):
    http_status_enum: HTTPStatus = HTTPStatus.BAD_GATEWAY

    def __init__(self, detail=None, error=None):

        self.status_code = self.http_status_enum.value
        self.error = error if error else self.http_status_enum.phrase
        self.detail = detail if detail else self.http_status_enum.description


class BadRequestException(CustomException):
    http_status_enum = HTTPStatus.BAD_REQUEST


def parsing_pydentic_errors(exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)
        reformatted_message[field_string].append(msg)
    return reformatted_message
