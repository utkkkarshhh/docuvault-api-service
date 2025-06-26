from rest_framework import serializers


class ForgetPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
