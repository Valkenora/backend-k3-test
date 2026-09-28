from .models import AuditLog


def log_action(entity_type, entity_id, action, performed_by, remarks=''):
    AuditLog.objects.create(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        performed_by=performed_by,
        remarks=remarks
    )