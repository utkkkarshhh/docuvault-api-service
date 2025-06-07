import logging
from urllib.parse import urlparse

import requests
from rest_framework import status

from service.constants import HTTPResponseMessages
from service.exceptions import ExceptionHandler, HTTPRequestException

logger = logging.getLogger()


class HTTPClient():
    @staticmethod
    def handle_exception_response(response):
        resp = response.json().get('errors')
        status_code = response.status_code
        exception_class = ExceptionHandler.STATUS_CODE_EXCEPTION_MAPPING.get(status_code)

        if exception_class:
            raise exception_class(resp)
        raise HTTPRequestException(f"{HTTPResponseMessages.STATUS_CODE_ERROR} {status_code}: {resp}")

    @classmethod
    def request(cls, method, url, params=None, data=None, headers=None, stream=False, **kwargs):
        try:
            url = urlparse(url)
            query = url.query
            if query != '':
                query = '?' + query
            
            response = requests.request(
                method,
                url.scheme + '://' + url.netloc + url.path + query,
                params=params,
                data=data,
                headers=headers,
                stream=stream,
                **kwargs
            )
        except Exception as exp:
            raise HTTPRequestException(HTTPResponseMessages.HTTP_REQUEST_ERROR)

        if not stream and response.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
            cls.handle_exception_response(response)

        return response
