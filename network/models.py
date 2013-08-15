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
    articles = models.ManyToManyField(Article)


class RelationList(models.Model):
    # relationships
    # friends: bidirectional
    # followings: one-directional

    holder = models.OneToOneField(User)
    friends = models.ManyToManyField(User, related_name='friends+', through="FriendShip")
    followings = models.ManyToManyField(User, related_name='followed_by')


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='+')
    receiver = models.ForeignKey(User, related_name='+')
    subject = models.CharField(max_length=settings.MESSAGE_SUBJECT_LENGTH_LIMIT)
    content = models.CharField(max_length=settings.MESSAGE_LENGTH_LIMIT)
    date_sent = models.DateTimeField(auto_now_add=True)
    MESSAGE_CHOICES = (
        ('MSG', 'message'),
        ('NTF', 'notification'),
        ('INV', 'invitation'),
    )
    type = models.CharField(max_length=3, choices=MESSAGE_CHOICES, default='MSG')
    unread = models.BooleanField(default=True)
    important = models.BooleanField(default=False)


class FriendGroup(models.Model):
    holder = models.ForeignKey(User)
    name = models.CharField(max_length=settings.GROUP_NAME_LENGTH_LIMIT)
    date_created = models.DateTimeField(auto_now_add=True)


class FriendShip(models.Model):
    relationlist = models.ForeignKey(RelationList)
    target = models.ForeignKey(User)
    group = models.ForeignKey(FriendGroup)


from django.db.models.signals import post_save, pre_save


def auto_add_default_group(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        FriendGroup.objects.create(holder=user, name="default group")


post_save.connect(auto_add_default_group, sender=User)


def auto_create_subscribe_list(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        SubscribeList.objects.create(holder=user)


post_save.connect(auto_create_subscribe_list, sender=User)


def auto_create_relation_list(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        RelationList.objects.create(holder=user)


post_save.connect(auto_create_relation_list, sender=User)


class Trace(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=settings.URL_LENGTH_LIMIT)
    description = models.CharField(max_length=settings.TRACE_DESCRIPTION_LENGTH_LIMIT)
    date = models.DateTimeField(auto_now_add=True)


# Add listeners in order to create trace messages
def create_topic_trace(sender, **kwargs):
    topic = kwargs["instance"]
    if kwargs["created"]:
        Trace.objects.create(user=topic.author,
                             url=topic.get_absolute_url(),
                             description=topic.trace_msg())


post_save.connect(create_topic_trace, sender=Topic)


def create_post_trace(sender, **kwargs):
    post = kwargs["instance"]
    if kwargs["created"]:
        Trace.objects.create(user=post.author,
                             url=post.get_absolute_url(),
                             description=post.trace_msg())


post_save.connect(create_post_trace, sender=Post)

from forum.models import Reply


def create_reply_trace(sender, **kwargs):
    reply = kwargs["instance"]
    if kwargs["created"]:
        Trace.objects.create(user=reply.author,
                             url=reply.get_absolute_url(),
                             description=reply.trace_msg())


post_save.connect(create_reply_trace, sender=Reply)

from pages.models import Comment


def create_article_trace(sender, **kwargs):
    article = kwargs["instance"]
    if kwargs["created"]:
        Trace.objects.create(user=article.author,
                             url=article.get_absolute_url(),
                             description=article.trace_msg())


post_save.connect(create_article_trace, sender=Article)


def create_comment_trace(sender, **kwargs):
    comment = kwargs["instance"]
    if kwargs["created"]:
        Trace.objects.create(user=comment.author,
                             url=comment.get_absolute_url(),
                             description=comment.trace_msg())


post_save.connect(create_comment_trace, sender=Comment)


from network.listeners import topic_subscribe_listener, \
    post_subscribe_listener, article_subscribe_listener, comment_subscribe_listener, reply_subscribe_listener

post_save.connect(topic_subscribe_listener, sender=Topic)
post_save.connect(post_subscribe_listener, sender=Post)
post_save.connect(reply_subscribe_listener, sender=Reply)
post_save.connect(article_subscribe_listener, sender=Article)
post_save.connect(comment_subscribe_listener, sender=Comment)

class EmailHash(models.Model):
    holder = models.OneToOneField(User)
    hash_str = models.CharField(max_length=128)
    gen_date = models.DateTimeField(auto_now = True)
