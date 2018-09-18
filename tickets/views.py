from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.context_processors import csrf
from .forms import TicketForm, PostForm, StatusForm
from tickets.models import Subject, Post, Ticket
from polls.models import PollOption, Poll


def forum(request):
    return render(request, 'forum/forum.html', {'subjects': Subject.objects.all()})

def tickets(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/tickets.html', {'subject': subject})


@login_required
def new_ticket(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        post_form = PostForm(request.POST)
        if (ticket_form.is_valid() and
                post_form.is_valid()):
            ticket = ticket_form.save(False)
            ticket.subject = subject
            ticket.user = request.user
            ticket.save()

            post = post_form.save(False)
            post.user = request.user
            post.ticket = ticket
            post.save()

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
        post_form = PostForm()

    args = {
        'ticket_form': ticket_form,
        'post_form': post_form,
        'subject': subject,
    }

    args.update(csrf(request))

    return render(request, 'forum/ticket_form.html', args)

def ticket(request, ticket_id):
    ticket_ = get_object_or_404(Ticket, pk=ticket_id)
    args = {'ticket': ticket_}
    args.update(csrf(request))
    return render(request, 'forum/ticket.html', args)

@login_required
def new_post(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == "POST":
        #Need to check if the requester is the admin to add status to be updated
        if request.user.is_staff:
            status_form = StatusForm(request.POST,prefix="statusform")
            if status_form.is_valid():
                statusform = status_form.save(False)
                ticket.status = statusform.status
                ticket.save()

        post_form = PostForm(request.POST,prefix="postform")
        if post_form.is_valid(): #and status_form.is_valid():
            #statusform = status_form.save(False)
            #ticket.status = statusform.status
            #ticket.save()

            postform = post_form.save(False)
            postform.ticket = ticket
            postform.user = request.user
            postform.save()

            messages.success(request, "Your post has been added to the ticket!")

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        status_form = StatusForm(prefix="statusform")
        post_form = PostForm(prefix="postform")

    args = {
        'post_form': post_form,
        'status_form': status_form,
        'form_action': reverse('new_post', args={ticket.id}),
        'button_text': 'Update Post'
    }
    args.update(csrf(request))

    return render(request, 'forum/post_form.html', args)

@login_required
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


@login_required
def delete_post(request, ticket_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    ticket_id = post.ticket.id
    post.delete()

    messages.success(request, "Your post was deleted!")

    return redirect(reverse('ticket', args={ticket_id}))


@login_required
def ticket_vote(request, ticket_id, subject_id):
    subject = Subject.objects.get(id=subject_id)

    #Check to see if voted on poll option
    option = subject.poll.votes.filter(user=request.user)

    for x in option:
        #print(request.user.username + " voted for " + str(x.option_id))

        if (x.option_id==int(ticket_id)):
            messages.error(request, "You already voted on this! ... You’re not trying to cheat are you?")
            return redirect(reverse('tickets', args={subject_id}))

    option = PollOption.objects.get(ticket_id=ticket_id)

    option.votes.create(poll=subject.poll, user=request.user)

    messages.success(request, "We've registered your vote!")

    return redirect(reverse('tickets', args={subject_id}))

def ticket_donate(request,ticket_id,subject_id):
    pass
