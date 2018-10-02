from django import forms
from .models import Ticket, Post, Feature, Bug


class TicketForm(forms.ModelForm):
    name = forms.CharField(label='Title')
    
    class Meta:
        model = Ticket
        fields = ['name','description','status']

    def __init__(self,*args,**kwargs):
        super(TicketForm,self).__init__(*args,**kwargs)
        #self.fields['donation_goal'].disabled = True
        instance = getattr(self,'instance',None)

        #if a brand new ticket, then disable status and donation goal
        if(instance.id is None):
            self.fields['status'].disabled = True
            #self.fields['donation_goal'].disabled = True

        #if this instance is a bug, then disable donation goal
        #try:
        #    if self.instance.subject.name == 'Bug':
        #        self.fields['donation_goal'].disabled=True
        #except:
        #    self.fields['donation_goal'].disabled = True

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['comment']

#class StatusForm(forms.ModelForm):
#    status = forms.ChoiceField(label='Status',choices=Ticket.STATUS_CHOICES)
#
#    class Meta:
#        model = Ticket
#        fields = ['status']

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


