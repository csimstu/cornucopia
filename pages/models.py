from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from TeenHope import settings


class Tag(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=settings.TAG_LENGTH_LIMIT)

    def __unicode__(self):
        return self.title

    def count(self):
        return self.article_set.count()


class Article(models.Model):
    author = models.ForeignKey(User)
    date_published = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=settings.ARTICLE_TITLE_LENGTH_LIMIT)
    content = models.TextField(max_length=settings.ARTICLE_LENGTH_LIMIT)
    tags = models.ManyToManyField(Tag)
    abstract = models.CharField(max_length=settings.ABSTRACT_LENGTH_LIMIT)

    def __unicode__(self):
        return "Article: " + self.title

    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'article_id': self.id})

    def trace_msg(self):
        return "Create article#%d <strong>%s</strong>" % (self.id, self.title)

    def get_subscribe_subject(self):
        return "%s has created a new article" % self.author.get_profile().nickname

    def get_subscribe_content(self):
        return "<a href=%s>Click here to view</a>" % self.get_absolute_url()


class Comment(models.Model):
    author = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    date_published = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=settings.COMMENT_LENGTH_LIMIT)

    def __unicode__(self):
        return "Comment #%d for Article %s" % (self.id, self.article.title)

    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'article_id': self.article.id})

    def trace_msg(self):
        return "Post a comment(#%d) on article <strong>%s</strong>" % (self.id, self.article.title)

    def get_subscribe_subject(self):
        return "%s has created a new comment" % self.author.get_profile().nickname

    def get_subscribe_content(self):
        return "<a href=%s>Click here to view</a>" % self.get_absolute_url()
