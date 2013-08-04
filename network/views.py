from django.contrib.auth.models import User
from accounts.models import Profile
import json
from django.http import HttpResponse, Http404


def get_receiver_list(request):
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

def get_initial_receiver(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        results = []
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
