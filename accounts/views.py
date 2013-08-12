from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from forms import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'login_form': form,
    })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))


from forms import RegistrationForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']
            )
            user.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            auth.login(request, user)
            return HttpResponseRedirect(reverse("home"))
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {
        'register_form': form,
    })


from django.shortcuts import get_object_or_404
from forum.models import *
from pages.models import *
from network.models import *

def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.get_profile()
    stat = {
        'topic_cnt': Topic.objects.filter(author=user).count(),
        'post_cnt': Post.objects.filter(author=user).count(),
        'reply_cnt': Reply.objects.filter(author=user).count(),
        'article_cnt': Article.objects.filter(author=user).count(),
        'comment_cnt': Comment.objects.filter(author=user).count(),
        'tag_cnt': Tag.objects.filter(author=user).count(),
        'friend_cnt': user.relationlist.friends.count(),
        'following_cnt': user.relationlist.followings.count(),
        'follower_cnt': RelationList.objects.filter(followings=user).count(),
    }
    is_friend = False
    if request.user.is_authenticated():
        if request.user.relationlist.friends.filter(id=user.id).count() > 0\
            or request.user.id == user.id:
            is_friend = True

    has_followed = False
    if request.user.is_authenticated():
        if user.relationlist.followings.filter(id=request.user.id).count() > 0\
        or request.user.id == user.id:
            has_followed = True

    return render(request, 'accounts/view_profile.html', {
        'this_user': user,
        'profile': profile,
        'stat': stat,
        'is_friend': is_friend,
        'has_followed': has_followed,
    })

