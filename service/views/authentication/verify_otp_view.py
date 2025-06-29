from django.db.models import Q
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView

from service.constants import ExceptionMessages, ResponseMessages
from service.exceptions import BadRequestException
from service.models import UserOTP, Users
from service.serializers import VerifyOTPSerializer
from service.utils import CommonUtils, ResponseHandler


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer

    def get_user_queryset(self, identifier):
        return Users.objects.filter(
            Q(username=identifier) | Q(email=identifier)
        ).first()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error_message = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(error_message)
        validated_data = serializer.validated_data

        identifier = validated_data.get('identifier')
        otp = validated_data.get('otp')
        otp_type = validated_data.get('otp_type')

        user_object = self.get_user_queryset(identifier)

        if not user_object:
            raise BadRequestException(ExceptionMessages.USER_NOT_FOUND)
        
        active_otp = self.get_active_otp(user_object, otp, otp_type)
        active_otp.is_used = True
        active_otp.save()

        return ResponseHandler(
            status=status.HTTP_200_OK,
            success=True,
            message=ResponseMessages.OTP_VERIFIED_SUCCESSFULLY
        )

    def get_active_otp(self, user_object, otp, otp_type):
        active_otp = UserOTP.objects.filter(
            user=user_object,
            otp=otp,
            type=otp_type,
        ).first()

        if not active_otp:
            raise BadRequestException(ExceptionMessages.INVALID_OTP)
        if active_otp.is_used == True:
            raise BadRequestException(ExceptionMessages.ALREADY_USED_OTP)
        if active_otp.expires_at < timezone.now():
            raise BadRequestException(ExceptionMessages.EXPIRED_OTP)
        return active_otp
