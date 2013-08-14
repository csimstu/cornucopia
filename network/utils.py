from network.models import Message
import datetime
from django.core.urlresolvers import reverse

def send_friend_invitation(sender, receiver):
    invitation = Message.objects.create(sender=sender, receiver=receiver,
                           type="INV", unread=True)

    invitation.subject = "%s wants to make friend with you" % sender.get_profile().nickname
    invitation.content = "Click the following url to accept the invitation."\
              + "<a href=" + reverse('network:accept_invitation', kwargs={'user_id': sender.id}) + \
              ">make friend with %s</a>" % sender.get_profile().nickname
    invitation.save()

def send_message(sender, receiver, subject, content):
    Message.objects.create(sender=sender, receiver=receiver,
                           type="MSG", unread=True, subject=subject,
                           content=content)
