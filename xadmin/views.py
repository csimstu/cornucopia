from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from forum.models import *
from pages.models import *
from network.models import RelationList, Message


@login_required
def dashboard(request):
    user = request.user

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

    attention = {
        'unread_msg': Message.objects.filter(receiver=user, unread=True, type="MSG").count(),
        'unread_ntf': Message.objects.filter(receiver=user, unread=True, type="NTF").count(),
        'unread_inv': Message.objects.filter(receiver=user, unread=True, type="INV").count(),
    }

    return render(request, 'xadmin/dashboard.html',
                  {
                      'stat': stat, 'attention': attention,
                  })


from django.core.paginator import Paginator, PageNotAnInteger


@login_required
def inbox(request):
    user = request.user
    msg_list = Message.objects.filter(receiver=user).order_by("-date_sent")
    paginator = Paginator(msg_list, 10)
    page = request.GET.get('page')

    try:
        msgs = paginator.page(page)
    except PageNotAnInteger, EmptyPage:
        msgs = paginator.page(1)

    return render(request, 'xadmin/inbox.html', {'msgs': msgs})


from django.shortcuts import get_object_or_404


@login_required()
def show_msg_in_inbox(request, msg_id):
    msg = get_object_or_404(Message, id=msg_id)
    msg.unread = False
    msg.save()
    return render(request, 'xadmin/show_msg_in_inbox.html', {'msg': msg})


from forms import NewMessageForm,AddConnectionsForm
import datetime
from django.http import HttpResponseRedirect


@login_required()
def send_msg(request):
    user = request.user
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['subject']
            content = cd['content']
            for x in cd['receivers'].split(','):
                receiver = User.objects.get(id=int(x))
                Message.objects.create(sender=user, receiver=receiver,
                                       subject=subject, content=content,
                                       date_sent=datetime.datetime.now(),
                                       type="MSG", unread=True)
            return HttpResponseRedirect(reverse('xadmin:inbox'))
    else:
        form = NewMessageForm()
    return render(request, 'xadmin/send_msg.html',
                  {'form': form})

from network.utils import send_friend_invitation

@login_required()
def add_connections(request):
    user = request.user
    if request.method == 'POST':
        form = AddConnectionsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['friends'] != "":
                for x in cd['friends'].split(','):
                    friend = User.objects.get(id=int(x))
                    send_friend_invitation(user,friend)

            return HttpResponseRedirect(reverse('xadmin:inbox'))
    else:
        form = AddConnectionsForm()
    return render(request, 'xadmin/add_connections.html',
                  {'form': form})

@login_required
def manage_connections(request):
    user = request.user
    friend_list = user.relationlist.friends.all()
    paginator = Paginator(friend_list, 10)
    page = request.GET.get('page')

    try:
        friends = paginator.page(page)
    except PageNotAnInteger, EmptyPage:
        friends = paginator.page(1)

    return render(request, 'xadmin/manage_connections.html', {'friends': friends})

from forum.forms import NewTopicForm

@login_required()
def new_topic(request):
    user = request.user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data['category']
            topic = Topic(title=form.cleaned_data['title'],
                          author=user,
                          date_published=datetime.datetime.now()
            )
            topic.save()
            for x in category:
                topic.category.add(x)

            first_post = Post(topic=topic,
                              author=user,
                              date_published=topic.date_published,
                              content=form.cleaned_data['content'])
            first_post.save()
            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = NewTopicForm()

    return render(request, 'xadmin/new_topic.html', {
        'form': form
    })

from pages.forms import NewArticleForm

@login_required()
def new_article(request):
    user = request.user
    if request.method == 'POST':
        form = NewArticleForm(user=user, data=request.POST)

        if form.is_valid():
            article = Article(title=form.cleaned_data['title'],
                              author=user,
                              content=form.cleaned_data['content'],
                              date_published=datetime.datetime.now()
            )
            article.save()

            tags = form.cleaned_data['tags']
            if tags != "":
                for tag_title in tags.split(','):
                    try:
                        tag = Tag.objects.get(title=tag_title, author=user)
                    except Tag.DoesNotExist:
                        tag = Tag.objects.create(title=tag_title, author=user)

                    article.tags.add(tag)

            return HttpResponseRedirect(article.get_absolute_url())
    else:
        form = NewArticleForm(user)

    return render(request, 'xadmin/new_article.html', {
        'form': form
    })

from forum.models import Topic, Post, Reply
from network.models import Trace
@login_required()
def recent_traces(request):
    user = request.user
    trace_list = Trace.objects.filter(user=user).order_by("-date")
    paginator = Paginator(trace_list, 10)
    page = request.GET.get('page')

    try:
        traces = paginator.page(page)
    except PageNotAnInteger, EmptyPage:
        traces = paginator.page(1)

    return render(request, 'xadmin/recent_traces.html', {'traces': traces})

from accounts.forms import ProfileForm

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(user=request.user, data=request.POST)
        profile = user.get_profile()

        if form.is_valid():
            if form.cleaned_data['new_password'] is not None\
                and len(form.cleaned_data['new_password']) > 0:
                user.set_password(form.cleaned_data['new_password'])
            user.email = form.cleaned_data['email']
            user.save()

            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.nickname = form.cleaned_data['nickname']
            profile.website = form.cleaned_data['website']
            profile.renren = form.cleaned_data['renren']
            profile.qq = form.cleaned_data['qq']
            profile.phone = form.cleaned_data['phone']
            profile.biography = form.cleaned_data['biography']
            profile.motto = form.cleaned_data['motto']

            profile.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        profile = user.get_profile()
        form = ProfileForm(initial={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'nickname': profile.nickname,
            'website': profile.website,
            'renren': profile.renren,
            'qq': profile.qq,
            'phone': profile.phone,
            'biography': profile.biography,
            'motto': profile.motto,
            'email': user.email},)

    return render(request, 'xadmin/update_profile.html', {
        'form': form,
    })