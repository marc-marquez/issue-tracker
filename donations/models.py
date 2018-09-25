from django.db import models
from tickets.models import Ticket

# Create your models here.

class Donation(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='donations', on_delete='models.CASCADE')
    donation_goal = models.DecimalField(max_digits=10, decimal_places=2)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2)

