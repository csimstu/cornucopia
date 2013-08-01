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
    # customer-sent messages
    sender = models.ForeignKey(User, related_name='+')
    receiver = models.ForeignKey(User, related_name='+')
    content = models.CharField(max_length=settings.MESSAGE_LENGTH_LIMIT)
    unread = models.BooleanField()


class Notification(models.Model):
    # system notifications
    receiver = models.ForeignKey(User)
    content = models.CharField(max_length=settings.MESSAGE_LENGTH_LIMIT)
    unread = models.BooleanField()


class Invitation(models.Model):
    # invite receiver to be a friend of sender
    sender = models.ForeignKey(User, related_name='+')
    receiver = models.ForeignKey(User, related_name='+')
    content = models.CharField(max_length=settings.MESSAGE_LENGTH_LIMIT)
    unread = models.BooleanField()

