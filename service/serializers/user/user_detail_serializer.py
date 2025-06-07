from rest_framework import serializers
from service.models import Users

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'name', 'bio', 'dob', 'is_subscribed_to_emails']
