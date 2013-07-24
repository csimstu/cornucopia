from django.contrib import admin
from forum.models import Category, Topic, Post, Reply
from django import forms
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Reply)
