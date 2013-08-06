import os
from TeenHope import settings

name_list = ['andrew', 'mike', 'ferona', 'john',
             'smith', 'nyx', 'rubic', 'bat', 'spectre']

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
    user = []
    for name in name_list:
        user.append(User.objects.create_user(name, name + '@gmail.com', '1'))


    # create stupid messages
    from network.models import Message
    import datetime
    for x in range(0, 50):
        Message.objects.create(sender=user[2], receiver=llx, unread=True,
                               subject="Drone message #%d" % x,
                               date_sent=datetime.datetime.now(),
                               type="MSG")

    from forum.models import Category
    default_cat = Category.objects.create(title="default")

    from forum.models import Topic, Post
    topic1 = Topic.objects.create(title="Topic Test",
                         date_published=datetime.datetime.now(),
                         author=llx)
    topic1.category.add(default_cat)
    post1 = Post.objects.create(topic=topic1, author=llx, date_published=datetime.datetime.now(),
                                content="First post by llx! Hoooray!")