from django import forms
from TeenHope import settings


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