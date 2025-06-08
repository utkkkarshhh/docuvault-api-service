from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.constants import DocumentServiceEndpoints
from service.utils import HTTPClient, ResponseHandler


class DocumentCategoryMaster(APIView):
    permission_classes = [IsAuthenticated]
        
    def get(self, request, *args, **kwargs):
        response = HTTPClient.request(
            method='GET',
            url=DocumentServiceEndpoints.DOCUMENT_CATEGORIES_MASTER
        )
        response_data = response.json()
        return ResponseHandler(
            success=True,
            data=response_data.get('data'),
            status=status.HTTP_200_OK
        )
