from rest_framework.response import Response
from rest_framework.views import exception_handler

from service.constants import HTTPStatusCodes
from service.utils import logger


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        logger.exception("Something went wrong")
        return Response(
            {
                "errors": ["Something went wrong"],
                "success": False
            },
            status=HTTPStatusCodes.INTERNAL_ERROR.value
        )
    if response.status_code not in HTTPStatusCodes.get_success_response_codes():
        error_response = reformat_error_response(response.data)
        result = {
            "errors": [error_response.get("detail")] if isinstance(error_response, dict) and error_response.get(
                "detail") else [error_response],
            "success": False
        }
        return Response(result, status=response.status_code)
    return response


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
