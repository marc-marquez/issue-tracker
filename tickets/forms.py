from django import forms
from .models import Ticket, Post


class TicketForm(forms.ModelForm):
    name = forms.CharField(label="Ticket name")
    is_a_poll = forms.BooleanField(label="Include a poll?", required=False)
    
    class Meta:
        model = Ticket
        fields = ['name']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['comment']