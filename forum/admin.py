from django.contrib import admin
from forum.models import Category, Topic, Post
from django import forms
from ckeditor.widgets import CKEditorWidget

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post, PostAdmin)
