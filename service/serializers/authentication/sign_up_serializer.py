from rest_framework import serializers

from service.constants import AuthConstants, ExceptionMessages
from service.exceptions import BadRequestException


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=55)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30, write_only=True, style={'input_type': 'password'})
    token = serializers.CharField()

    def validate_password(self, value):
        if len(value) < 8:
            raise BadRequestException(ExceptionMessages.PASSWORD_LENGTH_INVALID)
        return value

    def validate_token(self, value):
        if AuthConstants.SIGNUP_TOKEN != value:
            raise BadRequestException(ExceptionMessages.INVALID_REGISTRATION_TOKEN)
        return value
