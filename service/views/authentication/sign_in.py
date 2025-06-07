from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from service.constants import ExceptionMessages, ResponseMessages
from service.exceptions import BadRequestException
from service.models import UserActiveToken, Users
from service.serializers import SignInSerializer
from service.utils import JWT, CommonUtils, ResponseHandler


class SignIn(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignInSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error_message = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(error_message)
        validated_data = serializer.validated_data
        identifier = validated_data.get('identifier')
        password = validated_data.get('password')
        
        user, user_object = self._validate_login(identifier, password)
        user_payload = self._generate_token_payload(user)
        token = self._generate_jwt(user_payload)
        _ = self._save_token(user, token)
        response_data = {
            "user": user_object,
            "token": token
        }
        serialized_response = self.serializer_class(response_data)
        return ResponseHandler(
            status=status.HTTP_200_OK,
            success=True,
            message=ResponseMessages.SIGN_IN_SUCCESSFUL,
            **serialized_response.data
        )
        
    def _validate_login(self, identifier, password):
        user = Users.objects.filter(
            Q(username=identifier) | Q(email=identifier)
        ).first()
        if not user:
            raise BadRequestException(ExceptionMessages.INCORRECT_USERNAME_OR_EMAIL)
        self._check_password(user, password)
        user_object = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email 
        }
        return user, user_object

    def _check_password(self, user, password):
        is_valid = check_password(password, user.password)
        if not is_valid:
            raise BadRequestException(ExceptionMessages.INCORRECT_PASSWORD)
        return 1
    
    def _generate_token_payload(self, user):
        user_payload = {}
        user_payload['user_id'] = user.id
        user_payload['username'] = user.username
        user_payload['email'] = user.email
        return user_payload


    def _generate_jwt(self, user_payload):
        token = JWT.create_jwt(user_payload)
        return token

    def _save_token(seld, user, token):
        _ = UserActiveToken.objects.create(
            user=user,
            token=token,
            is_active = True
        )
