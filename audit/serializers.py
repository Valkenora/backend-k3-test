from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    performed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'entity_type', 'entity_id', 'action', 'performed_by', 'timestamp', 'remarks']