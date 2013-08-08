import re

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from TeenHope import settings


def username_validator(username):
    if not username:
        raise ValidationError("Username cannot be none.")
    if not re.compile(settings.USERNAME_PATTERN).match(username):
        raise ValidationError(settings.USERNAME_HINT)


def password_validator(password):
    if not password:
        raise ValidationError("Password cannot be none.")
    if not re.compile(settings.PASSWORD_PATTERN).match(password):
        raise ValidationError(settings.PASSWORD_HINT)


def email_validator(email):
    if not email:
        raise ValidationError("Email is required.")
    if not re.compile(settings.EMAIL_PATTERN).match(email):
        raise ValidationError("Invalid email format.")


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


class RegistrationForm(forms.Form):
    username = forms.CharField(validators=[username_validator])
    password = forms.CharField(validators=[password_validator], widget=forms.PasswordInput)
    re_password = forms.CharField(validators=[password_validator], widget=forms.PasswordInput)
    email = forms.CharField(validators=[email_validator])

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


class ProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    nickname = forms.CharField()

    website = forms.CharField(required=False)
    renren = forms.CharField(required=False)
    qq = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    biography = forms.CharField(required=False, widget=forms.Textarea)
    motto = forms.CharField(required=False, widget=forms.Textarea)

    new_password = forms.CharField(required=False, widget=forms.PasswordInput)
    re_password = forms.CharField(required=False, widget=forms.PasswordInput)
    email = forms.CharField()

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.__user = user


    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        nickname = cleaned_data.get('nickname')
        website = cleaned_data.get('website')
        renren = cleaned_data.get('renren')
        qq = cleaned_data.get('qq')
        phone = cleaned_data.get('phone')
        biography = cleaned_data.get('biography')
        motto = cleaned_data.get('motto')
        new_password = cleaned_data.get('new_password')
        re_password = cleaned_data.get('re_password')
        email = cleaned_data.get('email')

        if new_password is not None and len(new_password) > 0:
            if not self.check_password(new_password):
                raise forms.ValidationError('Invalid new password.')
            if new_password != re_password:
                raise forms.ValidationError('Inconsistent new passwords.')

        if not self.check_email(email):
            raise forms.ValidationError('Invalid new email address.')

        return cleaned_data

    def check_password(self, password):
        return password and re.compile(settings.PASSWORD_PATTERN).match(password)



