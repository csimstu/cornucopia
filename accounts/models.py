from pip.util import display_path
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

    def __unicode__(self):
        return self.nickname + "'s Profile"

    def get_icon_url(self):
        return "/static/accounts/default_portrait.jpg"


from django.db.models.signals import post_save


def auto_create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        Profile.objects.create(user=user, nickname=user.username)


post_save.connect(auto_create_profile, sender=User)

