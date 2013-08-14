from django import forms
from TeenHope import settings
from models import Category

class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

    def clean_content(self):
        content = self.cleaned_data['content']

        if content is None:
            raise forms.ValidationError("Content cannot be empty.")
        elif len(content) > settings.POST_LENGTH_LIMIT:
            raise forms.ValidationError("Post content must be no longer"
                                        "than %d characters." % settings.POST_LENGTH_LIMIT)
        return content
