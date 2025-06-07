from service.constants import ExceptionMessages
from service.exceptions import BadRequestException


def get_token_data(request):
    token_data = getattr(request, 'token_payload', None)
    if not token_data:
        raise BadRequestException(ExceptionMessages.NO_TOKEN_DATA)
    return token_data
