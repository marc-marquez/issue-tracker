"""
These are the views to:
    - Render forum
    - Render work dashboard
    - Render voting results for a subject
    - Add a new ticket to a subject
    - Edit a ticket in a subject
    - Render all tickets for a subject
    - Render a specific ticket in a subject
    - Add a new post to a ticket
    - Edit a post in a ticket
    - Delete a post from a ticket
    - Cast vote(s) for a ticket
    - Donate towards a ticket
    - Update the ticket donation data in the database
"""

from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.context_processors import csrf
from django.conf import settings
from django.db.models import Count
import stripe
from tickets.models import Subject, Post, Ticket, Bug, Feature
from polls.models import PollOption, Poll
from .forms import TicketForm, PostForm, FeatureForm, BugForm


stripe.api_key = settings.STRIPE_SECRET


def forum(request):
    """
    Renders forum page
    :param request: Type of request
    :return: forum page
    """

    return render(request, 'forum/forum.html', {'subjects': Subject.objects.all()})


def dashboard(request):
    """
    Renders work dashboard page
    :param request: Type of request
    :return: work dashboard page
    """

    return render(request, 'forum/dashboard.html')


def voting_results(request, subject_id):
    """
    Render voting results page for a subject
    :param request: Type of request
    :param subject_id: Requested subject for voting results (e.g. Bug, Feature)
    :return: Voting results page for specific subject
    """

    subject = get_object_or_404(Subject, pk=subject_id)
    options = PollOption.objects.filter(poll_id=subject_id)\
        .annotate(vote_count=Count('votes'))\
        .order_by('-vote_count')

    if subject.name == 'Feature':
        # get charge list.Stripe limit is 100 per query
        list = []
        charges = stripe.Charge.list(limit=100)

        for charge in charges.auto_paging_iter():
            list.append(charge)

        # dict to get total donations for each ticket_id
        total_donations = {}
        for current_charge in list:
            try:
                current_id = int(current_charge['metadata']['ticket_id'])
                if current_id not in total_donations:
                    total_donations[current_id] = 0
                total_donations[current_id] += float(current_charge['amount'] / 100)
            except:
                print('No ticket_id found in Stripe charge metadata.')

        for option in options:
            try:
                option.ticket.feature.total_donations = total_donations[option.ticket.id]
            except:
                option.ticket.feature.total_donations = 0
            option.ticket.feature.save()

    return render(request, 'forum/voting_results.html', {'subject': subject, 'options': options})


def tickets(request, subject_id):
    """
    Render tickets page for a subject
    :param request: Type of request
    :param subject_id: Requested subject for voting results (e.g. Bug, Feature)
    :return: Tickets page for a specific subject
    """
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/tickets.html', {'subject': subject})


@login_required(login_url='/login/')
def new_ticket(request, subject_id):
    """
    Add a new ticket to a subject in the database
    :param request: Type of request
    :param subject_id: Requested subject for new ticket (e.g. Bug, Feature)
    :return: Render ticket form (GET) or Save new ticket to database (POST)
    """

    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)

        if ticket_form.is_valid():
            ticket = ticket_form.save(False)
            ticket.subject = subject
            ticket.status = ticket.NEW
            ticket.user = request.user
            ticket.save()

            if subject.name == 'Bug':
                bug = Bug(ticket_id=ticket.id)
                bug.save()
            elif subject.name == 'Feature':
                supplement_form = FeatureForm(request.POST, prefix='supplementform')
                if supplement_form.is_valid():
                    supplementform = supplement_form.save(False)
                    feature = Feature(ticket_id=ticket.id)
                    feature.donation_goal = supplementform.donation_goal
                    feature.total_donations = 0
                    feature.save()
            else:
                print('WARNING: Unused subject -- ' + subject.name)

            #if first ticket in subject then create poll
            try:
                var = subject.poll
            except:
                subject.poll = Poll()
                subject.poll.question = 'What ' + subject.name.lower() + ' should i work on?'
                subject.poll.subject_id = subject_id
                subject.poll.save()

            #Create poll option for new ticket
            polloption = PollOption()
            polloption.name = ticket.name
            polloption.poll_id = subject.poll.id
            polloption.ticket_id = ticket.id
            polloption.save()

            #Add poll option to poll
            subject.poll.options.add(polloption)

            #Save poll with new option
            subject.poll.save()

            messages.success(request, 'You have created a new ticket!')
            return redirect(reverse('ticket', args=[ticket.pk]))
        else:
            for field, errors in ticket_form.errors.items():
                format_error = field.capitalize() + ' : ' + errors
                messages.error(request, format_error)
            return redirect(reverse('new_ticket', args={subject_id}))
    else:
        ticket_form = TicketForm()
        if subject.name == 'Feature':
            supplement_form = FeatureForm(prefix='supplementform')
        elif subject.name == 'Bug':
            supplement_form = BugForm(prefix='supplementform')
        else:
            pass

    args = {
        'ticket_form': ticket_form,
        'supplement_form': supplement_form,
        'form_action': reverse('new_ticket', kwargs={'subject_id': subject.id}),
        'button_text': 'Add New Ticket',
        'subject': subject,
    }

    args.update(csrf(request))

    return render(request, 'forum/ticket_form.html', args)


