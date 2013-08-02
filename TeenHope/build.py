import os
import settings
try:
    with open(settings.DATABASES['default']['NAME']):
        pass
    print 'Database already exists.'
except IOError:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeenHope.settings")
    from django.core.management import call_command
    from django.contrib.auth.models import User
    from accounts.models import Profile
    call_command('syncdb', interactive=False)
    me = User.objects.create_superuser('csimstu', 'csimstu@gmail.com', '1')
    Profile.objects.create(user=me, nickname=me.username)