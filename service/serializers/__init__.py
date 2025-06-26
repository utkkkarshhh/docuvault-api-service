__all__ = [
    'SignUpSerializer',
    'SignInSerializer',
    'UserDetailSerializer',
    'UpdateUserDetailSerializer',
    'UpdatePasswordSerializer',
    'DeleteUserSerializer',
    'UploadDocumentSerializer',
    'DeleteDocumentSerializer',
    'DownloadDocumentSerializer',
    'ForgetPasswordSerializer',
]

# Authentication Serializers
from service.serializers.authentication.sign_up_serializer import SignUpSerializer
from service.serializers.authentication.sign_in_serializer import SignInSerializer
from service.serializers.authentication.update_password_serializer import UpdatePasswordSerializer
from service.serializers.authentication.forget_password_serializer import ForgetPasswordSerializer

# User Serializers
from service.serializers.user.user_detail_serializer import UserDetailSerializer
from service.serializers.user.update_user_detail_serializer import UpdateUserDetailSerializer
from service.serializers.user.delete_user_serializer import DeleteUserSerializer

# Documents Serializers
from service.serializers.documents.upload_document_serializer import UploadDocumentSerializer
from service.serializers.documents.delete_document_serializer import DeleteDocumentSerializer
from service.serializers.documents.download_document_serializer import DownloadDocumentSerializer
