from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from TeenHope import settings


class Category(models.Model):
    title = models.CharField(max_length=settings.CATEGORY_TITLE_LENGTH_LIMIT)  # title of the category

    def __unicode__(self):
        return self.title


class Topic(models.Model):
    category = models.ManyToManyField(Category)     # one topic might belong to many kinds
    title = models.CharField(max_length=settings.TOPIC_TITLE_LENGTH_LIMIT)         # title of the topic
    date_published = models.DateTimeField()
    author = models.ForeignKey(User)

    def __unicode__(self):
        return "Topic: " + self.title

    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'topic_id': self.id})

    def trace_msg(self):
        return "Create topic#%d <strong>%s</strong>" % (self.id, self.title)


class Post(models.Model):
    topic = models.ForeignKey(Topic)    # a post belongs to only one topic
    author = models.ForeignKey(User)    # the writer of the post
    date_published = models.DateTimeField()         # time published
    content = models.CharField(
        max_length=settings.POST_LENGTH_LIMIT)        # content of the post, no limited char number

    def __unicode__(self):
        return "Post #%d for Topic %s" % (self.id, self.topic.title)

    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'topic_id': self.topic.id})

    def trace_msg(self):
        return "Follow up#%d for topic <strong>%s</strong>" % (self.id, self.topic.title)


class Reply(models.Model):
    post = models.ForeignKey(Post)      # reply to a single post
    author = models.ForeignKey(User)    # who replies
    date_published = models.DateTimeField() # time published
    content = models.CharField(max_length=settings.REPLY_LENGTH_LIMIT)  # content of the reply

    def __unicode(self):
        return "A reply by " + self.author.name

    def trace_msg(self):
        return "Reply#%d to post#%d of topic <strong>%s</strong>" % (self.id, self.post.id, self.post.author.title)