@login_required(login_url='/login/')
def edit_ticket(request, ticket_id):
    """
    Edit an existing ticket in the database
    :param request: Type of request
    :param ticket_id: Requested ticket to be edited
    :return: Render ticket form with data from database (GET) or
             Save edited ticket to database (POST)
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()

            if ticket.subject.name == 'Feature':
                feature = get_object_or_404(Feature, pk=ticket.feature.id)
                supplement_form = FeatureForm(request.POST, instance=feature)
            else:
                bug = get_object_or_404(Bug, pk=ticket.bug.id)
                print('Ticket id (BUG): ' + str(ticket.bug.id))
                supplement_form = BugForm(request.POST, instance=bug)

            supplement_form.save()
            messages.success(request, 'You have updated your ticket!')
            return redirect(reverse('ticket', args={ticket.pk}))
        else:
            for field, errors in ticket_form.errors.items():
                format_error = field.capitalize() + ' : ' + errors
                messages.error(request, format_error)
            return redirect(reverse('edit_ticket', args={ticket.pk}))
    else:
        ticket_form = TicketForm(instance=ticket)
        if ticket.subject.name == 'Feature':
            feature = get_object_or_404(Feature, pk=ticket.feature.id)
            supplement_form = FeatureForm(instance=feature)
        else:
            bug = get_object_or_404(Bug, pk=ticket.bug.id)
            supplement_form = BugForm(instance=bug)

    args = {
        'ticket_form': ticket_form,
        'supplement_form': supplement_form,
        'form_action': reverse('edit_ticket', kwargs={'ticket_id': ticket.id}),
        'button_text': 'Update Ticket'
    }
    args.update(csrf(request))

    return render(request, 'forum/ticket_form.html', args)


def ticket(request, ticket_id):
    """
    Render ticket page for a requested ticket
    :param request: Type of request
    :param ticket_id: Requested ticket to be viewed
    :return: Render ticket page
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    args = {'ticket': ticket}
    args.update(csrf(request))
    return render(request, 'forum/ticket.html', args)


