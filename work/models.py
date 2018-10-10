from django.db import models
from django.conf import settings
from tickets.models import Ticket
from django.utils import timezone


class Log(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='logs', on_delete='models.CASCADE')
    #comment = HTMLField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='logs', on_delete='models.CASCADE')
    created_at = models.DateTimeField(default=timezone.now)
    hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=False,auto_now=False,default=timezone.now)

    #def __unicode__(self):
    #    return self.ticket.name