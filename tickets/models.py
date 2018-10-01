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
    NEW = 'NEW'
    ASSIGNED = 'ASSIGNED'
    OPEN = 'OPEN'
    FIXED = 'FIXED'
    RETEST = 'RETEST'
    REOPENED = 'REOPENED'
    VERIFIED = 'VERIFIED'
    BLOCKED = 'BLOCKED'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = (
        (NEW, 'New'),
        (ASSIGNED, 'Assigned'),
        (OPEN, 'Open'),
        (FIXED, 'Fixed'),
        (RETEST, 'Retest'),
        (REOPENED, 'Reopened'),
        (VERIFIED, 'Verified'),
        (BLOCKED, 'Blocked'),
        (CLOSED, 'Closed'),
    )
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets',on_delete='models.CASCADE')
    subject = models.ForeignKey(Subject, related_name='tickets',on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=NEW)
    description = HTMLField(blank=False)
    donation_goal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_donations = models.DecimalField(max_digits=10,decimal_places=2)

class Post(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='posts', on_delete='models.CASCADE')
    comment = HTMLField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts',on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)
