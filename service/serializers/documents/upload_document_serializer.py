import os

from rest_framework import serializers


class UploadDocumentSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    file = serializers.FileField(required=True)
    type = serializers.IntegerField(required=True)
