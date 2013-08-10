from django import forms
from django.core.exceptions import ValidationError
from TeenHope import settings
from forum.models import *


class NewTopicForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=Category.objects.get(id=1)
    )
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(NewTopicForm, self).clean()

        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title is None:
            raise forms.ValidationError("Title cannot be empty.")
        elif len(title) > settings.TOPIC_TITLE_LENGTH_LIMIT:
            raise forms.ValidationError("Title length must be no longer "
                                        "than %d characters." % settings.TOPIC_TITLE_LENGTH_LIMIT)
        if content is None:
            raise forms.ValidationError("Content cannot be empty.")
        elif len(content) > settings.POST_LENGTH_LIMIT:
            raise forms.ValidationError("Post content must be no longer"
                                        "than %d characters." % settings.POST_LENGTH_LIMIT)

        return cleaned_data


class NewMessageForm(forms.Form):
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())
    receivers = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(NewMessageForm, self).clean()

        subject = cleaned_data.get('subject')
        content = cleaned_data.get('content')
        receivers = cleaned_data.get('receivers')

        if receivers is None or receivers == "":
            raise forms.ValidationError("Choose at least one receiver.")
        if subject is None:
            raise forms.ValidationError("Subject cannot be empty.")
        elif len(subject) > settings.MESSAGE_SUBJECT_LENGTH_LIMIT:
            raise forms.ValidationError("Subject length must be no longer "
                                        "than %d characters." % settings.MESSAGE_SUBJECT_LENGTH_LIMIT)
        if content is None:
            raise forms.ValidationError("Content cannot be empty.")
        elif len(content) > settings.MESSAGE_LENGTH_LIMIT:
            raise forms.ValidationError("Message content must be no longer"
                                        "than %d characters." % settings.MESSAGE_LENGTH_LIMIT)

        return cleaned_data


class AddConnectionsForm(forms.Form):
    friends = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(AddConnectionsForm, self).clean()
        friends = cleaned_data.get('friends')

        if friends is None or friends == "":
            raise forms.ValidationError("At least add one person.")

        return cleaned_data


from accounts.models import validate_email, validate_nickname, validate_website


class ProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    nickname = forms.CharField(validators=[validate_nickname])
    email = forms.CharField(validators=[validate_email])
    thumbnail = forms.ImageField(required=False)

    website = forms.CharField(required=False)
    renren = forms.CharField(required=False)
    qq = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    biography = forms.CharField(required=False, widget=forms.Textarea)
    motto = forms.CharField(required=False, widget=forms.Textarea)

    def clean_thumbnail(self):
        image = self.cleaned_data['thumbnail']
        if image:
            if image.size > 4 * 1024 * 1024:
                raise ValidationError("Image file too large (> 4mb).")


    def clean_website(self):
        website = self.cleaned_data['website']
        if website:
            validate_website(website)
        return website


from accounts.models import validate_password


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField(validators=[validate_password])
    re_password = forms.CharField(validators=[validate_password])

    def __init__(self, user=None, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.__user = user

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.__user.check_password(old_password):
            raise ValidationError("Incorrect password.")
        return old_password

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        new_password = cleaned_data.get('new_password')
        re_password = cleaned_data.get('re_password')

        if new_password != re_password:
            raise forms.ValidationError('Inconsistent passwords.')

        return cleaned_data