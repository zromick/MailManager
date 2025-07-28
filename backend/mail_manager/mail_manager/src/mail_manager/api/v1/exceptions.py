from functools import wraps
from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class MailItemNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="Mail item not found")


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.UNAUTHORIZED, detail="User is not authorized")


class InvalidMailItemReferenceException(HTTPException):
    def __init__(self, mail_item_uuid=None):
        detail = "Invalid mail item reference"
        if mail_item_uuid:
            detail = f"Referenced mail item {mail_item_uuid} does not exist"
        super().__init__(status_code=HTTPStatus.BAD_REQUEST, detail=detail)


def setup_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exception: HTTPException):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": exception.detail},
        )


def handle_mail_item_not_found(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MailItemNotFoundException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
    return wrapper


def handle_unauthorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UnauthorizedException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
    return wrapper


def handle_invalid_mail_item_reference(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidMailItemReferenceException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))
    return wrapper
