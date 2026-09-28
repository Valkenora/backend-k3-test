from django.db import models
from users.models import User
from projects.models import Project
from hira.models import HIRAActivity


class WorkPermit(models.Model):

    class PermitType(models.TextChoices):
        WORKING_AT_HEIGHT = 'working_at_height', 'Ijin Kerja Di Ketinggian'
        CONFINED_SPACE    = 'confined_space',    'Ijin Kerja Ruang Terbatas'
        FIRE_EXPLOSIVE    = 'fire_explosive',    'Ijin Kerja Berpotensi Kebakaran Dan Ledakan'
        LIFTING           = 'lifting',           'Ijin Kerja Pekerjaan Mengangkat'
        TOWER_CRANE       = 'tower_crane',       'Ijin Kerja Instalasi Dan Segmen Tower Crane'

    class Status(models.TextChoices):
        DRAFT      = 'draft',      'Draft'
        SUBMITTED  = 'submitted',  'Submitted'
        ENDORSED   = 'endorsed',   'Endorsed'
        APPROVED   = 'approved',   'Approved'
        ACTIVE     = 'active',     'Active'
        REJECTED   = 'rejected',   'Rejected'
        RETRACTED  = 'retracted',  'Retracted'
        CLOSED     = 'closed',     'Closed'

    # core references
    project          = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_permits')
    hira_activity    = models.ForeignKey(HIRAActivity, on_delete=models.PROTECT, related_name='work_permits')
    permit_type      = models.CharField(max_length=30, choices=PermitType.choices)
    document_number  = models.CharField(max_length=100, blank=True)

    # form fields — pulled from HIRA but stored here for record integrity
    work_date        = models.DateField()
    work_location    = models.CharField(max_length=255)
    work_description = models.CharField(max_length=500)
    equipment_used   = models.TextField(blank=True)
    work_start       = models.TimeField()
    work_end         = models.TimeField()
    person_in_charge = models.CharField(max_length=255)
    worker_count     = models.IntegerField()

    # checklist fields — differs per permit type, stored as JSON
    safety_area      = models.JSONField(default=dict, blank=True)
    # e.g. {"A": true, "B": false, "C": true}

    safety_checklist = models.JSONField(default=dict, blank=True)
    # e.g. {"1": true, "2": true, "3": false, ...}

    ppe_checklist    = models.JSONField(default=dict, blank=True)
    # e.g. {"sarung_tangan": true, "safety_belt": false, "body_harness": true}

    # attachments — nullable for now
    worker_certification  = models.FileField(upload_to='ptw/certifications/', null=True, blank=True)
    fit_to_work_document  = models.FileField(upload_to='ptw/fittowork/', null=True, blank=True)
    inspection_photo      = models.ImageField(upload_to='ptw/inspections/', null=True, blank=True)

    # workflow — who did what
    submitted_by     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='permits_submitted')
    endorsed_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='permits_endorsed')
    approved_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='permits_approved')
    retracted_by     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='permits_retracted')
    closed_by        = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='permits_closed')

    # timestamps per action
    submitted_at     = models.DateTimeField(null=True, blank=True)
    endorsed_at      = models.DateTimeField(null=True, blank=True)
    approved_at      = models.DateTimeField(null=True, blank=True)
    retracted_at     = models.DateTimeField(null=True, blank=True)
    closed_at        = models.DateTimeField(null=True, blank=True)

    # post work
    post_work_evaluation = models.TextField(blank=True)
    remarks              = models.TextField(blank=True)

    # status
    status           = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    printable        = models.BooleanField(default=False)

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Work Permit'
        verbose_name_plural = 'Work Permits'

    def __str__(self):
        return f'{self.get_permit_type_display()} — {self.work_location} ({self.status})'