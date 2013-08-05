from django.contrib.auth.models import User
from accounts.models import Profile
import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse


def search_user_thumb_list(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        user_list = User.objects.filter(username__icontains=q)
        results = []
        for user in user_list:
            user_json = {}
            user_json['label'] = user.get_profile().nickname
            user_json['value'] = user.username
            user_json['icon_url'] = user.get_profile().get_icon_url()
            user_json['id'] = user.id
            results.append(user_json)
        data = json.dumps(results)
        return HttpResponse(data, mimetype='application/json')
    return Http404()

def search_user_thumb_list_exclude(request):
    user = request.user
    if request.is_ajax():
        q = request.GET.get('term', '')
        user_list = User.objects.filter(username__icontains=q)
        user_list = user_list.exclude(id__in=[t.id for t in user.relationlist.friends.all()])
        user_list = user_list.exclude(id=user.id)

        results = []
        for user in user_list:
            user_json = {}
            user_json['label'] = user.get_profile().nickname
            user_json['value'] = user.username
            user_json['icon_url'] = user.get_profile().get_icon_url()
            user_json['id'] = user.id
            results.append(user_json)
        data = json.dumps(results)
        return HttpResponse(data, mimetype='application/json')
    return Http404()

def get_user_thumb_by_id(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        results = []
        if q is not None and q != "":
            for x in q.split(','):
                user = User.objects.get(id=int(x))
                user_json = {}
                user_json['label'] = user.get_profile().nickname
                user_json['value'] = user.username
                user_json['icon_url'] = user.get_profile().get_icon_url()
                user_json['id'] = user.id
                results.append(user_json)

        return HttpResponse(json.dumps(results), mimetype='application/json')
    return Http404()

from network.models import Message


def accept_invitation(request, user_id):
    p1 = request.user
    p2 = User.objects.get(id=user_id)
    try:
        Message.objects.get(type="INV", sender=p2, receiver=p1)
    except Message.DoesNotExist:
        return Http404()
    p1.relationlist.friends.add(p2)
    p2.relationlist.friends.add(p1)

    return HttpResponseRedirect(reverse('xadmin:inbox'))
