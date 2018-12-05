"""
These added function are used to:
    - Get ticket donations value
    - Get ticket donations list
    - Get the percentage value of a donation towards its goal
"""

import stripe
from django import template


register = template.Library()


@register.filter
def get_ticket_donation_value(option):
    """
        Gets ticket donation value of a ticket
        :param option: The ticket requested to get the donation value of
        :return: donation value
    """

    try:
        total_donations = option.ticket.feature.total_donations
    except:
        total_donations = 0

    return total_donations


def get_donations_list():
    """
        Get the entire donations list from the Stripe database
        :return: donations list
    """

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
    """
        Gets the percentage value of the donations earned in relation to donations goal
        :param ticket: The ticket requested to get the donation percentage of
        :return: percentage value of donations earned
    """
    if ticket.feature.donation_goal == 0:
        return 0

    return (float(ticket.feature.total_donations)/float(ticket.feature.donation_goal)) * 100
