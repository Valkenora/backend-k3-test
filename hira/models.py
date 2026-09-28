from django.db import models
from users.models import User
from projects.models import Project


class HIRADocument(models.Model):

    class Meta:
        verbose_name = 'HIRA Document'
        verbose_name_plural = 'HIRA Documents'

    class Status(models.TextChoices):
        DRAFT     = 'draft',     'Draft'
        SUBMITTED = 'submitted', 'Submitted'
        APPROVED  = 'approved',  'Approved'
        REJECTED  = 'rejected',  'Rejected'

    project         = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='hira_documents')
    document_number = models.CharField(max_length=100)
    work_package    = models.CharField(max_length=255)
    work_area       = models.CharField(max_length=255)
    status          = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='hira_created')
    reviewed_by     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hira_reviewed')
    reviewed_at     = models.DateTimeField(null=True, blank=True)
    remarks         = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.document_number} — {self.work_package}'


class HIRAGroup(models.Model):

    class Meta:
        verbose_name = 'HIRA Group'
        verbose_name_plural = 'HIRA Groups'

    hira_document     = models.ForeignKey(HIRADocument, on_delete=models.CASCADE, related_name='groups')
    location_function = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.hira_document.document_number} — {self.location_function}'


class HIRAActivity(models.Model):

    class Meta:
        verbose_name = 'HIRA Activity'
        verbose_name_plural = 'HIRA Activities'

    class ActivityType(models.TextChoices):
        ROUTINE    = 'R',  'Routine'
        NON_ROUTINE = 'NR', 'Non-Routine'
        EMERGENCY  = 'E',  'Emergency'

    class RiskLevel(models.TextChoices):
        SR = 'SR', 'Sangat Rendah'
        R  = 'R',  'Rendah'
        M  = 'M',  'Medium'
        T  = 'T',  'Tinggi'
        E  = 'E',  'Ekstrim'

    group           = models.ForeignKey(HIRAGroup, on_delete=models.CASCADE, related_name='activities')
    activity_name   = models.CharField(max_length=255)
    activity_type   = models.CharField(max_length=5, choices=ActivityType.choices)

    # stored as JSON — display only fields
    activity_details = models.JSONField(default=dict, blank=True)
    # expects: potential_hazards, risk_impact, applicable_regulations,
    #          control_category, control_measures, opportunity_notes

    # initial risk — user inputs
    initial_likelihood  = models.IntegerField()
    initial_severity    = models.IntegerField()
    # initial risk — calculated
    initial_score       = models.IntegerField(editable=False)
    initial_level       = models.CharField(max_length=5, choices=RiskLevel.choices, editable=False)
    initial_acceptable  = models.BooleanField(editable=False)

    # residual risk — user inputs
    residual_likelihood = models.IntegerField()
    residual_severity   = models.IntegerField()
    # residual risk — calculated
    residual_score      = models.IntegerField(editable=False)
    residual_level      = models.CharField(max_length=5, choices=RiskLevel.choices, editable=False)
    residual_acceptable = models.BooleanField(editable=False)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def calculate_risk(self, likelihood, severity):
        score = likelihood * severity
        if score <= 1:
            level = 'SR'
        elif score <= 4:
            level = 'R'
        elif score <= 8:
            level = 'M'
        elif score <= 12:
            level = 'T'
        else:
            level = 'E'
        acceptable = score <= 4
        return score, level, acceptable

    def save(self, *args, **kwargs):
        # auto calculate on every save
        self.initial_score, self.initial_level, self.initial_acceptable = \
            self.calculate_risk(self.initial_likelihood, self.initial_severity)
        self.residual_score, self.residual_level, self.residual_acceptable = \
            self.calculate_risk(self.residual_likelihood, self.residual_severity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.activity_name} (Rt={self.residual_score})'