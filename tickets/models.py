"""
Models for saving subjects, tickets (bug or feature), and posts to the database
"""

from django.db import models
from django.utils import timezone
from django.conf import settings
from tinymce.models import HTMLField


class Subject(models.Model):
    """
    Subject consists of a name and a description
    """
    name = models.CharField(max_length=255)
    description = HTMLField()

    def __unicode__(self):
        return self.name


class Ticket(models.Model):
    """
    Ticket consists of a name, description, user, subject, creation date, and status
    """
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
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tickets',
                             on_delete='models.CASCADE')
    subject = models.ForeignKey(Subject, related_name='tickets', on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=NEW)
    description = HTMLField()

    def __unicode__(self):
        return self.name


class Post(models.Model):
    """
    Post consists of a ticket, comment, username, and creation date
    """
    ticket = models.ForeignKey(Ticket, related_name='posts', on_delete='models.CASCADE')
    comment = HTMLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts',
                             on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)


class Bug(models.Model):
    """
    Bug consists of a ticket
    """
    ticket = models.OneToOneField(Ticket, on_delete='models.CASCADE')


class Feature(models.Model):
    """
    Feature consists of a ticket, donation goal, and total donations received
    """
    ticket = models.OneToOneField(Ticket, on_delete='models.CASCADE')
    donation_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0)
