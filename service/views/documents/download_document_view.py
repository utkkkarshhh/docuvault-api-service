from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.constants import (DocumentConstants, DocumentServiceEndpoints,
                               ExceptionMessages)
from service.exceptions import BadRequestException
from service.models import UserLimit, Users
from service.serializers import DownloadDocumentSerializer
from service.utils import (CommonUtils, HTTPClient, ResponseHandler,
                           get_token_data)



class DownloadDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DownloadDocumentSerializer
    
    def get_user(self, user_id):
        return Users.objects.filter(id=user_id).first()

    def get(self, request, *args, **kwargs):
        token_data = get_token_data(request)
        user_id = token_data.get('user_id')

        user = self.get_user(user_id)
        if not user:
            raise BadRequestException(ExceptionMessages.USER_DOES_NOT_EXIST)

        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            errors = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(errors)

        validated_data = serializer.validated_data
        
        data = {
            "user_id": user_id,
            **validated_data
        }
        
        response = HTTPClient.request(
            method='POST',
            url=DocumentServiceEndpoints.DOWNLOAD_DOCUMENT,
            json=data,  
            headers={"Content-Type": "application/json"}
        )
        response_data = response.json()
        
        return ResponseHandler(
            success=True,
            message = response_data.get('message'),
            data=response_data.get('data')
        )
