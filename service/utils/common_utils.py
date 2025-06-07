import logging
import os
from typing import Any, Dict, List, Union

from service.constants import ResponseMessages
from service.exceptions import BadRequestException

logger = logging.getLogger()

class CommonUtils:
    
    @classmethod
    def handle_serializer_error(cls, error_response: Dict) -> List[str]:
        formatted_errors = []
        cls.flatted_response(error_response, formatted_errors)
        return formatted_errors

    @classmethod
    def flatted_response(cls, errors:Union[Dict, List], formatted_errors: List[str]):
        if isinstance(errors, dict):
            for key, value in errors.items():
                if isinstance(value, list):
                    for error in value:
                        formatted_errors.append(f"Invalid or missing {key}")
                elif isinstance(value, dict):
                    cls.flatted_response(value, formatted_errors)
        elif isinstance(errors, list):
            for error in errors:
                cls.flatted_response(error, formatted_errors)

    @classmethod
    def get_value_from_config(cls, key: str, default: Any=None) -> str:
        config_value = os.environ.get(key, None)
        if config_value is None and default is not None:
            config_value = default
        cls.data_validations(config_value, key + "in config")
        return config_value

    @classmethod
    def data_validations(cls, data: Any, message: str):
        if data is None:
            raise BadRequestException(ResponseMessages.NOT_FOUND.value.format(message))
