from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings


class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = HTMLField()

    def __unicode__(self):
        return self.name

class Thread(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='threads',on_delete='models.CASCADE')
    subject = models.ForeignKey(Subject, related_name='threads',on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)