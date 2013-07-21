from django.db import models
from django.contrib.auth.models import User
from TeenHope import settings

class Profile(models.Model):
    user = models.OneToOneField(User)       # handle of default User object
    name = models.CharField(max_length=settings.PROFILE_NAME_LENGTH_LIMIT)  # name for display

