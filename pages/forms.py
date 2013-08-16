from django import forms
from TeenHope import settings
from pages.models import Tag


class NewArticleForm(forms.Form):
    tags = forms.CharField(widget=forms.HiddenInput(), required=False)
    title = forms.CharField()
    abstract = forms.CharField(widget=forms.Textarea())
    content = forms.CharField(widget=forms.Textarea())

    def __init__(self, user, *args, **kwargs):
        super(NewArticleForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(author=user)

    def clean_title(self):
        title = self.cleaned_data['title']
        if title is None:
            raise forms.ValidationError("Title cannot be empty.")
        elif len(title) > settings.ARTICLE_TITLE_LENGTH_LIMIT:
            raise forms.ValidationError("Title length must be no longer"
                                        "than %d characters." % settings.ARTICLE_TITLE_LENGTH_LIMIT)
        return title

    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']

        if abstract is None:
            raise forms.ValidationError("Abstract cannot be empty.")
        elif len(abstract) > settings.ABSTRACT_LENGTH_LIMIT:
            raise forms.ValidationError("Article abstract must be no longer"
                                        "than %d characters." % settings.ABSTRACT_LENGTH_LIMIT)
        return abstract

    def clean_content(self):
        content = self.cleaned_data['content']

        if content is None:
            raise forms.ValidationError("Content cannot be empty.")
        elif len(content) > settings.ARTICLE_LENGTH_LIMIT:
            raise forms.ValidationError("Article content must be no longer"
                                        "than %d characters." % settings.ARTICLE_LENGTH_LIMIT)
        return content


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
