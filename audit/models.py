from django.db import models
from users.models import User


class AuditLog(models.Model):

    class EntityType(models.TextChoices):
        HIRA_DOCUMENT = 'hira_document', 'HIRA Document'
        HIRA_ACTIVITY = 'hira_activity', 'HIRA Activity'
        WORK_PERMIT   = 'work_permit',   'Work Permit'

    class Action(models.TextChoices):
        CREATED   = 'created',   'Created'
        SUBMITTED = 'submitted', 'Submitted'
        APPROVED  = 'approved',  'Approved'
        REJECTED  = 'rejected',  'Rejected'
        ENDORSED  = 'endorsed',  'Endorsed'
        RETRACTED = 'retracted', 'Retracted'
        CLOSED    = 'closed',    'Closed'
        UPLOADED  = 'uploaded',  'Photo Uploaded'

    entity_type  = models.CharField(max_length=30, choices=EntityType.choices)
    entity_id    = models.IntegerField()
    action       = models.CharField(max_length=20, choices=Action.choices)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    timestamp    = models.DateTimeField(auto_now_add=True)
    remarks      = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.entity_type} #{self.entity_id} — {self.action} by {self.performed_by}'