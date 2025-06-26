import random
from datetime import datetime

from django.utils import timezone

from service.constants import OTPConstants
from service.models import UserOTP


def generate_otp(user_id):
    while True:
        otp = random.randint(100000, 999999)
        existing_otp = UserOTP.objects.filter(
            user_id=user_id,
            otp=otp,
            is_used=False,
            type=OTPConstants.OTP_TYPES.get('PASSWORD_RESET'),
            expires_at__gt=timezone.now()
        ).exists()

        if not existing_otp:
            return otp
