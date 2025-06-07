from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from service.constants import HTTPStatusCodes, ExceptionMessages
from service.exceptions import ExceptionHandler
from service.utils.logger import logger


def global_exception_handler(exc, context):
    response = exception_handler(exc, context)

    logger.exception(str(exc))
    if response is not None:
        exception_details = ExceptionHandler.EXCEPTION_MAP.get(type(exc))
        if exception_details:
            return Response(
                {"success": False, "message": exception_details["message"]},
                status=exception_details["status"],
            )

        error_response = reformat_error_response(response.data)
        if isinstance(error_response, dict) and error_response.get("detail"):
            errors =  [error_response.get("detail")]
        elif isinstance(error_response, list):
            errors = error_response
        else:
            errors = [error_response]
        return Response(
            {
                "errors": errors,
                "success": False,
            },
            status=response.status_code,
        )
    elif str(ExceptionMessages.DOES_NOT_EXIST) in str(exc):
        return Response(
            {"success": False, "message": ExceptionMessages.DATA_NOT_AVAILABLE},
            status=status.HTTP_404_NOT_FOUND,
        )
    else:
        return Response(
            {
                "errors": [ExceptionMessages.SOMETHING_WENT_WRONG],
                "success": False,
            },
            status=HTTPStatusCodes.INTERNAL_ERROR.value,
        )

def reformat_error_response(input_data):
    if isinstance(input_data, dict):
        result = {}
        for key, value in input_data.items():
            if isinstance(value, str):
                result = extract_cleaned_response(key, value, result)
            else:
                result[key] = reformat_error_response(value)
        return result
    elif isinstance(input_data, list):
        return [reformat_error_response(item) for item in input_data]
    else:
        return input_data


def extract_cleaned_response(key, value, result):
    start_index = value.find("[{'detail':")
    if start_index != -1:
        cleaned_response = value[start_index:].split("}],")[0]
        result = extract_detail_value(cleaned_response, result, key, value)
    else:
        result[key] = value
    return result


def extract_detail_value(cleaned_response, result, key, value):
    detail_key_index = cleaned_response.find("'detail': ")
    if detail_key_index != -1:
        detail_value = cleaned_response[detail_key_index + len("'detail': "):]
        result[key] = detail_value.strip(" '")
    else:
        result[key] = value

    return result
