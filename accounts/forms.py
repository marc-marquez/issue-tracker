"""
Forms to register new users and login users.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Registration form
    """
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    email = forms.EmailField()

    class Meta:
        """
        Fields to include and exclude from form
        """
        model = User
        fields = ['email', 'password1', 'password2']
        exclude = ['username']

    def clean_password2(self):
        """
        Validates passwords match
        :return: validated password
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = 'Passwords do not match. '
            raise ValidationError(message)

        return password2

    def clean_email(self):
        """
        Validates email does not exist in database
        :return: validated email
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            message = 'This email address already exists. Please choose another one. '
            raise ValidationError(message)

        return email

    def save(self, commit=True):
        """
        Saves the user to the database
        :param commit: Commit save
        :return: user instance
        """
        instance = super(UserRegistrationForm, self).save(commit=False)

        # automatically set to email address to create a unique identifier
        instance.username = instance.email

        if commit:
            instance.save()

        return instance

class UserLoginForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
