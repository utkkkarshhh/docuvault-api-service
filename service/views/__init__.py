__all__ = [
    "HealthCheck",
    "SignUp",
    "SignIn",
    "UserDetailsView",
    "UpdateUserDetailsView",
    "UpdateUserPasswordView",
    "DeleteUserView",
    "DocumentCategoryMaster",
    "UserDocumentsListView",
    "UploadDocumentView",
    "DeleteDocumentView",
    "DownloadDocumentView",
]

# Generic Views
from service.views.healthcheck import HealthCheck

# Authentication Views
from service.views.authentication.sign_up import SignUp
from service.views.authentication.sign_in import SignIn

# User Views
from service.views.user.user_details_view import UserDetailsView
from service.views.user.update_user_details_view import UpdateUserDetailsView
from service.views.user.update_user_password_view import UpdateUserPasswordView
from service.views.user.delete_user_view import DeleteUserView

# Documents
from service.views.documents.document_category_master import DocumentCategoryMaster
from service.views.documents.user_documents_list_view import UserDocumentsListView
from service.views.documents.upload_document_view import UploadDocumentView
from service.views.documents.delete_document_view import DeleteDocumentView
from service.views.documents.download_document_view import DownloadDocumentView
