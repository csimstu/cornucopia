import re
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from TeenHope import settings
from django.core.urlresolvers import reverse

class Profile(models.Model):
    user = models.OneToOneField(User)       # handle of default User object
    first_name = models.CharField(max_length=settings.PROFILE_NAME_LENGTH_LIMIT)
    last_name = models.CharField(max_length=settings.PROFILE_NAME_LENGTH_LIMIT)
    nickname = models.CharField(max_length=settings.PROFILE_NAME_LENGTH_LIMIT)
    thumbnail = models.ImageField(upload_to="thumbnail",
                                  default=settings.DEFAULT_USER_THUMBNAIL)

    website = models.CharField(max_length=settings.WEBSITE_LENGTH_LIMIT)
    renren = models.CharField(max_length=settings.RENREN_LENGTH_LIMIT)
    qq = models.CharField(max_length=settings.QQ_LENGTH_LIMIT)
    phone = models.CharField(max_length=settings.PHONE_LENGTH_LIMIT)

    biography = models.CharField(max_length=settings.BIOGRAPHY_LENGTH_LIMIT)
    motto = models.CharField(max_length=settings.MOTTO_LENGTH_LIMIT)

    def __unicode__(self):
        return self.nickname + "'s Profile"

    def get_unread_message_cnt(self):
        from network.models import Message

        return Message.objects.filter(receiver=self.user, unread=True).count()


    def get_absolute_url(self):
        return reverse('accounts:view_profile', kwargs={'user_id': self.id})




from django.db.models.signals import post_save


def auto_create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        Profile.objects.create(user=user, nickname=user.username)


post_save.connect(auto_create_profile, sender=User)


def validate_username(username):
    if not username:
        raise ValidationError("Username cannot be none.")
    if not re.compile(settings.USERNAME_PATTERN).match(username):
        raise ValidationError(settings.USERNAME_HINT)


def validate_password(password):
    if not password:
        raise ValidationError("Password cannot be none.")
    if not re.compile(settings.PASSWORD_PATTERN).match(password):
        raise ValidationError(settings.PASSWORD_HINT)


def validate_email(email):
    if not email:
        raise ValidationError("Email is required.")
    if not re.compile(settings.EMAIL_PATTERN).match(email):
        raise ValidationError("Invalid email format.")


def validate_nickname(nickname):
    if not nickname:
        raise ValidationError("Nickname is required.")
    if not re.compile(settings.NICKNAME_PATTERN).match(nickname):
        raise ValidationError("Invalid nickname.")


def validate_website(website):
    if not re.compile(settings.WEBSITE_PATTERN).match(website):
        raise ValidationError('Invalid website.')