from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from forms import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return HttpResponseRedirect(reverse('home'))
            else:
                return activate(request)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'login_form': form,
    })

@login_required()
def logout(request):
    auth.logout(request)
    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET['next'])
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
            user.is_active = False
            user.save()

            return activate(request, user)

            #auth.login(request, user)
            #if 'next' in request.GET:
            #    return HttpResponseRedirect(request.GET['next'])
            #return HttpResponseRedirect(reverse('home'))
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {
        'register_form': form,
    })

def activate(request, user):
    from xadmin.views import activate_send_email
    activate_send_email(request, user)
    return render(request, 'accounts/activate.html')

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
    has_login = request.user.is_authenticated()
    is_friend = False
    if request.user.is_authenticated():
        if request.user.relationlist.friends.filter(id=user.id).count() > 0\
            or request.user.id == user.id:
            is_friend = True

    has_followed = False
    if request.user.is_authenticated():
        if request.user.relationlist.followings.filter(id=user.id).count() > 0\
        or request.user.id == user.id:
            has_followed = True

    topic_list = Topic.objects.filter(author=user).order_by('-date_published')[:5]
    post_list = Post.objects.filter(author=user).order_by('-date_published')[:5]
    article_list = Article.objects.filter(author=user).order_by('-date_published')[:5]
    comment_list = Comment.objects.filter(author=user).order_by('-date_published')[:5]
    tag_list = Tag.objects.filter(author=user)[:10]


    return render(request, 'accounts/view_profile.html', {
        'this_user': user,
        'profile': profile,
        'stat': stat,
        'has_login': has_login,
        'is_friend': is_friend,
        'has_followed': has_followed,
        'topic_list': topic_list,
        'post_list': post_list,
        'article_list': article_list,
        'comment_list': comment_list,
        'tag_list': tag_list,
    })


from accounts.forms import ForgetPasswordForm
def forget_password(request):
    if request.method == "POST":
        fpf = ForgetPasswordForm(request.POST)
        if fpf.is_valid():
            user = User.objects.get(username = fpf.cleaned_data['username'])
            if user and user.email == fpf.cleaned_data['email']:
                from xadmin.views import _chpsw_sendmail
                return _chpsw_sendmail(request,user,reverse("accounts:forget_password"))
    return render(request, 'accounts/forgot_password.html')
