from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.context_processors import csrf
from .forms import TicketForm, PostForm, FeatureForm, BugForm
from tickets.models import Subject, Post, Ticket, Bug, Feature
from polls.models import PollOption, Poll
from django.conf import settings
import stripe
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from tickets.serializers import TicketSerializer, TicketCustomSerializer

stripe.api_key = settings.STRIPE_SECRET

def forum(request):
    return render(request, 'forum/forum.html', {'subjects': Subject.objects.all()})

def dashboard(request):
    return render(request, 'forum/dashboard.html')

def voting_results(request,subject_id):
    #for subject in Subject.objects.all():
    subject = get_object_or_404(Subject, pk=subject_id)
    options = PollOption.objects.filter(poll_id=subject_id).annotate(vote_count=Count('votes')).order_by('-vote_count')

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
            print("No ticket_id found in charge.")

    if subject.name == 'Feature':
        for option in options:
            try:
                option.ticket.feature.total_donations = total_donations[option.ticket.id]
            except:
                option.ticket.feature.total_donations = 0
            option.ticket.feature.save()

    return render(request, 'forum/voting_results.html', {'subject': subject, 'options': options})

def tickets(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/tickets.html', {'subject': subject})

@login_required(login_url='/login/')
def new_ticket(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        #if subject.name == 'Feature':
        #    supplement_form = FeatureForm(request.POST,prefix="supplementform")
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
                supplement_form = FeatureForm(request.POST, prefix="supplementform")
                if supplement_form.is_valid():
                    supplementform = supplement_form.save(False)
                    feature = Feature(ticket_id=ticket.id)
                    feature.donation_goal = supplementform.donation_goal
                    feature.total_donations = 0
                    feature.save()
            else:
                print("Unknown subject -- " + subject.name)

            #if first ticket in subject then create poll
            try:
                var = subject.poll
            except:
                subject.poll = Poll()
                subject.poll.question = "What " + subject.name.lower() + " should i work on?"
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

            messages.success(request, "You have created a new ticket!")

            return redirect(reverse('ticket', args=[ticket.pk]))
        else:
            messages.error(request,ticket_form.errors)
            return redirect(reverse('new_ticket',args={subject_id}))
    else:
        ticket_form = TicketForm()
        if subject.name == 'Feature':
            supplement_form = FeatureForm(prefix="supplementform")
        elif subject.name == 'Bug':
            supplement_form = BugForm(prefix="supplementform")
        else:
            pass

    args = {
        'ticket_form': ticket_form,
        'supplement_form': supplement_form,
        'form_action': reverse('new_ticket', kwargs={"subject_id": subject.id}),
        'button_text': 'Add New Ticket',
        'subject': subject,
    }

    args.update(csrf(request))

    return render(request, 'forum/ticket_form.html', args)

@login_required(login_url='/login/')
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()

            if ticket.subject.name == 'Feature':
                feature = get_object_or_404(Feature, pk=ticket.feature.id)
                supplement_form = FeatureForm(request.POST, instance=feature)
            else:
                bug = get_object_or_404(Bug, pk=ticket.bug.id)
                print("Ticket id (BUG): " + str(ticket.bug.id))
                supplement_form = BugForm(request.POST, instance=bug)

            supplement_form.save()
            messages.success(request, "You have updated your ticket!")

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        ticket_form = TicketForm(instance=ticket)
        if ticket.subject.name == 'Feature':
            feature = get_object_or_404(Feature,pk=ticket.feature.id)
            supplement_form = FeatureForm(instance=feature)
        else:
            bug = get_object_or_404(Bug, pk=ticket.bug.id)
            supplement_form = BugForm(instance=bug)

    args = {
        'ticket_form': ticket_form,
        'supplement_form': supplement_form,
        'form_action': reverse('edit_ticket', kwargs={"ticket_id": ticket.id}),
        'button_text': 'Update Ticket'
    }
    args.update(csrf(request))

    return render(request, 'forum/ticket_form.html', args)

def ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    args = {'ticket': ticket}
    args.update(csrf(request))
    return render(request, 'forum/ticket.html', args)

@login_required(login_url='/login/')
def new_post(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == "POST":

        post_form = PostForm(request.POST,prefix="postform")
        if post_form.is_valid():

            postform = post_form.save(False)
            postform.ticket = ticket
            postform.user = request.user
            postform.save()

            messages.success(request, "Your post has been added to the ticket!")

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        post_form = PostForm(prefix="postform")


    args = {
        'post_form': post_form,
        'form_action': reverse('new_post', args={ticket.id}),
        'button_text': 'Add Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)

@login_required(login_url='/login/')
def edit_post(request, ticket_id, post_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "You have updated your ticket!")

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        form = PostForm(instance=post)

    args = {
        'post_form': form,
        'form_action': reverse('edit_post', kwargs={"ticket_id": ticket.id, "post_id": post.id}),
        'button_text': 'Update Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)


@login_required(login_url='/login/')
def delete_post(request, ticket_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    ticket_id = post.ticket.id
    post.delete()

    messages.success(request, "Your post was deleted!")

    return redirect(reverse('ticket', args={ticket_id}))


@login_required(login_url='/login/')
def ticket_vote(request, ticket_id, subject_id,*donate_votes):
    subject = Subject.objects.get(id=subject_id)

    #Check to see if voted on poll option is on bugs
    votes = subject.poll.votes.filter(user=request.user)
    if(subject.name == 'Bug'):
        for vote in votes:
            if (vote.option.ticket.id==ticket_id):
                messages.error(request, "You already voted on this! ... You’re not trying to cheat are you?")
                return redirect(reverse('tickets', args={subject_id}))

    option = PollOption.objects.get(ticket_id=ticket_id)

    if donate_votes:
        count = 0
        while count < donate_votes[0]:
            option.votes.create(poll=subject.poll, user=request.user)
            count+=1
    else:
        option.votes.create(poll=subject.poll, user=request.user)

    messages.success(request, "We've registered your vote(s)!")

    return redirect(reverse('tickets', args={subject_id}))

@login_required(login_url='/login/')
def ticket_donate(request,ticket_id,subject_id):
    if request.method == 'POST':
        ticket = Ticket.objects.get(id=ticket_id)
        subject = Subject.objects.get(id=subject_id)

        try:
            customer = stripe.Customer.retrieve(request.user.stripe_id)
        except stripe.error.StripeError as e:
            messages.error(request, "No credit card on file. Please add a credit card.")
            #redirect to profile page to add a card
            return redirect(reverse('profile'))

        try:
            #retrive list of cards for customer
            cards = stripe.Customer.retrieve(customer.id).sources.list(object='card')
            charge = stripe.Charge.create(
                amount=1000,
                currency="usd",
                source=cards.data[0].id,
                customer=customer.id,
                description="Donation for the "+ticket.name+" "+subject.name,
                metadata={'ticket_id':ticket.id}
            )
        except stripe.error.StripeError as e:
            messages.error(request, e)
            return redirect(reverse('tickets', args={subject_id}))

        if(charge.status=='succeeded'):
            messages.success(request,"Thanks for the $10 donation!")
            #After successfull charge, add vote to ticket
            ticket_vote(request, ticket_id, subject_id)
        else:
            messages.error(request,"Could not process donation.")

    return redirect(reverse('tickets', args={subject_id}))

@login_required(login_url='/login/')
def custom_donate(request,subject_id,ticket_id):
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
            messages.error(request, "No customer registered with Stripe. Please add a credit card.")
            return redirect(reverse('profile'))

        default_source = customer.default_source

        if default_source is None:
            messages.error(request, "No credit card registered with Stripe. Please add a credit card.")
            return redirect(reverse('profile'))
        else:
            default_card = customer.sources.retrieve(default_source)

        try:
            #retrive list of cards for customer
            charge = stripe.Charge.create(
                amount=stripe_formatted_amount,
                currency="usd",
                source=default_card.id,
                customer=customer.id,
                description="Donation for the "+ticket.name+" "+subject.name,
                metadata={'ticket_id':ticket.id}
            )
        except stripe.error.StripeError as e:
            messages.error(request, e)
            return redirect(reverse('tickets', args={subject_id}))

        if(charge.status=='succeeded'):
            messages.success(request,"Thanks for the $" + str_amount + " donation!")
            #update donation table
            ticket_vote(request, ticket_id, subject_id,votes)
        else:
            messages.error(request,"Could not process donation.")

        return redirect(reverse('tickets', args={subject_id}))
    else:
        #return render(request, 'forum/donation_form.html',args={"ticket":ticket})
        pass

    args = {
        'ticket':ticket,
        'subject':subject,
    }
    return render(request, 'forum/donation_form.html', args)

class TicketView(APIView):

    def get(self,request):
        ticket_items = Ticket.objects.all()
        serializer = TicketSerializer(ticket_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

class TicketCustomView(APIView):

    def get(self,request):
        ticket_items = Ticket.objects.all()
        serializer = TicketCustomSerializer(ticket_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)