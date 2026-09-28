from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'location', 'client_name', 'start_date', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']