import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from service.constants import ExceptionMessages, ResponseMessages
from service.exceptions import BadRequestException
from service.models import Users
from service.serializers import ResetPasswordSerializer
from service.utils import CommonUtils, ResponseHandler


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error_message = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(error_message)
        validated_data = serializer.validated_data

        new_password = validated_data.get('new_password')
        confirm_new_password = validated_data.get('confirm_new_password')
        reset_password_token = validated_data.get('reset_password_token')

        user = self.validate_jwt_and_get_user(reset_password_token)
        self.validate_passwords(user, new_password, confirm_new_password)
        user.password = make_password(new_password)
        user.save()
        
        return ResponseHandler(
            status=status.HTTP_200_OK,
            success=True,
            message=ResponseMessages.PASSWORD_UPDATED_SUCCESSFULLY
        )

    def validate_jwt_and_get_user(self, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            if payload.get("purpose") != "password_reset":
                raise AuthenticationFailed(ExceptionMessages.TOKEN_INVALID)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(ExceptionMessages.TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(ExceptionMessages.TOKEN_INVALID)
        try:
            user = Users.objects.get(id=payload['user_id'])
        except Users.DoesNotExist:
            raise AuthenticationFailed(ExceptionMessages.USER_DOES_NOT_EXIST)
        return user

    def validate_passwords(self, user, new_password, confirm_new_password):
        if new_password != confirm_new_password:
            raise BadRequestException(ExceptionMessages.NEW_AND_CONFIRM_PASS_NOT_MATCH)

        if check_password(new_password, user.password):
            raise BadRequestException(ExceptionMessages.NEW_PASS_CANT_BE_EXISTING)
