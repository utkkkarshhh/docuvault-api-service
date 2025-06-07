from datetime import datetime, timedelta

import jwt
from django.conf import settings


class JWT:
    @staticmethod
    def create_jwt(payload):
        payload = {
            **payload,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
        return token
