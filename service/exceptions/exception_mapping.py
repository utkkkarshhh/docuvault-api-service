from rest_framework import status
from rest_framework.exceptions import (AuthenticationFailed, MethodNotAllowed,
                                       NotAcceptable, NotAuthenticated,
                                       PermissionDenied, UnsupportedMediaType)

from service.constants import HTTPResponseMessages
from service.exceptions import (BadRequestException, NotFoundException,
                                UnauthorizedException)


class ExceptionHandler:

    AUTH_FAILED_EXCEPTIONS = (AuthenticationFailed, NotAuthenticated, PermissionDenied)
    METHOD_NOT_ALLOWED_EXCEPTION = MethodNotAllowed
    UNSUPPORTED_MEDIA_TYPE_EXCEPTION = UnsupportedMediaType
    NOT_ACCEPTABLE_EXCEPTION = NotAcceptable

    EXCEPTION_MAP = {
        AUTH_FAILED_EXCEPTIONS: {
            "status": status.HTTP_401_UNAUTHORIZED,
            "message": HTTPResponseMessages.AUTHENTICATION_ERROR,
        },
        METHOD_NOT_ALLOWED_EXCEPTION: {
            "status": status.HTTP_405_METHOD_NOT_ALLOWED,
            "message": HTTPResponseMessages.INVALID_METHOD,
        },
        UNSUPPORTED_MEDIA_TYPE_EXCEPTION: {
            "status": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "message": HTTPResponseMessages.UNSUPPORTED_DATA,
        },
        NOT_ACCEPTABLE_EXCEPTION: {
            "status": status.HTTP_406_NOT_ACCEPTABLE,
            "message": HTTPResponseMessages.UNACCEPTABLE_DATA,
        },
    }

    STATUS_CODE_EXCEPTION_MAPPING = {
        status.HTTP_400_BAD_REQUEST: BadRequestException,
        status.HTTP_404_NOT_FOUND: NotFoundException,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedException,
    }
