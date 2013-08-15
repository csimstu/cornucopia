from network.utils import send_notification


def send_mass_notification(users, obj, exl=None):
    for x in users:
        if x != exl:
            send_notification(x, obj.get_subscribe_subject(), obj.get_subscribe_content())


def topic_subscribe_listener(sender, **kwargs):
    # triggered only when created a new topic
    topic = kwargs["instance"]
    if kwargs["created"]:
        list = topic.subscribelist_set.all()
        author = topic.author

        send_mass_notification([x.holder for x in list], topic, author)
        send_mass_notification([x.holder for x in author.followed_by.all()], topic, author)
        send_mass_notification([x for x in author.relationlist.friends.all()], topic, author)


def post_subscribe_listener(sender, **kwargs):
    post = kwargs["instance"]
    if kwargs["created"]:
        list = post.topic.subscribelist_set.all()
        author = post.author

        send_mass_notification([x.holder for x in list], post, author)


def reply_subscribe_listener(sender, **kwargs):
    reply = kwargs["instance"]
    if kwargs["created"]:
        send_notification(reply.post.author, reply.get_subscribe_subject(), reply.get_subscribe_content())


def article_subscribe_listener(sender, **kwargs):
    # triggered when new article published
    article = kwargs["instance"]
    if kwargs["created"]:
        list = article.subscribelist_set.all()
        author = article.author

        send_mass_notification([x.holder for x in list], article, author)
        send_mass_notification([x.holder for x in author.followed_by.all()], article, author)
        send_mass_notification([x for x in author.relationlist.friends.all()], article, author)


def comment_subscribe_listener(sender, **kwargs):
    # response only to author
    comment = kwargs["instance"]
    if kwargs["created"]:
        send_notification(comment.article.author, comment.get_subscribe_subject(), comment.get_subscribe_content())


