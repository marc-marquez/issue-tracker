import arrow
from django import template
from django.urls import reverse
from django.contrib.auth import models

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

    if(votes):
        for vote in votes:

            # Check to see if already voted on this option
            if(ticket.id == vote.option_id):
                return ""

    if user.is_authenticated:
        link = """
        <div class="col-md-3 btn-vote">
        <a href="%s" class="btn btn-default btn-sm">
            Add my vote!
        </a>
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