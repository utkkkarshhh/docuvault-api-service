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
    
    def generate_reset_token(user_id):
        payload = {
            "user_id": user_id,
            "purpose": "password_reset",
            "exp": datetime.utcnow() + timedelta(minutes=1),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
