__all__ = [
    "HealthCheck",
    "SignUp",
    "SignIn",
    "GoogleOAuthView",
    "UserDetailsView",
    "UpdateUserDetailsView",
    "UpdateUserPasswordView",
    "DeleteUserView",
    "DocumentCategoryMaster",
    "UserDocumentsListView",
    "UploadDocumentView",
    "DeleteDocumentView",
    "DownloadDocumentView",
    "ForgetPasswordView",
    "VerifyOTPView",
    "ResetPasswordView",
]

# Generic Views
from service.views.healthcheck import HealthCheck

# Authentication Views
from service.views.authentication.sign_up import SignUp
from service.views.authentication.sign_in import SignIn
from service.views.authentication.google_oauth_view import GoogleOAuthView
from service.views.authentication.forget_password_view import ForgetPasswordView
from service.views.authentication.verify_otp_view import VerifyOTPView
from service.views.authentication.reset_password_view import ResetPasswordView

# User Views
from service.views.user.user_details_view import UserDetailsView
from service.views.user.update_user_details_view import UpdateUserDetailsView
from service.views.user.delete_user_view import DeleteUserView
from service.views.user.update_user_password_view import UpdateUserPasswordView

# Document Views
from service.views.documents.document_category_master import DocumentCategoryMaster
from service.views.documents.user_documents_list_view import UserDocumentsListView
from service.views.documents.upload_document_view import UploadDocumentView
from service.views.documents.delete_document_view import DeleteDocumentView
from service.views.documents.download_document_view import DownloadDocumentView
