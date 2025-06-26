from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from service.constants import (DocumentConstants, ExceptionMessages,
                               ResponseMessages)
from service.exceptions import BadRequestException
from service.models import UserLimit, Users
from service.serializers import SignUpSerializer
from service.utils import CommonUtils, ResponseHandler, logger


class SignUp(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            error_message = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(error_message)
        validated_data = serializer.validated_data
        
        self._validate_user_input(validated_data)
        self._create_user_and_user_limit(validated_data)

        return ResponseHandler(
            success=True,
            status=status.HTTP_201_CREATED,
            message=ResponseMessages.USER_CREATED_SUCCESSFULLY
        )
        
    def _validate_user_input(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')

        existing_user = Users.objects.filter(
            Q(username=username) | Q(email=email)
        ).first()

        if existing_user:
            if existing_user.is_o_auth == True:
                raise BadRequestException(ExceptionMessages.LOGIN_USING_GOOGLE)
            if existing_user.username == username:
                raise BadRequestException(ExceptionMessages.USERNAME_ALREADY_EXISTS)
            if existing_user.email == email:
                raise BadRequestException(ExceptionMessages.EMAIL_ALREADY_EXISTS)

    def _create_user_and_user_limit(self, validated_data):
        with transaction.atomic():
            try:
                user = Users.objects.create(
                    username=validated_data.get('username'),
                    email=validated_data.get('email'),
                    password=make_password(validated_data.get('password'))
                )

                user_limit = UserLimit.objects.create(
                    upload_limit_count = DocumentConstants.DEFAULT_UPLOAD_LIMIT,
                    user = user
                )
                
            except Exception as e:
                logger.exception(f'{ExceptionMessages.ERROR_WHILE_CREATING_USER} : {e}')
                raise BadRequestException(ExceptionMessages.ERROR_WHILE_CREATING_USER)
