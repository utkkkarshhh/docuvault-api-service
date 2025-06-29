from rest_framework import status
from rest_framework.views import APIView
from service.constants import ExceptionMessages
from service.exceptions import BadRequestException
from service.utils import CommonUtils, ResponseHandler

from service.serializers import ResetPasswordSerializer


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error_message = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(error_message)
        validated_data = serializer.validated_data

        