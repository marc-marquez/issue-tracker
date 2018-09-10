from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.context_processors import csrf
from .forms import TicketForm, PostForm
from tickets.models import Subject, Post, Ticket
from django.forms import formset_factory
from polls.forms import PollSubjectForm, PollForm
from polls.models import PollSubject


def forum(request):
    return render(request, 'forum/forum.html', {'subjects': Subject.objects.all()})

def tickets(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/tickets.html', {'subject': subject})


@login_required
def new_ticket(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    poll_subject_formset_class = formset_factory(PollSubjectForm, extra=3)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        post_form = PostForm(request.POST)
        poll_form = PollForm(request.POST)
        poll_subject_formset = poll_subject_formset_class(request.POST)
        if (ticket_form.is_valid() and
                post_form.is_valid() and
                poll_form.is_valid() and
                poll_subject_formset.is_valid()):
            ticket = ticket_form.save(False)
            ticket.subject = subject
            ticket.user = request.user
            ticket.save()

            post = post_form.save(False)
            post.user = request.user
            post.ticket = ticket
            post.save()

            poll = poll_form.save(False)
            poll.ticket = ticket
            poll.save()

            for subject_form in poll_subject_formset:
                subject = subject_form.save(False)
                subject.poll = poll
                subject.save()

            messages.success(request, "You have created a new ticket!")

            return redirect(reverse('ticket', args=[ticket.pk]))

    else:
        ticket_form = TicketForm()
        post_form = PostForm()
        poll_form = PollForm()
        poll_subject_formset = poll_subject_formset_class()

    args = {
        'ticket_form': ticket_form,
        'post_form': post_form,
        'subject': subject,
        'poll_form': poll_form,
        'poll_subject_formset': poll_subject_formset,
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
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(False)
            post.ticket = ticket
            post.user = request.user
            post.save()

            messages.success(request, "Your post has been added to the ticket!")

            return redirect(reverse('ticket', args={ticket.pk}))
    else:
        form = PostForm()

    args = {
        'form': form,
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
        'form': form,
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
    ticket = Ticket.objects.get(id=ticket_id)

    subject = ticket.poll.votes.filter(user=request.user)

    if subject:
        messages.error(request, "You already voted on this! ... You’re not trying to cheat are you?")
        return redirect(reverse('ticket', args={ticket_id}))

    subject = PollSubject.objects.get(id=subject_id)

    subject.votes.create(poll=subject.poll, user=request.user)

    messages.success(request, "We've registered your vote!")

    return redirect(reverse('ticket', args={ticket_id}))