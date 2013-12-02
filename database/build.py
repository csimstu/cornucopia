import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeenHope.settings")
from django.db import connection
from TeenHope import settings
from django.core.management import call_command


def recreate_db():
    print "Wiping database..."
    dbinfo = settings.DATABASES['default']

    print "Dropping and creating database" + dbinfo['NAME']
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE " + dbinfo["NAME"] + "; CREATE DATABASE "
                   + dbinfo["NAME"] + "; USE " + dbinfo["NAME"] + ";")
    print "Done."


def add_test_data():

    name_list = ['andrew', 'mike', 'ferona', 'john',
             'smith', 'nyx', 'rubic', 'bat', 'spectre']
    from django.contrib.auth.models import User

    llx = User.objects.create_superuser('csimstu', 'csimstu@gmail.com', '1')

    # creating detailed bio for llx
    prof = llx.get_profile()
    prof.first_name = "Lingxiao"
    prof.last_name = "Li"
    prof.nickname = "Mike Lee"
    prof.website = "http://www.csimstu.com"
    prof.renren = "http://www.renren.cn/1234567"
    prof.qq = "504500868"
    prof.phone = "18908130137"

    prof.motto = "The tragedy of life is not that it ends so soon, but that we wait so long to begin it."
    prof.biography = "Programming in Python, Java, Delphi.\
During my spare time, I take care of my family and write music. You can find some of my compositions here: http://being-without.tumblr.com\
My recent projects include a Multiplayer Browser game (http://alqazar.com) " \
                 "and Social network for people who seek betting advice (https://tipleaders.com). Both of them in django"

    prof.save()


    user = []
    for name in name_list:
        user.append(User.objects.create_user(name, name + '@gmail.com', '1'))


    # create stupid messages
    from network.models import Message
    import datetime

    for x in range(0, 50):
        Message.objects.create(sender=user[2], receiver=llx, unread=True,
                               subject="Drone message #%d" % x,
                               type="MSG")

    from forum.models import Category
    from forum.models import Topic, Post, Reply


    default_cat = Category.objects.create(title="Uncategorized", label="uncategorized")
    cat_new = Category.objects.create(title="A New Category", label="a_new_category")

    for cat in Category.objects.all():
        topic_tmp = Topic.objects.create(category=cat, title="Watch for category %s" % cat.title,
                                         author=llx)
        post_tmp = Post.objects.create(topic=topic_tmp, author=llx,
                                       content="First post by llx! Hoooray!")

    topic1 = Topic.objects.create(title="A Journey Through Beautiful Typography In Web Design",
                                  author=llx)
    post1 = Post.objects.create(topic=topic1, author=llx,
                                content="First post by llx! Hoooray!")
    reply1 = Reply.objects.create(post=post1,author=user[2],content="This is a post with <strong>strong text</strong>")

    topic2 = Topic.objects.create(title="Teaching Web Design To New Students In Higher Education",
                                  author=llx)
    post2 = Post.objects.create(topic=topic2, author=llx,
                                content="Second post by llx! Hoooray!")

    # generator a bunch of topics
    for x in range(0, 10):
        tmp = Topic.objects.create(title="Drone Topic #%d" % x, author=llx)
        for y in range(0, 10):
            tmp2 = Post.objects.create(topic=tmp, author=llx, content="hehe")
            if x != 9:
                break
            if y == 0:
                for z in range(0, 10):
                    Reply.objects.create(post=tmp2, author=llx, content="haha")

    from pages.models import Article, Comment, Tag

    tag1 = Tag.objects.create(author=llx, title="Innovation")
    tag2 = Tag.objects.create(author=llx, title="Web Design")
    tag3 = Tag.objects.create(author=llx, title="Fonts")

    article1 = Article.objects.create(title="Creative And Innovative Navigation Designs ",
                                      author=llx,
                                      content="A website has a personality - it is a "
                                              "reflection of the person or organization behin"
                                              "d it. When people visit your website, you want it to st"
                                              "and out from the crowd, to be memorable. You want people to c"
                                              "ome back and use your website or get in touch with you. So, ...",
    )
    article1.tags.add(tag1, tag2, tag3)

    comment1 = Comment.objects.create(author=user[0], article=article1,
                                      content="Super awesome collection. I love typography. :)"
    )
    comment2 = Comment.objects.create(author=llx, article=article1,
                                      content="This is a <strong>comment</strong>"
    )

    article2 = article1
    article2.pk = None
    article2.date_published = datetime.datetime.now()
    article2.save()

    article3 = article1
    article3.pk = None

    article3.save()
    article3.date_published = datetime.datetime.now() - datetime.timedelta(days=1)
    article3.save()

    article4 = article1
    article4.pk = None

    article4.save()

    article4.date_published = datetime.datetime.now() - datetime.timedelta(days=40)
    article4.save()

    Article.objects.create(title="Creative And Innovative Navigation Designs ",

                                      author=llx,
                                      content="A website has a personality - it is a "
                                              "reflection of the person or organization behin"
                                              "d it. When people visit your website, you want it to st"
                                              "and out from the crowd, to be memorable. You want people to c"
                                              "ome back and use your website or get in touch with you. So, ...",
    )


def main():
    recreate_db()
    print "Syncing DB..."
    call_command('syncdb', interactive=False)
    print "Adding test data..."
    add_test_data()
    print "Building database successfully."

if __name__ == "__main__":
    main()
