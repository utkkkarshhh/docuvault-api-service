from rest_framework import serializers


class SignInUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()

class SignInSerializer(serializers.Serializer):
    identifier = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    user = SignInUserSerializer(read_only=True)
    token = serializers.CharField(read_only=True)
