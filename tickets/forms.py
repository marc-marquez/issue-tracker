from django import forms
from .models import Ticket, Post


class TicketForm(forms.ModelForm):
    name = forms.CharField(label='Title')
    
    class Meta:
        model = Ticket
        fields = ['name','description']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['comment']

class StatusForm(forms.ModelForm):
    status = forms.ChoiceField(label='Status',choices=Ticket.STATUS_CHOICES)

    class Meta:
        model = Ticket
        fields = ['status']

class DonationGoalForm(forms.ModelForm):
    #goal = forms.CharField(label='Donation Goal')

    class Meta:
        model = Ticket
        fields = ['donation_goal']


