from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from TeenHope import settings


class Tag(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=settings.TAG_LENGTH_LIMIT)

    def __unicode__(self):
        return self.title


from django.db.models.signals import post_save


def auto_create_default_tag(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        Tag.objects.create(author=user, title="default")


post_save.connect(auto_create_default_tag, sender=User)


class Article(models.Model):
    author = models.ForeignKey(User)
    date_published = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=settings.ARTICLE_TITLE_LENGTH_LIMIT)
    content = models.CharField(max_length=settings.ARTICLE_LENGTH_LIMIT)
    tags = models.ManyToManyField(Tag)

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