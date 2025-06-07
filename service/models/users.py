from django.db import models

from service.models import BaseModel

class Users(BaseModel):
    username = models.CharField(max_length=55, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True) 
    is_subscribed_to_emails = models.BooleanField(null=True, default=True)
    is_deleted = models.BooleanField(null=True, default=False)
    reason_for_deletion = models.CharField(max_length=255, null=True, blank=True) 
    deleted_at = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'users'

    @property
    def is_authenticated(self):
        return getattr(self, '_is_authenticated', False)
