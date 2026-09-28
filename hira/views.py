from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import HIRADocument, HIRAGroup, HIRAActivity
from .serializers import HIRADocumentSerializer, HIRAGroupSerializer, HIRAActivitySerializer
from core.permissions import IsSHEOfficer, IsSHECoordinator, IsAnyRole
from audit.utils import log_action


class HIRADocumentViewSet(viewsets.ModelViewSet):
    queryset = HIRADocument.objects.all()
    serializer_class = HIRADocumentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'submit']:
            return [IsSHEOfficer()]
        elif self.action in ['approve', 'reject']:
            return [IsSHECoordinator()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'she_officer':
            # SHE Officer only sees their own HIRA documents
            return HIRADocument.objects.filter(created_by=user)
        elif user.role == 'she_coordinator':
            # SHE Coordinator sees submitted and beyond
            return HIRADocument.objects.filter(
                status__in=['submitted', 'approved', 'rejected']
            )
        elif user.role in ['site_manager', 'project_manager', 'foreman']:
            # Read-only roles see only approved HIRAs
            return HIRADocument.objects.filter(status='approved')
        return HIRADocument.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        log_action('hira_document', instance.id, 'created', self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        hira = self.get_object()
        if hira.status != 'draft':
            return Response(
                {'error': 'Only draft HIRA can be submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        hira.status = 'submitted'
        hira.save()
        log_action('hira_document', hira.id, 'submitted', request.user)
        return Response({'message': 'HIRA submitted for review'})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        hira = self.get_object()
        if hira.status != 'submitted':
            return Response(
                {'error': 'Only submitted HIRA can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        activities = HIRAActivity.objects.filter(group__hira_document=hira)
        non_acceptable = activities.filter(residual_acceptable=False)
        if non_acceptable.exists():
            return Response(
                {'error': 'Cannot approve — some activities have non-acceptable residual risk',
                'non_acceptable_activities': list(non_acceptable.values('id', 'activity_name', 'residual_score'))},
                status=status.HTTP_400_BAD_REQUEST
            )
        hira.status = 'approved'
        hira.reviewed_by = request.user
        hira.reviewed_at = timezone.now()
        hira.save()
        log_action('hira_document', hira.id, 'approved', request.user)
        return Response({'message': 'HIRA approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        hira = self.get_object()
        if hira.status != 'submitted':
            return Response(
                {'error': 'Only submitted HIRA can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        remarks = request.data.get('remarks', '')
        hira.status = 'rejected'
        hira.reviewed_by = request.user
        hira.reviewed_at = timezone.now()
        hira.remarks = remarks
        hira.save()
        log_action('hira_document', hira.id, 'rejected', request.user, remarks)
        return Response({'message': 'HIRA rejected', 'remarks': remarks})


class HIRAGroupViewSet(viewsets.ModelViewSet):
    queryset = HIRAGroup.objects.all()
    serializer_class = HIRAGroupSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsSHEOfficer()]


class HIRAActivityViewSet(viewsets.ModelViewSet):
    queryset = HIRAActivity.objects.all()
    serializer_class = HIRAActivitySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsSHEOfficer()]