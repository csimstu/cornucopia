from django.core.urlresolvers import reverse

from network.models import Message


def send_friend_invitation(sender, receiver):
    invitation = Message.objects.create(sender=sender, receiver=receiver,
                                        type="INV")

    invitation.subject = "%s wants to make friend with you" % sender.get_profile().nickname
    invitation.content = "Click the following url to accept the invitation." \
                         + "<a href=" + reverse('network:accept_invitation', kwargs={'user_id': sender.id}) + \
                         ">make friend with %s</a>" % sender.get_profile().nickname
    invitation.save()


def send_message(sender, receiver, subject, content):
    Message.objects.create(sender=sender, receiver=receiver,
                           type="MSG", subject=subject,
                           content=content)


def send_notification(receiver, subject, content):
    Message.objects.create(sender=receiver, receiver=receiver,
                           type="NTF", subject=subject,
                           content=content)


from forum.models import Topic
from pages.models import Article
from django.shortcuts import get_object_or_404


def subscribe_topic(user, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    user.subscribelist.topics.add(topic)


def subscribe_article(user, article_id):
    article = get_object_or_404(Article, id=article_id)
    user.subscribelist.articles.add(article)