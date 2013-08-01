from django.contrib.auth.models import User
from accounts.models import Profile
from django.db import connection

try:
    llx = User.objects.get(username__exact="csimstu")
    try:
        llx.get_profile()
    except Profile.DoesNotExist:
        Profile.objects.create(user=llx, nickname=llx.username)
except Exception as e:
    print e