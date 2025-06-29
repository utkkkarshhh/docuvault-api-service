from rest_framework import serializers

from service.constants import OTPConstants

class VerifyOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    otp = serializers.IntegerField(required=True)
    otp_type = serializers.ChoiceField(
        choices=list(OTPConstants.OTP_TYPES.values()),
        required=True
    )

    def validate_otp(self, value):
        if value < 100000 or value > 999999:
            raise serializers.ValidationError("OTP must be a 6-digit number.")
        return value
