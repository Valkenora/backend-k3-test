from rest_framework import serializers
from .models import WorkPermit
from hira.models import HIRAActivity


class WorkPermitSerializer(serializers.ModelSerializer):
    submitted_by = serializers.StringRelatedField(read_only=True)
    endorsed_by = serializers.StringRelatedField(read_only=True)
    approved_by = serializers.StringRelatedField(read_only=True)
    retracted_by = serializers.StringRelatedField(read_only=True)
    closed_by = serializers.StringRelatedField(read_only=True)

    # read only fields pulled from HIRA for context
    hira_activity_name = serializers.SerializerMethodField()
    hira_residual_score = serializers.SerializerMethodField()
    hira_residual_level = serializers.SerializerMethodField()

    class Meta:
        model = WorkPermit
        fields = [
            'id', 'project', 'hira_activity',
            'hira_activity_name', 'hira_residual_score', 'hira_residual_level',
            'permit_type', 'document_number',
            'work_date', 'work_location', 'work_description',
            'equipment_used', 'work_start', 'work_end',
            'person_in_charge', 'worker_count',
            'safety_area', 'safety_checklist', 'ppe_checklist',
            'worker_certification', 'fit_to_work_document', 'inspection_photo',
            'submitted_by', 'endorsed_by', 'approved_by',
            'retracted_by', 'closed_by',
            'submitted_at', 'endorsed_at', 'approved_at',
            'retracted_at', 'closed_at',
            'post_work_evaluation', 'remarks',
            'status', 'printable',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'submitted_by', 'endorsed_by', 'approved_by',
            'retracted_by', 'closed_by',
            'submitted_at', 'endorsed_at', 'approved_at',
            'retracted_at', 'closed_at',
            'status', 'printable',
            'created_at', 'updated_at'
        ]

    def get_hira_activity_name(self, obj):
        return obj.hira_activity.activity_name

    def get_hira_residual_score(self, obj):
        return obj.hira_activity.residual_score

    def get_hira_residual_level(self, obj):
        return obj.hira_activity.residual_level

    def validate_hira_activity(self, value):
        # enforce HIRA must be approved before PTW can be created
        if value.group.hira_document.status != 'approved':
            raise serializers.ValidationError(
                'Cannot create work permit — the referenced HIRA document is not approved yet.'
            )
        return value