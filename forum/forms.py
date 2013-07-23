from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import CheckboxSelectMultiple
from TeenHope import settings
import re
from models import Category

class NewTopicForm(forms.Form):
    category = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple(),
        queryset=Category.objects.all()
    )
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(NewTopicForm, self).clean()

        category = cleaned_data.get('category')  # a query-set
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if category is None:
            raise forms.ValidationError("Please select a category.")

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
