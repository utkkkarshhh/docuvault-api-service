from rest_framework import serializers


class UpdateUserDetailSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    dob = serializers.DateField(required=False)
    is_subscribed_to_emails = serializers.BooleanField(required=False)
