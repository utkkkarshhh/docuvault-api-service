from django.contrib.auth.hashers import make_password
from django.db import transaction
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from service.constants import (DocumentConstants, ExceptionMessages,
                               ResponseMessages)
from service.exceptions import BadRequestException
from service.models import UserActiveToken, UserLimit, Users
from service.utils import JWT, ResponseHandler, logger


class GoogleOAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get("id_token")
        if not token:
            raise BadRequestException(ExceptionMessages.INVALID_ID_TOKEN)

        try:
            id_info = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                request.data.get("client_id")
            )
        except Exception as e:
            logger.exception(ExceptionMessages.INVALID_ID_TOKEN)
            raise BadRequestException(ExceptionMessages.INVALID_ID_TOKEN)

        email = id_info.get("email")
        first_name = id_info.get("given_name", "")
        last_name = id_info.get("family_name", "")
        # picture = id_info.get("picture", "")
        username = email.split("@")[0]

        if not email:
            raise BadRequestException(ExceptionMessages.EMAIL_REQUIRED)

        try:
            user = Users.objects.filter(email=email).first()

            if not user:
                user = self._create_user(email, username, first_name, last_name)

            if user.is_deleted:
                raise BadRequestException(ExceptionMessages.ACCOUNT_WAS_DELETED)

            user_object = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }

            user_payload = self._generate_token_payload(user)
            token = self._generate_jwt(user_payload)
            self._save_token(user, token)

            response_data = {
                "user": user_object,
                "token": token
            }

            return ResponseHandler(
                status=status.HTTP_200_OK,
                success=True,
                message=ResponseMessages.SIGN_IN_SUCCESSFUL,
                **response_data
            )

        except Exception as e:
            logger.exception(f"{ExceptionMessages.ERROR_WHILE_CREATING_USER}: {e}")
            raise BadRequestException(f"{ExceptionMessages.ERROR_WHILE_CREATING_USER}: {e}")

    def _create_user(self, email, username, first_name, last_name):
        with transaction.atomic():
            user = Users.objects.create(
                username=username,
                email=email,
                password=make_password(None),
                name=f'{first_name} {last_name}',
                is_o_auth=True
            )

            UserLimit.objects.create(
                upload_limit_count=DocumentConstants.DEFAULT_UPLOAD_LIMIT,
                user=user
            )
            return user

    def _generate_token_payload(self, user):
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }

    def _generate_jwt(self, user_payload):
        return JWT.create_jwt(user_payload)

    def _save_token(self, user, token):
        UserActiveToken.objects.create(
            user=user,
            token=token,
            is_active=True
        )
