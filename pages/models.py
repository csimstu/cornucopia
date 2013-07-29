from django.db import models
from django.contrib.auth.models import User
from TeenHope import settings
from django.core.urlresolvers import reverse

class Tag(models.Model):
    title = models.CharField(max_length=settings.TAG_LENGTH_LIMIT)

    def __unicode__(self):
        return self.title

class Article(models.Model):
    author = models.ForeignKey(User)
    date_published = models.DateTimeField()
    title = models.CharField(max_length=settings.ARTICLE_TITLE_LENGTH_LIMIT)
    content = models.CharField(max_length=settings.ARTICLE_LENGTH_LIMIT)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return "Article: " + self.title

    def get_absolute_url(self):
        return reverse('pages:detail', kwargs={'article_id': self.id})


class Comment(models.Model):
    author = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    date_published = models.DateTimeField()
    content = models.CharField(max_length=settings.COMMENT_LENGTH_LIMIT)

    def __unicode__(self):
        return "Comment #%d for Article %s" % (self.id, self.article.title)