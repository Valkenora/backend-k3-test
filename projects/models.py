from django.db import models
from users.models import User

class Project(models.Model):
    name        = models.CharField(max_length=255)
    location    = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    start_date  = models.DateField()
    created_by  = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='projects_created'
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} — {self.client_name}'