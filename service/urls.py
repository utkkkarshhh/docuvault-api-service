from django.urls import path

from service.views import *

urlpatterns = [
    path('Healthcheck', HealthCheck.as_view(), name='healthcheck'),
    
    # Auth APIs
    path('SignUp', SignUp.as_view(), name='sign_up'),
    path('SignIn', SignIn.as_view(), name='sign_in'),
    
    # User APIs
    path('User/Details', UserDetailsView.as_view(), name='user_details'),
    path('User/Details/Update', UpdateUserDetailsView.as_view(), name="update_user_details"),
    path('User/Password/Update', UpdateUserPasswordView.as_view(), name="update_user_password"),
    path('User/Delete', DeleteUserView.as_view(), name="delete_user"),
    
    # Document APIs
    path('Documents/CategoryMaster', DocumentCategoryMaster.as_view(), name="documents_category_master"),
    path('Documents/DocumentsList', UserDocumentsListView.as_view(), name="user_documents_list"),
    path('Documents/UploadDocument', UploadDocumentView.as_view(), name="upload_user_ddocument"),
    path('Documents/DeleteDocument', DeleteDocumentView.as_view(), name="delete_user_ddocument"),
    path('Documents/DownloadDocument', DownloadDocumentView.as_view(), name="download_user_ddocument"),
]
