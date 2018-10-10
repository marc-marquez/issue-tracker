from django import forms
from .models import Log


class LogForm(forms.ModelForm):

    #def clean(self):
    #    log_date = self.cleaned_data.get('date')
    #    if log_date <

    class Meta:
        model = Log
        fields = ['ticket', 'user', 'hours','date']
        exclude = ['created_at']
