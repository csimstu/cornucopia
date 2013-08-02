from django.db import models
from django.contrib.auth.models import User
from forum.models import Topic, Post
from pages.models import Article
from TeenHope import settings


class SubscribeList(models.Model):
    # subscribe
    # topic: notify every new post
    # post: notify every new reply
    # article: notify every new comment

    holder = models.OneToOneField(User)
    topics = models.ManyToManyField(Topic)
    posts = models.ManyToManyField(Post)
    articles = models.ManyToManyField(Article)


class RelationList(models.Model):
    # relationships
    # friends: bidirectional
    # followings: one-directional

    holder = models.OneToOneField(User)
    friends = models.ManyToManyField(User, related_name='friends+')
    followings = models.ManyToManyField(User, related_name='followings+')


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='+')
    receiver = models.ForeignKey(User, related_name='+')
    content = models.CharField(max_length=settings.MESSAGE_LENGTH_LIMIT)
    MESSAGE_CHOICES = (
        ('MSG', 'message'),
        ('NTF', 'notification'),
        ('INV', 'invitation'),
    )
    type = models.CharField(max_length=3, choices=MESSAGE_CHOICES, default='MSG')
    unread = models.BooleanField()
