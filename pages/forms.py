from django import forms
from django.forms import CheckboxSelectMultiple
from TeenHope import settings
from pages.models import Tag

class NewArticleForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        widget=CheckboxSelectMultiple(),
        queryset=Tag.objects.all()
    )
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())

    def clean(self):
        cleaned_data = super(NewArticleForm, self).clean()
        tags = cleaned_data.get('tags')
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if tags is None:
            raise forms.ValidationError("At least choose one tag")

        if title is None:
            raise forms.ValidationError("Title cannot be empty.")
        elif len(title) > settings.ARTICLE_TITLE_LENGTH_LIMIT:
            raise forms.ValidationError("Title length must be no longer"
                                        "than %d characters." % settings.ARTICLE_TITLE_LENGTH_LIMIT)
        if content is None:
            raise forms.ValidationError("Content cannot be empty.")
        elif len(content) > settings.ARTICLE_LENGTH_LIMIT:
            raise forms.ValidationError("Article content must be no longer"
                                        "than %d characters." % settings.ARTICLE_LENGTH_LIMIT)

        return cleaned_data


class NewCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

    def clean(self):
        cleaned_data = super(NewCommentForm, self).clean()

        content = cleaned_data.get('content')

        if content is None:
            raise forms.ValidationError("Content cannot be empty.")
        elif len(content) > settings.COMMENT_LENGTH_LIMIT:
            raise forms.ValidationError("Comment content must be no longer than"
                                        "%d characters." % settings.COMMENT_LENGTH_LIMIT)

        return cleaned_data
