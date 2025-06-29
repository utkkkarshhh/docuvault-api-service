from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from service.constants import ExceptionMessages, ResponseMessages
from service.exceptions import BadRequestException
from service.models import Users
from service.serializers import UpdatePasswordSerializer
from service.utils import CommonUtils, ResponseHandler, get_token_data


class UpdateUserPasswordView(APIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, user_id):
        return Users.objects.filter(id=user_id, is_deleted=False)
    
    def patch(self, request, *args, **kwargs):
        token_data = get_token_data(request)
        user_id = token_data.get('user_id')

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            errors = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(errors)

        validated_data = serializer.validated_data
        user_object = self.get_queryset(user_id)
        if not user_object.exists():
            raise BadRequestException(ExceptionMessages.USER_NOT_FOUND)
        user = user_object.first()
        self._check_if_o_auth_user(user)
        is_updated = self._update_user_password(user, validated_data)
        if not is_updated:
            return ResponseHandler(
                success=False,
                message=ResponseMessages.PASSWORD_NOT_UPDATED,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return ResponseHandler(
            success=True,
            message=ResponseMessages.PASSWORD_UPDATED_SUCCESSFULLY,
            status=status.HTTP_202_ACCEPTED
        )
        
    def _update_user_password(self, user, validated_data):
        current_password = validated_data.get('current_password')
        new_password = validated_data.get('new_password')
        confirm_new_password = validated_data.get('confirm_new_password')

        if not check_password(current_password, user.password):
            raise BadRequestException(ExceptionMessages.INCORRECT_PASSWORD)

        if new_password != confirm_new_password:
            raise BadRequestException(ExceptionMessages.NEW_AND_CONFIRM_PASS_NOT_MATCH)
        
        if check_password(confirm_new_password, user.password):
            raise BadRequestException(ExceptionMessages.NEW_PASS_CANT_BE_EXISTING)

        user.password = make_password(new_password)
        user.save()
        return 1

    def _check_if_o_auth_user(self, user):
        if user.is_o_auth is True:
            raise BadRequestException(ExceptionMessages.NOT_ALLOWED_FOR_OAUTH_USER.format('Password'))