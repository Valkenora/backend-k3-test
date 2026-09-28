from rest_framework import serializers
from .models import HIRADocument, HIRAGroup, HIRAActivity


class HIRAActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HIRAActivity
        fields = [
            'id', 'group', 'activity_name', 'activity_type', 'activity_details',
            'initial_likelihood', 'initial_severity',
            'initial_score', 'initial_level', 'initial_acceptable',
            'residual_likelihood', 'residual_severity',
            'residual_score', 'residual_level', 'residual_acceptable',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'initial_score', 'initial_level', 'initial_acceptable',
            'residual_score', 'residual_level', 'residual_acceptable',
            'created_at', 'updated_at'
        ]


class HIRAGroupSerializer(serializers.ModelSerializer):
    activities = HIRAActivitySerializer(many=True, read_only=True)

    class Meta:
        model = HIRAGroup
        fields = ['id', 'hira_document', 'location_function', 'activities']


class HIRADocumentSerializer(serializers.ModelSerializer):
    groups = HIRAGroupSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    reviewed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = HIRADocument
        fields = [
            'id', 'project', 'document_number', 'work_package', 'work_area',
            'status', 'created_by', 'reviewed_by', 'reviewed_at',
            'remarks', 'created_at', 'updated_at', 'groups'
        ]
        read_only_fields = ['status', 'created_by', 'reviewed_by', 'reviewed_at', 'created_at', 'updated_at']