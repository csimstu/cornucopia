from django import forms
from TeenHope import settings
from models import Category


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


class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

    def clean(self):
        cleaned_data = super(NewPostForm, self).clean()

        content = cleaned_data.get('content')

        if content is None:
            raise forms.ValidationError("Content cannot be empty.")
        elif len(content) > settings.POST_LENGTH_LIMIT:
            raise forms.ValidationError("Post content must be no longer"
                                        "than %d characters." % settings.POST_LENGTH_LIMIT)
        return cleaned_data


class NewReplyForm(forms.Form):
    content = forms.CharField()

    def clean(self):
        cleaned_data = super(NewReplyForm, self).clean()

        content = cleaned_data.get('content')

        if content is None:
            raise forms.ValidationError("Content cannot be empty.")
        elif len(content) > settings.REPLY_LENGTH_LIMIT:
            raise forms.ValidationError("Reply content must be no longer"
                                        "than %d characters." % settings.POST_LENGTH_LIMIT)
        return cleaned_data
