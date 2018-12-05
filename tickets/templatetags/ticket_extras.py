"""
These added function are used to:
    - Get total count of posts for a specific subject
    - Get a humanized start time (e.g. "2 months ago")
    - Get the username of the last post
    - Display the vote button for a specific ticket
    - Get the percentage value of votes a ticket receives
    - Get a customized color of the status
    - Get the vote rank of a specific ticket
"""

from django.db.models import Count
from django import template
from django.urls import reverse
import arrow
from polls.models import PollOption


register = template.Library()


@register.filter
def get_total_subject_posts(subject):
    """
        Gets the total count of posts for a specific subject
        :param subject: The subject requested to get the post count for
        :return: total count of posts for subject
    """

    total_posts = 0
    for ticket in subject.tickets.all():
        total_posts += ticket.posts.count()
    return total_posts


@register.filter
def started_time(created_at):
    """
        Get a humanized start time (e.g. "2 months ago")
        :return: start time in a humanized form
    """

    return arrow.get(created_at).humanize()


@register.simple_tag
def last_posted_user_name(ticket):
    """
        Get the username of the last post created
        :param ticket: The requested ticket to get last post for
        :return: username of last post
    """

    last_post = ticket.posts.all().order_by('created_at').last()
    return last_post.user.username


@register.simple_tag
def user_vote_button(ticket, subject, user):
    """
        Display the vote button for a specific ticket
        :param ticket: The requested ticket for voting
        :param subject: The requested subject of the ticket for voting
        :param user: The current user that is voting
        :return: Customized button to be displayed on webpage
    """

    votes = subject.poll.votes.filter(user_id=user.id)

    if votes:
        for vote in votes:
            #if bug, each user only gets one vote per ticket
            if ticket.subject.name == 'Bug':
                # Check to see if already voted on this option
                if ticket.id == vote.option.ticket.id:
                    return """<button class='btn btn-secondary'disabled>
                    Voted <i class='fas fa-thumbs-up'></i></button>"""

    if user.is_authenticated:
        link = """
        <div class='btn-vote'>
        <a href='%s' class='btn btn-success' onclick='showLoader(true)'>Upvote <i class='fas fa-thumbs-up'></i></a>
        </div>""" % reverse('cast_vote', kwargs={'ticket_id': ticket.id, 'subject_id': subject.id})
        return link
    return ""


@register.filter
def vote_percentage(ticket):
    """
        Get the percentage value of votes a ticket receives
        :param ticket: The requested ticket to get vote percentage for
        :return: percentage of votes received in relation to other tickets
    """

    count = ticket.votes.count()

    if count == 0:
        return 0

    total_votes = ticket.poll.votes.count()
    return (100 / total_votes) * count


@register.filter
def get_label_color(status):
    """
        Get a customized color of the status
        :param status: The requested status to get a customized color for
        :return: customized color
    """

    colors = {'NEW':'grey',
              'ASSIGNED':'blue',
              'OPEN': 'orange',
              'FIXED': 'purple',
              'RETEST':'cyan',
              'REOPENED':'orange',
              'VERIFIED': 'green',
              'BLOCKED': 'red',
              'CLOSED':'black',
              }

    return colors[status]


@register.filter
def get_vote_rank(ticket):
    """
        Get the vote rank of a specific ticket
        :param ticket: The requested ticket to get the vote rank for
        :return: vote rank in comparison to other tickets
    """

    subject_id = ticket.subject.id

    options = PollOption.objects.filter(poll_id=subject_id)\
        .annotate(vote_count=Count('votes'))\
        .order_by('-vote_count')

    rank = 1
    for option in options:
        if option.ticket.id == ticket.id:
            return rank
        else:
            rank += 1

    return rank
