from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.constants import (DocumentConstants, DocumentServiceEndpoints,
                               ExceptionMessages)
from service.exceptions import BadRequestException
from service.models import UserLimit, Users
from service.serializers import UploadDocumentSerializer
from service.utils import (CommonUtils, HTTPClient, ResponseHandler,
                           get_token_data)


class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadDocumentSerializer

    def get_user(self, user_id):
        return Users.objects.filter(id=user_id).first()

    def post(self, request, *args, **kwargs):
        token_data = get_token_data(request)
        user_id = token_data.get('user_id')

        user = self.get_user(user_id)
        if not user:
            raise BadRequestException(ExceptionMessages.USER_DOES_NOT_EXIST)

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            errors = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(errors)

        user_limit, created = UserLimit.objects.get_or_create(
            user=user,
            defaults={'upload_limit_count': DocumentConstants.DEFAULT_UPLOAD_LIMIT}
        )
        if not created and user_limit.upload_limit_count <= 0:
            raise BadRequestException(ExceptionMessages.UPLOAD_LIMIT_EXCEEDED)

        validated_data = serializer.validated_data
        data = {
            "name": validated_data["name"],
            "description": validated_data["description"],
            "type": validated_data["type"],
            "user_id": user_id
        }

        files = {
            "file": request.FILES.get("file")
        }

        response = HTTPClient.request(
            method='POST',
            url=DocumentServiceEndpoints.UPLOAD_DOCUMENT,
            data=data,
            files=files
        )
        response_data = response.json()

        user_limit.upload_limit_count -= 1
        user_limit.save()

        return ResponseHandler(
            success=True,
            message=response_data.get('message'),
            data=response_data.get('data')
        )
