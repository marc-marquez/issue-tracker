"""
Form that create/modify bug and feature tickets and posts
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import Ticket, Post, Feature, Bug


class TicketForm(forms.ModelForm):
    """
    Ticket form
    """
    name = forms.CharField(label='Title')
    class Meta:
        """
        Fields to include on form
        """
        model = Ticket
        fields = ['name', 'description', 'status']

    def __init__(self, *args, **kwargs):
        """
        Set init details for Ticket form
        :return: Disable the status field on form
        """
        super(TicketForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        #if a brand new ticket, then disable status and donation goal
        if instance.id is None:
            self.fields['status'].disabled = True

    def clean_name(self):
        """
        Validates ticket name does not exist in database
        :return: validated ticket name
        """
        name = self.cleaned_data.get('name')
        if Ticket.objects.filter(name=name).exists() and self.instance.id is None:
            message = 'This ticket name already exists. Please choose another one. '
            raise ValidationError(message)

        return name

    def clean_description(self):
        """
        Validates description field is not left blank
        :return: validated description text
        """
        description = self.cleaned_data.get('description')
        if description is None:
            message = 'Description is required and cannot be left blank. '
            raise ValidationError(message)

        return description

class PostForm(forms.ModelForm):
    """
    Post form
    """
    class Meta:
        """
        Fields to include on form
        """
        model = Post
        fields = ['comment']


class FeatureForm(forms.ModelForm):
    """
    Feature ticket form
    """
    class Meta:
        """
        Fields to include and exclude on form
        """
        model = Feature
        fields = ['donation_goal']
        exclude = ['total_donations']

    def __init__(self, *args, **kwargs):
        """
        Set init details for Feature form
        :return: Disable the donation goal field on form
        """
        super(FeatureForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        #if a brand new ticket, then disable donation goal
        if instance.id is None:
            self.fields['donation_goal'].disabled = True


class BugForm(forms.ModelForm):
    """
    Bug ticket form
    """
    class Meta:
        """
        Fields to include on form
        """
        model = Bug
        exclude = ['ticket']
