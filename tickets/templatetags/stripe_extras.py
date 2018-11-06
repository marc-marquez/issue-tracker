import stripe
from django import template


register = template.Library()


@register.filter
def get_ticket_donation_value(option):

    try:
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
        current_id = int(charge['metadata']['ticket_id'])

        if current_id not in total_donations:
            total_donations[current_id] = 0

        total_donations[current_id] += float(charge['amount'] / 100)

    return total_donations


@register.filter
def donation_percentage(ticket):

    if ticket.feature.donation_goal == 0:
        return 0

    return (float(ticket.feature.total_donations)/float(ticket.feature.donation_goal)) * 100
