from service.models import BaseModel, Users

from django.db import models

class UserLimit(BaseModel):
    upload_limit_count = models.IntegerField(null=False, default=6)
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_limit'
