from django.db import models
from django.contrib.auth.models import User
from TeenHope import settings


class Profile(models.Model):
    user = models.OneToOneField(User)       # handle of default User object
    first_name = models.CharField(max_length=settings.PROFILE_NAME_LENGTH_LIMIT)
    last_name = models.CharField(max_length=settings.PROFILE_NAME_LENGTH_LIMIT)
    nickname = models.CharField(max_length=settings.PROFILE_NAME_LENGTH_LIMIT)

    website = models.CharField(max_length=settings.WEBSITE_LENGTH_LIMIT)
    renren = models.CharField(max_length=settings.RENREN_LENGTH_LIMIT)
    qq = models.CharField(max_length=settings.QQ_LENGTH_LIMIT)
    phone = models.CharField(max_length=settings.PHONE_LENGTH_LIMIT)

    biography = models.CharField(max_length=settings.BIOGRAPHY_LENGTH_LIMIT)
    motto = models.CharField(max_length=settings.MOTTO_LENGTH_LIMIT)
