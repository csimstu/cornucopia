import os
import settings

try:
    with open(settings.DATABASES['default']['NAME']):
        pass
    print 'Database already exists.'
except IOError:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeenHope.settings")
    from django.core.management import call_command
    call_command('syncdb', interactive=False)

    from django.contrib.auth.models import User
    llx = User.objects.create_superuser('csimstu', 'csimstu@gmail.com', '1')
    llx2 = User.objects.create_user('sabolaji', 'sabolaji@gmail.com', '1')


    # create stupid messages
    from network.models import Message
    import datetime
    for x in range(0, 50):
        Message.objects.create(sender=llx2, receiver=llx, unread=True,
                               subject="Drone message #%d" % x,
                               date_sent=datetime.datetime.now(),
                               type="MSG")
