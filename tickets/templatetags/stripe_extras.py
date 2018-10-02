import stripe
from django import template
from django.db.models import Count
#from django.urls import reverse
#from django.contrib.auth import models


register = template.Library()

@register.filter
def get_ticket_donation_value(option):
    #list = get_donations_list()

    try:
        #total_donations = list[ticket.id]
        total_donations = option.ticket.feature.total_donations
    except:
        total_donations = 0

    return total_donations

def get_donations_list():
    # get charge list
    list = stripe.Charge.list()

    # dict to get total donations for each ticket_id
    total_donations = {}
    for charge in list:
        # print(charge['metadata']['ticket_id'])
        current_id = int(charge['metadata']['ticket_id'])

        if current_id not in total_donations:
            total_donations[current_id] = 0

        total_donations[current_id] += float(charge['amount'] / 100)

    return total_donations

@register.filter
def donation_percentage(option):

    if option.ticket.feature.donation_goal == 0:
        return 0

    return (float(option.ticket.feature.total_donations)/float(option.ticket.feature.donation_goal)) * 100

