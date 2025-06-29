from rest_framework import serializers

from service.constants import ExceptionMessages
from service.exceptions import BadRequestException


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    reset_password_token = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise BadRequestException(ExceptionMessages.PASSWORD_LENGTH_INVALID)
        return value

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_new_password'):
            raise BadRequestException(ExceptionMessages.NEW_AND_CONFIRM_PASS_NOT_MATCH)
        return data
