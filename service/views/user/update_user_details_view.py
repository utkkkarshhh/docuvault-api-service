from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.constants import ExceptionMessages, ResponseMessages
from service.exceptions import BadRequestException
from service.models import Users
from service.serializers import UpdateUserDetailSerializer
from service.utils import CommonUtils, ResponseHandler, get_token_data


class UpdateUserDetailsView(APIView):
    serializer_class = UpdateUserDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, user_id):
        return Users.objects.filter(id=user_id, is_deleted=False)
    
    def patch(self, request, *args, **kwargs):
        token_data = get_token_data(request)
        user_id = token_data.get("user_id")
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error_message = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(error_message)
        validated_data = serializer.validated_data
        
        user_object = self.get_queryset(user_id)
        if not user_object.exists():
            raise BadRequestException(ExceptionMessages.USER_NOT_FOUND)
        
        user = user_object.first()
        self.update_user_details(user, validated_data)
        
        return ResponseHandler(
            status=status.HTTP_202_ACCEPTED,
            success=True,
            message=ResponseMessages.USER_DETAILS_UPDATED
        )
        
    def update_user_details(self, user, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")

        if username and Users.objects.exclude(id=user.id).filter(username=username).exists():
            raise BadRequestException(ExceptionMessages.USERNAME_ALREADY_TAKEN)
        if email and Users.objects.exclude(id=user.id).filter(email=email).exists():
            raise BadRequestException(ExceptionMessages.EMAIL_ALREADY_REGISTERED)

        for key, value in validated_data.items():
            setattr(user, key, value)
        user.save()
