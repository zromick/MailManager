from functools import wraps
from http import HTTPStatus

import requests


class MailManagerClientException(Exception):
    def __init__(
        self,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        detail="An error occurred with the Mail Manager client",
    ):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class MailManagerNotFoundException(MailManagerClientException):
    def __init__(self, detail="Resource not found"):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)


def handle_mail_manager_not_found(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == HTTPStatus.NOT_FOUND:
                raise MailManagerNotFoundException(detail=f"Resource not found: {e}")
            raise

    return wrapper


def handle_http_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            raise MailManagerClientException(detail=f"HTTP error occurred: {e}")

    return wrapper


def handle_request_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            raise MailManagerClientException(detail=f"Request failed: {e}")

    return wrapper
