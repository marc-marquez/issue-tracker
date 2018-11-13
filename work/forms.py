"""
Form that creates a work log for a specific ticket
"""
from django import forms
from .models import Log


class LogForm(forms.ModelForm):
    """
    Form used to create work log
    """
    class Meta:
        """
        Fields to include and exclude in work log
        """
        model = Log
        fields = ['ticket', 'user', 'hours', 'date']
        exclude = ['created_at']
