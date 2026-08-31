from django import forms
from django.contrib.auth.forms import AuthenticationForm


class SecureAdminLoginForm(AuthenticationForm):
    """
    Same mechanics as Django's normal login form, just re-skinned and with
    copy that makes clear this gate is not for portfolio visitors.
    """
    username = forms.CharField(
        label='Admin username',
        widget=forms.TextInput(attrs={'autofocus': True, 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
