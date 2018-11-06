from django import forms
from .models import Ticket, Post, Feature, Bug
from django.core.exceptions import ValidationError


class TicketForm(forms.ModelForm):
    name = forms.CharField(label='Title')
    
    class Meta:
        model = Ticket
        fields = ['name','description','status']

    def __init__(self,*args,**kwargs):
        super(TicketForm,self).__init__(*args,**kwargs)
        instance = getattr(self,'instance',None)

        #if a brand new ticket, then disable status and donation goal
        if(instance.id is None):
            self.fields['status'].disabled = True

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Ticket.objects.filter(name=name).exists():
            message = "This ticket name already exists. Please choose another one. "
            raise ValidationError(message)

        return name


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['comment']


class FeatureForm(forms.ModelForm):

    class Meta:
        model = Feature
        fields = ['donation_goal']
        exclude = ['total_donations']

    def __init__(self,*args,**kwargs):
        super(FeatureForm,self).__init__(*args,**kwargs)
        instance = getattr(self,'instance',None)

        #if a brand new ticket, then disable donation goal
        if instance.id is None:
            self.fields['donation_goal'].disabled = True


class BugForm(forms.ModelForm):

    class Meta:
        model = Bug
        exclude = ['ticket']


