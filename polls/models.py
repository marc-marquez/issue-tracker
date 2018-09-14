from django.db import models
from django.conf import settings
from tickets.models import Subject,Ticket


class Poll(models.Model):
    question = models.TextField()
    subject = models.OneToOneField(Subject, null=True, on_delete='models.CASCADE')

    def __unicode__(self):
        return self.question


class PollOption(models.Model):
    name = models.CharField(max_length=255)
    poll = models.ForeignKey(Poll, related_name='options',on_delete='models.CASCADE')
    ticket = models.ForeignKey(Ticket,related_name='options',on_delete='models.CASCADE')

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes',on_delete='models.CASCADE')
    option = models.ForeignKey(PollOption, related_name='votes', on_delete='models.CASCADE')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes',on_delete='models.CASCADE')