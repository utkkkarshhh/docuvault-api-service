import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from service.constants import ExceptionMessages
from service.exceptions import UnauthorizedException
from service.models import UserActiveToken, Users


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(ExceptionMessages.TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(ExceptionMessages.TOKEN_INVALID)

        try:
            user = Users.objects.get(id=payload['user_id'])
        except Users.DoesNotExist:
            raise AuthenticationFailed(ExceptionMessages.USER_DOES_NOT_EXIST)

        if not UserActiveToken.objects.filter(user=user, token=token, is_active=True).exists():
            raise AuthenticationFailed(ExceptionMessages.TOKEN_NOT_ACTIVE_INVALID)

        request.token_payload = payload
        user._is_authenticated = True
        return (user, token)
