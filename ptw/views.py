from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import WorkPermit
from .serializers import WorkPermitSerializer
from core.permissions import IsForeman, IsSHEOfficer, IsSiteOrProjectManager
from audit.utils import log_action


class WorkPermitViewSet(viewsets.ModelViewSet):
    queryset = WorkPermit.objects.all()
    serializer_class = WorkPermitSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'submit', 'close']:
            return [IsForeman()]
        elif self.action in ['endorse']:
            return [IsSHEOfficer()]
        elif self.action in ['approve', 'retract']:
            return [IsSiteOrProjectManager()]
        elif self.action == 'reject':
            return [IsAuthenticated()]  # SHE Officer or Site/PM can reject
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'foreman':
            # Foreman only sees their own permits
            return WorkPermit.objects.filter(submitted_by=user)
        elif user.role == 'she_officer':
            # SHE Officer sees submitted and endorsed permits + their own endorsed
            return WorkPermit.objects.filter(
                status__in=['submitted', 'endorsed', 'approved', 'active', 'rejected', 'retracted', 'closed']
            )
        elif user.role == 'she_coordinator':
            # SHE Coordinator sees all permits for oversight
            return WorkPermit.objects.all()
        elif user.role in ['site_manager', 'project_manager']:
            # SM/PM sees endorsed and beyond
            return WorkPermit.objects.filter(
                status__in=['endorsed', 'approved', 'active', 'rejected', 'retracted', 'closed']
            )
        return WorkPermit.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save(submitted_by=self.request.user)
        log_action('work_permit', instance.id, 'created', self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        permit = self.get_object()
        if permit.status != 'draft':
            return Response(
                {'error': 'Only draft permits can be submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        permit.status = 'submitted'
        permit.submitted_at = timezone.now()
        permit.save()
        log_action('work_permit', permit.id, 'submitted', request.user)
        return Response({'message': 'Work permit submitted for SHE Officer review'})

    @action(detail=True, methods=['post'])
    def endorse(self, request, pk=None):
        permit = self.get_object()
        if permit.status != 'submitted':
            return Response(
                {'error': 'Only submitted permits can be endorsed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not permit.inspection_photo:
            return Response(
                {'error': 'Inspection photo is required before endorsement'},
                status=status.HTTP_400_BAD_REQUEST
            )
        permit.status = 'endorsed'
        permit.endorsed_by = request.user
        permit.endorsed_at = timezone.now()
        permit.save()
        log_action('work_permit', permit.id, 'endorsed', request.user)
        return Response({'message': 'Work permit endorsed — forwarded to Site/Project Manager'})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        permit = self.get_object()
        if permit.status != 'endorsed':
            return Response(
                {'error': 'Only endorsed permits can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        permit.status = 'approved'
        permit.approved_by = request.user
        permit.approved_at = timezone.now()
        permit.printable = True
        permit.save()
        log_action('work_permit', permit.id, 'approved', request.user)
        return Response({'message': 'Work permit approved — work may commence'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        permit = self.get_object()
        if permit.status not in ['submitted', 'endorsed']:
            return Response(
                {'error': 'Only submitted or endorsed permits can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user.role not in ['she_officer', 'site_manager', 'project_manager']:
            return Response(
                {'error': 'You do not have permission to reject this permit'},
                status=status.HTTP_403_FORBIDDEN
            )
        remarks = request.data.get('remarks', '')
        permit.status = 'rejected'
        permit.remarks = remarks
        permit.save()
        log_action('work_permit', permit.id, 'rejected', request.user, remarks)
        return Response({'message': 'Work permit rejected', 'remarks': remarks})

    @action(detail=True, methods=['post'])
    def retract(self, request, pk=None):
        permit = self.get_object()
        if permit.status != 'approved':
            return Response(
                {'error': 'Only approved permits can be retracted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        remarks = request.data.get('remarks', '')
        permit.status = 'retracted'
        permit.retracted_by = request.user
        permit.retracted_at = timezone.now()
        permit.remarks = remarks
        permit.save()
        log_action('work_permit', permit.id, 'retracted', request.user, remarks)
        return Response({'message': 'Work permit retracted'})

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        permit = self.get_object()
        if permit.status != 'approved':
            return Response(
                {'error': 'Only approved permits can be closed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        evaluation = request.data.get('post_work_evaluation', '')
        permit.status = 'closed'
        permit.closed_by = request.user
        permit.closed_at = timezone.now()
        permit.post_work_evaluation = evaluation
        permit.save()
        log_action('work_permit', permit.id, 'closed', request.user)
        return Response({'message': 'Work permit closed successfully'})

    @action(detail=True, methods=['post'], url_path='upload_photo')
    def upload_photo(self, request, pk=None):
        permit = self.get_object()
        if 'inspection_photo' not in request.FILES:
            return Response(
                {'error': 'No photo provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        permit.inspection_photo = request.FILES['inspection_photo']
        permit.save()
        log_action('work_permit', permit.id, 'uploaded', request.user)
        return Response({'message': 'Photo uploaded successfully'})