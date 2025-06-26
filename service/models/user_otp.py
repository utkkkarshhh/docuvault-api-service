from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from service.models import BaseModel, Users

OTP_TYPE_CHOICES = (
    ('password_reset', 'Password Reset'),
)

class UserOTP(BaseModel):
    otp = models.IntegerField(
        validators=[
            MinValueValidator(100000),
            MaxValueValidator(999999)
        ],
        null=False
    )
    expires_at = models.DateTimeField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='otps')
    is_used = models.BooleanField(default=False)
    type = models.CharField(max_length=32, choices=OTP_TYPE_CHOICES, null=True)

    class Meta:
        db_table = 'user_otp'

    def __str__(self):
        return f"{self.user.email} - {self.type} - OTP: {self.otp}"
