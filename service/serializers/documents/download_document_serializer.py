from rest_framework import serializers


class DownloadDocumentSerializer(serializers.Serializer):
    document_id = serializers.IntegerField(required=True)
