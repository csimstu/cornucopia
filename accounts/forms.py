import re

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from TeenHope import settings
from accounts.models import validate_username



class LoginForm(forms.Form):
    username = forms.CharField() # validators=[username_validator]
    password = forms.CharField(widget=forms.PasswordInput) # validators=[password_validator]

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Unmatched username and password.")
        elif not user.is_active:
            raise forms.ValidationError("The account has been disabled.")
        return cleaned_data

from accounts.models import validate_email, validate_password, validate_username


class RegistrationForm(forms.Form):
    username = forms.CharField(validators=[validate_username])
    password = forms.CharField(validators=[validate_password], widget=forms.PasswordInput)
    re_password = forms.CharField(validators=[validate_password], widget=forms.PasswordInput)
    email = forms.CharField(validators=[validate_email])

    def clean_username(self):
        tmp = self.cleaned_data['username']
        if User.objects.filter(username=tmp).count():
            raise forms.ValidationError("Username being occupied.")
        return tmp

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')

        pswd1 = cleaned_data.get('password')

        pswd2 = cleaned_data.get('re_password')
        if pswd2:
            if pswd1 != pswd2:
                msg = "You must enter the same password twice."
                self._errors["re_password"] = self.error_class([msg])

                del cleaned_data["re_password"]

        return cleaned_data




class ForgetPasswordForm(forms.Form):
    username = forms.CharField(validators=[validate_username])
    email = forms.CharField(validators=[validate_email])
