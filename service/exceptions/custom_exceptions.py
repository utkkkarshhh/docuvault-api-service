from rest_framework import status

from service.exceptions import BaseException


class BadRequestException(BaseException):
    def __init__(self, detail, status_code=400):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)
        
class UnauthorizedException(BaseException):
    def __init__(self, detail, status_code=401):
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED)
        
class NotFoundException(BaseException):
    def __init__(self, detail):
        super().__init__(detail, status.HTTP_404_NOT_FOUND)
