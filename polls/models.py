"""
Models for saving polls, poll options, and votes to the database
"""
from django.db import models
from django.conf import settings
from tickets.models import Subject, Ticket


class Poll(models.Model):
    """
    Poll consists of a poll question and subject type (e.g. Bug, Feature)
    """
    question = models.TextField()
    subject = models.OneToOneField(Subject, null=True, on_delete='models.CASCADE')

    def __unicode__(self):
        return self.question


class PollOption(models.Model):
    """
    Poll options consist of a poll and corresponding ticket to be voted on
    """
    poll = models.ForeignKey(Poll, related_name='options', on_delete='models.CASCADE')
    ticket = models.OneToOneField(Ticket, related_name='options', on_delete='models.CASCADE')

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    """
    Votes consist of the poll the vote is being used for, the option in that poll,
    and the user that voted.
    """
    poll = models.ForeignKey(Poll, related_name='votes', on_delete='models.CASCADE')
    option = models.ForeignKey(PollOption, related_name='votes',
                               on_delete='models.CASCADE')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes',
                             on_delete='models.CASCADE')
