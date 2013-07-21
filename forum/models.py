from django.db import models
from django.contrib.auth.models import User
from TeenHope import settings


class Category(models.Model):
    title = models.CharField(max_length=settings.CATEGORY_TITLE_LENGTH_LIMIT)  # title of the category


class Topic(models.Model):
    category = models.ManyToManyField(Category)     # one topic might belong to many kinds
    title = models.CharField(max_length=settings.TOPIC_TITLE_LENGTH_LIMIT)         # title of the topic
    date_published = models.DateTimeField()         # time published


class Post(models.Model):
    topic = models.ForeignKey(Topic)    # a post belongs to only one topic
    author = models.ForeignKey(User)    # the writer of the post
    date_published = models.DateTimeField()         # time published
    content = models.CharField(max_length=settings.POST_LENGTH_LIMIT)        # content of the post, no limited char number


class Reply(models.Model):
    post = models.ForeignKey(Post)      # reply to a single post
    author = models.ForeignKey(User)    # who replies
    content = models.CharField(max_length=settings.REPLY_LENGTH_LIMIT)  # content of the reply




