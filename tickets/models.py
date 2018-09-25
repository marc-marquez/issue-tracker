from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = HTMLField()

    def __unicode__(self):
        return self.name

class Ticket(models.Model):
    CREATED = 'CREATED'
    ASSIGNED = 'ASSIGNED'
    IN_PROGESS = 'IN PROGRESS'
    COMPLETED = 'COMPLETED'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (ASSIGNED, 'Assigned'),
        (IN_PROGESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CLOSED, 'Closed'),
    )
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets',on_delete='models.CASCADE')
    subject = models.ForeignKey(Subject, related_name='tickets',on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=CREATED)
    description = HTMLField(blank=False)
    donation_goal = models.DecimalField(max_digits=10,decimal_places=2)
    total_donations = models.DecimalField(max_digits=10,decimal_places=2)

class Post(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='posts', on_delete='models.CASCADE')
    comment = HTMLField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts',on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)
    #status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=CREATED)
