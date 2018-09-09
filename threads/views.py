from django.shortcuts import render, get_object_or_404
from .models import Subject, Thread, Post
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.context_processors import csrf


def forum(request):
    return render(request, 'forum/forum.html', {'subjects': Subject.objects.all()})

def threads(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'forum/threads.html', {'subject': subject})

@login_required
def new_thread(request, subject_id):
    pass