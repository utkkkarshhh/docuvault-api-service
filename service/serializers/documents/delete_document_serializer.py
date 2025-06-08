from rest_framework import serializers


class DeleteDocumentSerializer(serializers.Serializer):
    document_id = serializers.IntegerField(required=True)
