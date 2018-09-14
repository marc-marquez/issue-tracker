from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings

STATUS_CHOICES = (
    (1,'Assigned'),
    (2,'In Progress'),
    (3,'Completed'),
)

class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = HTMLField()

    def __unicode__(self):
        return self.name

class Ticket(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets',on_delete='models.CASCADE')
    subject = models.ForeignKey(Subject, related_name='tickets',on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)

class Post(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='posts', on_delete='models.CASCADE')
    comment = HTMLField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts',on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)
    #status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=1)