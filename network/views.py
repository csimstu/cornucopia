import json

from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from network.models import Message
from django.contrib import messages
from network.models import FriendShip

def accept_invitation(request, user_id):
    p1 = request.user
    p2 = User.objects.get(id=user_id)

    if Message.objects.filter(type="INV", sender=p2, receiver=p1).count():
        if p1.relationlist.friends.filter(id=p2.id).count() == 0:
            FriendShip.objects.create(relationlist=p1.relationlist, target=p2, group=p1.friendgroup_set.all()[0])
        if p2.relationlist.friends.filter(id=p1.id).count() == 0:
            FriendShip.objects.create(relationlist=p2.relationlist, target=p1, group=p2.friendgroup_set.all()[0])

        messages.success(request, '<i class="icon-ok"></i> You and %s become friends.' % p2.get_profile().nickname)

    return HttpResponseRedirect(reverse('xadmin:inbox'))


from network.utils import send_message


def send_message_single(request):
    user = request.user
    if request.method == 'POST':
        receiver = User.objects.get(id=request.POST['receiver_id'])
        send_message(user, receiver, request.POST['subject'], request.POST['content'])
        return HttpResponse("Message to %s sent." % receiver.get_profile().nickname)
    raise Http404()

import json

def send_message_selected(request):
    user = request.user
    if request.method == 'POST':
        receiver_list = json.loads(request.POST['recv_list'])
        for recv in receiver_list:
            if recv["type"] == "friend":
                receiver = User.objects.get(id = recv["id"])
                send_message(user,receiver,request.POST['subject'],request.POST['content'])
        return HttpResponse("Messages sent.")
    raise Http404()


def _remove_friend(request,user1,user2):
    send_message(user1, user2, 'Canceling connection',
                'Sadly, %s has broken the relationship'
                ' with you.' % user1.get_profile().nickname)
    messages.success(request, "You have broken up relationship with %s."
                        % user2.get_profile().nickname)
    
    FriendShip.objects.filter(relationlist=user1.relationlist, target=user2).delete()
    FriendShip.objects.filter(relationlist=user2.relationlist, target=user1).delete()


def remove_friend(request):
    user = request.user
    if request.method == 'GET':
        q = request.GET.get('term', '')
        tmp = User.objects.get(id=int(q))
        _remove_friend(request,user,tmp)
        return HttpResponseRedirect(reverse('xadmin:manage_connections'))
    raise Http404()

import datetime
from network import utils

def send_invitation(request):
    user = request.user
    if request.method == 'POST':
        receiver = User.objects.get(id=request.POST['receiver_id'])
        utils.send_friend_invitation(user, receiver, request.POST['content'])
        return HttpResponse("Invitation for %s sent." % receiver.get_profile().nickname)
    raise Http404()


def add_follow(request):
    user = request.user
    if request.method == 'GET':
        receiver = User.objects.get(id=request.GET['receiver_id'])
        user.relationlist.followings.add(receiver)
        return HttpResponse("Successfully add %s to your following list." % receiver.get_profile().nickname)
    raise Http404()

from forum.models import Topic
from pages.models import Article

@login_required()
def subscribe_topic(request):
    user = request.user
    if request.method == 'GET':
        topic = get_object_or_404(Topic, id=request.GET['topic_id'])
        user.subscribelist.topics.add(topic)
        return HttpResponse()
    raise Http404()

@login_required()
def unsubscribe_topic(request):
    user = request.user
    if request.method == 'GET':
        topic = get_object_or_404(Topic, id=request.GET['topic_id'])
        user.subscribelist.topics.remove(topic)
        return HttpResponse()
    raise Http404()

@login_required()
def subscribe_article(request):
    user = request.user
    if request.method == 'GET':
        article = get_object_or_404(Article, id=request.GET['article_id'])
        user.subscribelist.articles.add(article)
        return HttpResponse()
    raise Http404()

@login_required()
def unsubscribe_article(request):
    user = request.user
    if request.method == 'GET':
        article = get_object_or_404(Article, id=request.GET['article_id'])
        user.subscribelist.articles.remove(article)
        return HttpResponse()
    raise Http404()
