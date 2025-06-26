from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from service.constants import (Constants, ExceptionMessages, OTPConstants,
                               ResponseMessages)
from service.exceptions import BadRequestException
from service.models import UserOTP, Users
from service.serializers import ForgetPasswordSerializer
from service.utils import (CommonUtils, EmailService, ResponseHandler,
                           generate_otp)


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error_message = CommonUtils.handle_serializer_error(serializer.errors)
            raise BadRequestException(error_message)
    
        validated_data = serializer.validated_data
        identifier_value = validated_data.get("identifier")

        user, identifier_type = self._get_user_object_and_identifier_type(identifier_value)
        otp = self._create_otp(user)

        EmailService(
            subject="Your Password Reset OTP",
            to=[user.email],
            template_name="reset_password.html",
            context={
                "user": user,
                "otp": otp
            }
        ).send()

        return ResponseHandler(
            status=status.HTTP_200_OK,
            success=True,
            message=ResponseMessages.OTP_SENT_SUCCESSFULLY,
        )

    def _get_user_object_and_identifier_type(self, identifier):
        user = Users.objects.filter(username=identifier).first()
        if not user:
            user = Users.objects.filter(email=identifier).first()
            if not user:
                raise BadRequestException(ExceptionMessages.USER_DOES_NOT_EXIST)
            identifier_type = "email"
        else:
            identifier_type = "username"

        if user.is_o_auth:
            raise BadRequestException(ExceptionMessages.NOT_ALLOWED_FOR_OAUTH_USER.format('Password'))

        return user, identifier_type
    
    def _recent_otp_verification(self, user):
        recent_otp = (
            UserOTP.objects.filter(user_id=user.id)
            .order_by('-created_at')
            .first()
        )

        if recent_otp:
            time_difference = timezone.now() - recent_otp.created_at
            if time_difference.total_seconds() < int(OTPConstants.RESET_PASSWORD_OTP_WAIT_TIME):
                raise BadRequestException(ExceptionMessages.OTP_ALREADY_SENT_PLEASE_WAIT)
            
    def _save_otp(self, otp, user_id):
        expires_at = timezone.now() + timedelta(minutes=OTPConstants.RESET_PASSWORD_OTP_EXPIRY_MINUTES)
        UserOTP.objects.create(
            otp=otp,
            expires_at=expires_at,
            user_id=user_id,
            type=OTPConstants.OTP_TYPES.get('PASSWORD_RESET')
        )

    def _create_otp(self, user):
        self._recent_otp_verification(user)
        otp = generate_otp(user.id)
        self._save_otp(otp, user.id)
        return otp
