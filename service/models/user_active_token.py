from service.models import BaseModel, Users

from django.db import models

class UserActiveToken(BaseModel):
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    token = models.CharField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_active_tokens'
