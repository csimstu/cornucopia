from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from TeenHope import settings
from django.db.models.signals import post_save
import datetime

class Category(models.Model):
    title = models.CharField(max_length=settings.CATEGORY_TITLE_LENGTH_LIMIT)  # title of the category
    label = models.CharField(max_length=settings.CATEGORY_LABEL_LENGTH_LIMIT)
    description = models.CharField(default="Description goes here...", max_length=settings.CATEGORY_DESCRIPTION_LENGTH_LIMIT)
    topic_cnt = models.IntegerField(default=0)
    post_cnt = models.IntegerField(default=0)
    last_editor_id = models.IntegerField(default=0)
    last_modified_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ""


class Topic(models.Model):
    category = models.ForeignKey(Category, default=1)     # one topic belongs to only one kind
    title = models.CharField(max_length=settings.TOPIC_TITLE_LENGTH_LIMIT)         # title of the topic
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return "Topic: " + self.title

    def get_absolute_url(self):
        return reverse('forum:topic_detail', kwargs={'topic_id': self.id})

    def trace_msg(self):
        return "Create topic#%d <strong>%s</strong>" % (self.id, self.title)

    def get_participants(self):
        return [y.author for y in self.post_set.all()]

    def get_subscribe_subject(self):
        return "%s has created a new topic" % self.author.get_profile().nickname

    def get_subscribe_content(self):
        return "<a href=%s>Click here to view</a>" % self.get_absolute_url()

    def get_last_post(self):
        return self.post_set.order_by('-date_published')[0]


class Post(models.Model):
    topic = models.ForeignKey(Topic)    # a post belongs to only one topic
    author = models.ForeignKey(User)    # the writer of the post
    date_published = models.DateTimeField(auto_now_add=True)         # time published
    content = models.CharField(
        max_length=settings.POST_LENGTH_LIMIT)        # content of the post, no limited char number

    def __unicode__(self):
        return "Post #%d for Topic %s" % (self.id, self.topic.title)

    def get_absolute_url(self):
        return reverse('forum:topic_detail', kwargs={'topic_id': self.topic.id})

    def trace_msg(self):
        return "Follow up#%d for topic <strong>%s</strong>" % (self.id, self.topic.title)

    def get_subscribe_subject(self):
        return "%s has created a new post" % self.author.get_profile().nickname

    def get_subscribe_content(self):
        return "<a href=%s>Click here to view</a>" % self.get_absolute_url()


class Reply(models.Model):
    post = models.ForeignKey(Post)      # reply to a single post
    author = models.ForeignKey(User)    # who replies
    date_published = models.DateTimeField(auto_now_add=True) # time published
    content = models.CharField(max_length=settings.REPLY_LENGTH_LIMIT)  # content of the reply

    def __unicode(self):
        return "A reply by " + self.author.name

    def trace_msg(self):
        return "Reply#%d to post#%d of topic <strong>%s</strong>" % (self.id, self.post.id, self.post.topic.title)

    def get_absolute_url(self):
        return self.post.get_absolute_url()

    def get_subscribe_subject(self):
        return "%s has replied your post" % self.author.get_profile().nickname

    def get_subscribe_content(self):
        return "<a href=%s>Click here to view</a>" % self.get_absolute_url()


def listen_to_topic(sender, **kwargs):
    topic = kwargs["instance"]
    if kwargs["created"]:
        cat = topic.category
        cat.topic_cnt += 1
        cat.save()

post_save.connect(listen_to_topic, sender=Topic)

def listen_to_post(sender, **kwargs):
    post = kwargs["instance"]
    if kwargs["created"]:
        topic = post.topic
        cat = topic.category
        cat.post_cnt += 1
        cat.last_editor_id = post.author.id
        cat.last_modified_time = post.date_published
        cat.save()

post_save.connect(listen_to_post, sender=Post)

