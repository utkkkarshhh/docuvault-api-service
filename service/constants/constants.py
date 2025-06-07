import os

class Constants:
    pass

class DocumentConstants:
    DEFAULT_UPLOAD_LIMIT = 6

class AuthConstants:
    SIGNUP_TOKEN = os.getenv('SIGNUP_TOKEN', None)