@login_required(login_url='/login/')
def new_post(request, ticket_id):
    """
    Add a new post to a ticket in the database
    :param request: Type of request
    :param ticket_id: Requested ticket to add post to
    :return: Render post form (GET) or Save new post to database (POST)
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':

        post_form = PostForm(request.POST, prefix='postform')
        if post_form.is_valid():

            postform = post_form.save(False)
            postform.ticket = ticket
            postform.user = request.user
            postform.save()

            messages.success(request, 'Your post has been added to the ticket!')

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        post_form = PostForm(prefix='postform')


    args = {
        'post_form': post_form,
        'form_action': reverse('new_post', args={ticket.id}),
        'button_text': 'Add Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required(login_url='/login/')
def edit_post(request, ticket_id, post_id):
    """
    Edit an existing post to a ticket in the database
    :param request: Type of request
    :param ticket_id: Requested ticket where post exists
    :param post_id: Requested post to be edited
    :return: Render post form with data from database (GET) or Save edited post to database (POST)
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have updated your ticket!')

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        form = PostForm(instance=post)

    args = {
        'post_form': form,
        'form_action': reverse('edit_post', kwargs={'ticket_id': ticket.id, 'post_id': post.id}),
        'button_text': 'Update Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required(login_url='/login/')
def delete_post(request, ticket_id, post_id):
    """
    Delete an existing post to a ticket in the database
    :param request: Type of request
    :param ticket_id: Requested ticket where post exists
    :param post_id: Requested post to be deleted
    :return: Render ticket page (GET) or Delete post from database (POST)
    """

    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        ticket_id = post.ticket.id
        post.delete()
        messages.success(request, 'Your post was deleted!')

    return redirect(reverse('ticket', args={ticket_id}))


@login_required(login_url='/login/')
def ticket_vote(request, ticket_id, subject_id, *donate_votes):
    """
    Cast vote(s) for a ticket
    :param request: Type of request
    :param ticket_id: Requested ticket to cast vote(s) for
    :param subject_id: Requested subject of ticket for casting vote(s)
    :param donate_votes (optional): Number of votes to be cast if based on donation amount
    :return: Render page used to cast vote (tickets page or ticket page)
    """

    subject = Subject.objects.get(id=subject_id)

    #Check to see if voted on poll option is on bugs
    votes = subject.poll.votes.filter(user=request.user)

    #previous http location
    prev = request.META.get('HTTP_REFERER')

    if subject.name == 'Bug':
        for vote in votes:
            if vote.option.ticket.id == ticket_id:
                messages.error(request,
                               'You already voted on this! ... You’re not trying to cheat are you?')
                return redirect(prev)

    option = PollOption.objects.get(ticket_id=ticket_id)

    if donate_votes:
        count = 0
        while count < donate_votes[0]:
            option.votes.create(poll=subject.poll, user=request.user)
            count += 1
    else:
        option.votes.create(poll=subject.poll, user=request.user)

    messages.success(request, 'We have registered your vote!')

    return redirect(prev)


@login_required(login_url='/login/')
def custom_donate(request, subject_id, ticket_id):
    """
    Donate towards a ticket
    :param request: Type of request
    :param ticket_id: Requested ticket to donate to
    :param subject_id: Requested subject of ticket
    :return: Render donation page (GET) or Process donations through Stripe (POST)
    """

    ticket = get_object_or_404(Ticket, pk=ticket_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    COST_PER_VOTE = 10

    if request.method == 'POST':
        amount = int(request.POST['amount'])
        votes = int(amount/COST_PER_VOTE)
        stripe_formatted_amount = amount*100
        str_amount = str(amount)

        # Look for default card. If not, redirect to profile page to add a card
        try:
            customer = stripe.Customer.retrieve(request.user.stripe_id)
        except stripe.error.StripeError as e:
            messages.error(request, 'No credit card on file. Please add a credit card.')
            #return redirect(reverse('profile'))
            return redirect(reverse('profile')+'?next='+request.path)

        default_source = customer.default_source

        if default_source is None:
            messages.error(request, 'No credit card on file. Please add a credit card.')
            #return redirect(reverse('profile'))
            return redirect(reverse('profile') + '?next=' + request.path)
        else:
            default_card = customer.sources.retrieve(default_source)

        try:
            #retrive list of cards for customer
            charge = stripe.Charge.create(
                amount=stripe_formatted_amount,
                currency='usd',
                source=default_card.id,
                customer=customer.id,
                description='Donation for the '+ticket.name+' '+subject.name,
                metadata={'ticket_id':ticket.id}
            )
        except stripe.error.StripeError as e:
            messages.error(request, e)
            return redirect(reverse('tickets', args={subject_id}))

        if charge.status == 'succeeded':
            messages.success(request, 'Thanks for the $' + str_amount + ' donation!')
            update_ticket_donation_data(ticket)
            ticket_vote(request, ticket_id, subject_id, votes)
        else:
            messages.error(request, 'Could not process donation.')

        return redirect(reverse('tickets', args={subject_id}))
    else:
        pass

    args = {
        'ticket':ticket,
        'subject':subject,
    }
    return render(request, 'forum/donation_form.html', args)


def update_ticket_donation_data(ticket):
    """
    Update the ticket donation data in the database
    :param ticket: Requested ticket to be updated
    :return: Save updated donation data in the database
    """

    # get charge list
    list = stripe.Charge.list()

    # dict to get total donations for each ticket_id
    total_donations = {}
    for charge in list:
        try:
            current_id = int(charge['metadata']['ticket_id'])
            if current_id not in total_donations:
                total_donations[current_id] = 0
            total_donations[current_id] += float(charge['amount'] / 100)
        except:
            print('No ticket_id found in charge.')

    # Update feature with new donation total donations
    try:
        ticket.feature.total_donations = total_donations[ticket.id]
    except:
        ticket.feature.total_donations = 0
    ticket.feature.save()
