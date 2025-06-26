import os

class Constants:
    pass
class DocumentConstants:
    DEFAULT_UPLOAD_LIMIT = 6

class AuthConstants:
    SIGNUP_TOKEN = os.getenv('SIGNUP_TOKEN', None)

class DocumentServiceEndpoints:
    DOCUMENT_SERVICE_BASE_URL = os.getenv('DOCUMENT_SERVICE_BASE_URL', '')
    
    # Endpoints
    DOCUMENT_CATEGORIES_MASTER = f'{DOCUMENT_SERVICE_BASE_URL}/api/v1/Doc/DocumentCategories'
    UPLOAD_DOCUMENT = f'{DOCUMENT_SERVICE_BASE_URL}/api/v1/Doc/UploadDocument'
    DOWNLOAD_DOCUMENT = f'{DOCUMENT_SERVICE_BASE_URL}/api/v1/Doc/DownloadDocument'
    DELETE_DOCUMENT = f'{DOCUMENT_SERVICE_BASE_URL}/api/v1/Doc/DeleteDocument'
    DELETE_ALL_DOCUMENTS = f'{DOCUMENT_SERVICE_BASE_URL}/api/v1/Doc/DeleteAllDocument/{{user_id}}'
    DOCUMENT_LISTING = f'{DOCUMENT_SERVICE_BASE_URL}/api/v1/Doc/DocumentList/{{user_id}}'
    CONVERT_DOCUMENT = f'{DOCUMENT_SERVICE_BASE_URL}/api/v1/Doc/ConvertDocument'
    
class OTPConstants:
    RESET_PASSWORD_OTP_WAIT_TIME = os.getenv('RESET_PASSWORD_OTP_WAIT_TIME')
    RESET_PASSWORD_OTP_EXPIRY_MINUTES = 3

    OTP_TYPES = {
        "PASSWORD_RESET": "password_reset"
    }
