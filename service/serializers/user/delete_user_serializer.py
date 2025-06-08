from rest_framework import serializers

class DeleteUserSerializer(serializers.Serializer):
    reason_for_deletion = serializers.CharField(required=True)
