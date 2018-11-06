from django.db.models import Count
from django import template
from django.urls import reverse
import arrow
from polls.models import PollOption


register = template.Library()


@register.filter
def get_total_subject_posts(subject):
    total_posts = 0
    for ticket in subject.tickets.all():
        total_posts += ticket.posts.count()
    return total_posts


@register.filter
def started_time(created_at):
    return arrow.get(created_at).humanize()


@register.simple_tag
def last_posted_user_name(ticket):
    last_post = ticket.posts.all().order_by('created_at').last()
    return last_post.user.username


@register.simple_tag
def user_vote_button(ticket, subject, user):
    votes = subject.poll.votes.filter(user_id=user.id)

    if votes:
        for vote in votes:
            #if bug, each user only gets one vote per ticket
            if ticket.subject.name == 'Bug':
                # Check to see if already voted on this option
                if ticket.id == vote.option.ticket.id:
                    return """<button class="btn btn-secondary"
                    disabled data-toggle="tooltip" data-placement="bottom" 
                    title="Upvote"><i class="fas fa-thumbs-up"></i></button>"""

    if user.is_authenticated:
        link = """
        <div class="btn-vote">
        <a href="%s" class="btn btn-success" data-toggle="tooltip" data-placement="bottom" 
        title="Upvote"><i class="fas fa-thumbs-up"></i></a>
        </div>""" % reverse('cast_vote', kwargs={'ticket_id': ticket.id, 'subject_id': subject.id})
        return link
    return ""


@register.filter
def vote_percentage(ticket):
    count = ticket.votes.count()

    if count == 0:
        return 0

    total_votes = ticket.poll.votes.count()
    return (100 / total_votes) * count


@register.filter
def get_label_color(status):
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
