from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from TeenHope import settings
import re

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

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

class RegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField()

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if not self.check_username(username):
            raise forms.ValidationError("Invalid username.")
        if (User.objects.filter(username=username).count()):
            raise forms.ValidationError("Username being occupied.")

        pswd1 = cleaned_data.get('password')
        pswd2 = cleaned_data.get('re_password')
        if not self.check_password(pswd1):
            raise forms.ValidationError("Invalid password.")
        if (pswd1 != pswd2):
            raise forms.ValidationError("Inconsistent passwords.")

        email = cleaned_data.get('email')
        if not self.check_email(email):
            raise forms.ValidationError("Incorrect email address.")

        return cleaned_data

    def check_username(self, username):
        return username and re.compile(settings.USERNAME_PATTERN).match(username)
    def check_password(self, password):
        return password and re.compile(settings.PASSWORD_PATTERN).match(password)
    def check_email(self, email):
        return email and re.compile(settings.EMAIL_PATTERN).match(email)

class ProfileForm(forms.Form):
    name = forms.CharField()
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField()

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.__user = user


    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        name = cleaned_data.get('name')
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        re_password = cleaned_data.get('re_password')
        email = cleaned_data.get('email')

        if not self.__user.check_password(old_password):
            raise forms.ValidationError('Wrong password.')
        if not self.check_password(new_password):
            raise forms.ValidationError('Invalid new password.')
        if new_password != re_password:
            raise forms.ValidationError('Inconsistent new passwords.')
        if not self.check_email(email):
            raise forms.ValidationError('Invalid new email address.')

        return cleaned_data

    def check_password(self, password):
        return password and re.compile(settings.PASSWORD_PATTERN).match(password)
    def check_email(self, email):
        return email and re.compile(settings.EMAIL_PATTERN).match(email)