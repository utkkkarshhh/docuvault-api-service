from datetime import datetime

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.constants import ExceptionMessages, ResponseMessages
from service.exceptions import BadRequestException
from service.models import Users, UserActiveToken
from service.serializers import DeleteUserSerializer
from service.utils import CommonUtils, ResponseHandler, get_token_data, logger


class DeleteUserView(APIView):
    serializer_class = DeleteUserSerializer
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
        self._initiate_deletion(user, validated_data)
        
        return ResponseHandler(
            status=status.HTTP_200_OK,
            success=True,
            message=ResponseMessages.USER_DELETED_SUCCESSFULLY
        )
        
    def _initiate_deletion(self, user, validated_data):
        with transaction.atomic():
            try:
                self._delete_user(user, validated_data)
                self._delete_all_active_token(user)
            except Exception as e:
                logger.exception(ExceptionMessages.ERROR_WHILE_DELETING.format(e))
                raise BadRequestException(ExceptionMessages.ERROR_WHILE_DELETING.format(e))
        
    def _delete_user(self, user, validated_data):
        reason_for_deletion = validated_data.get('reason_for_deletion')
        user.is_deleted = True
        user.reason_for_deletion = reason_for_deletion
        user.deleted_at = datetime.now()
        user.save()

    def _delete_all_active_token(self, user):
        UserActiveToken.objects.filter(user_id=user.id).delete()
