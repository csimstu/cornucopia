from django import forms
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