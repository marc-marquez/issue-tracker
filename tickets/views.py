from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.context_processors import csrf
from .forms import TicketForm, PostForm, StatusForm, DonationGoalForm
from tickets.models import Subject, Post, Ticket
from polls.models import PollOption, Poll
from django.conf import settings
import stripe
from django.db.models import Count
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET

def forum(request):
    return render(request, 'forum/forum.html', {'subjects': Subject.objects.all()})

def report(request,subject_id):
    #for subject in Subject.objects.all():
    subject = get_object_or_404(Subject, pk=subject_id)
    options = PollOption.objects.filter(poll_id=subject_id).annotate(vote_count=Count('votes')).order_by('-vote_count')

    # get charge list
    list = stripe.Charge.list()

    # dict to get total donations for each ticket_id
    total_donations = {}
    for charge in list:
        current_id = int(charge['metadata']['ticket_id'])

        if current_id not in total_donations:
            total_donations[current_id] = 0

        total_donations[current_id] += float(charge['amount'] / 100)

    for option in options:
        try:
            option.ticket.total_donations = total_donations[option.ticket.id]
        except:
            option.ticket.total_donations = 0
        option.ticket.save()

    return render(request, 'forum/progress_report.html', {'subject': subject,'options': options})

def tickets(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/tickets.html', {'subject': subject})

@login_required(login_url='/login/')
def new_ticket(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(False)
            ticket.subject = subject
            ticket.status = ticket.CREATED
            ticket.user = request.user

            #temporary until donations app is working
            ticket.donation_goal = 0
            ticket.total_donations = 0

            ticket.save()

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
        ticket_form = TicketForm()

    args = {
        'ticket_form': ticket_form,
        'form_action': reverse('new_ticket', kwargs={"subject_id": subject.id}),
        'button_text': 'Add New Ticket',
        'subject': subject,
    }

    args.update(csrf(request))

    return render(request, 'forum/ticket_form.html', args)

@login_required(login_url='/login/')
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    #post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            messages.success(request, "You have updated your ticket!")

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        ticket_form = TicketForm(instance=ticket)

    args = {
        'ticket_form': ticket_form,
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
        '''
        #Need to check if the requester is the admin to add status to be updated
        if request.user.is_staff:
            status_form = StatusForm(request.POST,prefix="statusform")
            if status_form.is_valid():
                statusform = status_form.save(False)
                ticket.status = statusform.status
                ticket.save()
            donation_goal_form = DonationGoalForm(request.POST,prefix="donationgoalform")
            if donation_goal_form.is_valid():
                donationgoalform = donation_goal_form.save(False)
                ticket.donation_goal = donationgoalform.donation_goal
                ticket.save()
        '''
        post_form = PostForm(request.POST,prefix="postform")
        if post_form.is_valid():

            postform = post_form.save(False)
            postform.ticket = ticket
            postform.user = request.user
            postform.save()

            messages.success(request, "Your post has been added to the ticket!")

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        #status_form = StatusForm(instance=Ticket.objects.get(id=ticket_id),prefix="statusform")
        post_form = PostForm(prefix="postform")
        #donation_goal_form = DonationGoalForm(instance=Ticket.objects.get(id=ticket_id),prefix="donationgoalform")

    args = {
        'post_form': post_form,
        #'status_form': status_form,
        #'donation_goal_form': donation_goal_form,
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
def ticket_vote(request, ticket_id, subject_id,*votes):
    subject = Subject.objects.get(id=subject_id)

    #Check to see if voted on poll option is on bugs
    option = subject.poll.votes.filter(user=request.user)

    if(subject.name == 'Bug'):
        for x in option:
            if (x.option_id==int(ticket_id)):
                messages.error(request, "You already voted on this! ... You’re not trying to cheat are you?")
                return redirect(reverse('tickets', args={subject_id}))

    option = PollOption.objects.get(ticket_id=ticket_id)

    if votes:
        print("Process " + str(votes[0]) + " votes")
        count = 0
        while count < votes[0]:
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
        print("Process Donation...")

        amount = int(request.POST['amount'])
        votes = int(amount/COST_PER_VOTE)
        stripe_formatted_amount = amount*100
        str_amount = str(amount)
        print("Donation Amount: $" + str_amount)

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
                amount=stripe_formatted_amount,
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
            messages.success(request,"Thanks for the $" + str_amount + " donation!")
            #args = {votes}
            #After successfull charge, add vote to ticket
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