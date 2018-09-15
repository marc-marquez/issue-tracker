from django import forms
from .models import Ticket, Post


class TicketForm(forms.ModelForm):
    name = forms.CharField(label="Title")
    #is_a_poll = forms.BooleanField(label="Include a poll?", required=False)
    
    class Meta:
        model = Ticket
        fields = ['name']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['comment']

class StatusForm(forms.ModelForm):
    #status =forms.CharField(label="Status")
    status = forms.ChoiceField(label="Status",choices=Ticket.STATUS_CHOICES)

    #def __init__(self,*args,**kwargs):
    #    super(StatusForm,self).__init__(*args,**kwargs)
    #    if (args) is not None:


    class Meta:
        model = Ticket
        fields = ['status']

