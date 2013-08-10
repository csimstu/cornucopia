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
    from forum.models import Topic, Post


    default_cat = Category.objects.create(title="Uncategorized", label="uncategorized")
    cat_new = Category.objects.create(title="A New Category", label="a_new_category")

    for cat in Category.objects.all():
        topic_tmp = Topic.objects.create(category=cat, title="Watch for category %s" % cat.title,
                                         date_published=datetime.datetime.now(),
                                         author=llx)
        post_tmp = Post.objects.create(topic=topic_tmp, author=llx, date_published=datetime.datetime.now(),
                                       content="First post by llx! Hoooray!")

    topic1 = Topic.objects.create(title="A Journey Through Beautiful Typography In Web Design",
                                  date_published=datetime.datetime.now(),
                                  author=llx)
    post1 = Post.objects.create(topic=topic1, author=llx, date_published=datetime.datetime.now(),
                                content="First post by llx! Hoooray!")

    topic2 = Topic.objects.create(title="Teaching Web Design To New Students In Higher Education",
                                  date_published=datetime.datetime.now(),
                                  author=llx)
    post2 = Post.objects.create(topic=topic2, author=llx, date_published=datetime.datetime.now(),
                                content="Second post by llx! Hoooray!")

    from pages.models import Article, Comment, Tag

    tag1 = Tag.objects.create(author=llx, title="Innovation")
    tag2 = Tag.objects.create(author=llx, title="Web Design")
    tag3 = Tag.objects.create(author=llx, title="Fonts")

    article1 = Article.objects.create(title="Creative And Innovative Navigation Designs "
                                            "Creative And Innovative Navigation Designs",
                                      author=llx, date_published=datetime.datetime.now(),
                                      content="A website has a personality - it is a "
                                              "reflection of the person or organization behin"
                                              "d it. When people visit your website, you want it to st"
                                              "and out from the crowd, to be memorable. You want people to c"
                                              "ome back and use your website or get in touch with you. So, ...",
    )
    article1.tags.add(tag1, tag2, tag3)

    comment1 = Comment.objects.create(author=user[0], article=article1,
                                      date_published=datetime.datetime.now(),
                                      content="Super awesome collection. I love typography. :)"
    )

    article2 = article1
    article2.pk = None
    article2.date_published = datetime.datetime.now();
    article2.save()