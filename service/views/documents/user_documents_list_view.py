from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.constants import DocumentServiceEndpoints, ExceptionMessages
from service.exceptions import BadRequestException
from service.models import Users
from service.utils import HTTPClient, ResponseHandler, get_token_data


class UserDocumentsListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, user_id):
        return Users.objects.filter(id=user_id).first()
    
    def get(self, request, *args, **kwargs):
        token_data = get_token_data(request)
        user_id = token_data.get('user_id')
        user = self.get_queryset(user_id=user_id)
        if not user:
            raise BadRequestException(ExceptionMessages.USER_DOES_NOT_EXIST)
        response = HTTPClient.request(
            method='GET',
            url=DocumentServiceEndpoints.DOCUMENT_LISTING.format(user_id=user_id)
        )
        response_data = response.json()
        return ResponseHandler(
            success=True,
            message=response_data.get('message'),
            data=response_data.get('data')
        )
