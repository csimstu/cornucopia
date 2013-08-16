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
from xadmin.utils import get_ck_list,encode_ck_list

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

    ck_list = get_ck_list(request.session.get(settings.CKBOX_SESSION_NAME))

    for m in msgs:
        m.checked = m.id in ck_list

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
from django.http import HttpResponseRedirect,HttpResponse


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

from network.models import FriendGroup,FriendShip

@login_required
def manage_connections(request):
    user = request.user
    group_list = FriendGroup.objects.filter(holder = user).order_by("name")

    groups = []
    for g in group_list:
        cgr = {}
        cgr["name"] = g.name
        cgr["id"] = g.id
        cgr["friends"] = []
        for f in user.relationlist.friendship_set.filter(group = g).order_by("target"):
            cgr["friends"].append(f.target)

        groups.append(cgr)

    return render(request, 'xadmin/manage_connections.html', {'groups' : groups})

from xadmin.forms import NewTopicForm

@login_required()
def new_topic(request):
    user = request.user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data['category']
            topic = Topic(title=form.cleaned_data['title'],
                          author=user,
                          category=category
            )
            topic.save()

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
                              abstract=form.cleaned_data['abstract'],
                              content=form.cleaned_data['content'],
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

from xadmin.forms import ProfileForm

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        profile = user.get_profile()

        if form.is_valid():
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

            thumbnail = request.FILES.get('thumbnail', None)
            if thumbnail is not None:
                with open('thumbnail.upload', 'wb+') as des:
                    for chunk in thumbnail.chunks():
                        des.write(chunk)
                des.close()
                from django.core.files import File

                f = File(open('thumbnail.upload', 'r'))
                profile.thumbnail.save('thumbnail/' + user.username,
                                       f)

            profile.save()
            from django.contrib import messages
            messages.success(request, "Your profile has been updated.")
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

from TeenHope import settings

@login_required
def on_checkbox(request):
    if request.method == 'GET':
        ck_id = int(request.GET.get("msg_id"))
        ck_list = get_ck_list(request.session.get(settings.CKBOX_SESSION_NAME))

        if ck_id in ck_list:
            ck_list.remove(ck_id)
        else:
            ck_list.append(ck_id)

        request.session[settings.CKBOX_SESSION_NAME] = encode_ck_list(ck_list)
    return HttpResponse("")


def _ckbox_select(request,page,flag):
    user = request.user
    msg_list = Message.objects.filter(receiver=user).order_by("-date_sent")
    paginator = Paginator(msg_list, 10)

    try:
        msgs = paginator.page(page)
    except:
        msgs = paginator.page(1)

    ck_list= get_ck_list(request.session.get(settings.CKBOX_SESSION_NAME))

    for m in msgs:
        if m.id in ck_list:
            ck_list.remove(m.id)
        if flag:
            ck_list.append(m.id)
    request.session[settings.CKBOX_SESSION_NAME] = encode_ck_list(ck_list)
    return HttpResponse("")


@login_required
def ckbox_select_all(request,page):
    return _ckbox_select(request,page,True)

@login_required
def ckbox_unselect_all(request,page):
    return _ckbox_select(request,page,False)

@login_required
def ckbox_remove(request):
    ck_list = get_ck_list(request.session.get(settings.CKBOX_SESSION_NAME))
    for ck_id in ck_list:
        Message.objects.get(id = ck_id).delete()
    request.session[settings.CKBOX_SESSION_NAME] = encode_ck_list([])
    return HttpResponseRedirect(reverse("xadmin:inbox"))

def _ckbox_mark_flag(request,flag):
    ck_list = get_ck_list(request.session.get(settings.CKBOX_SESSION_NAME))
    for ck_id in ck_list:
        a = Message.objects.get(id = ck_id)
        a.important = flag
        a.save()
    return HttpResponse("")

@login_required
def ckbox_mark(request):
    return _ckbox_mark_flag(request,True)

@login_required
def ckbox_unmark(request):
    return _ckbox_mark_flag(request,False)


from xadmin.forms import InboxSearchForm
from django.contrib import messages

@login_required
def inbox_search(request):
    if request.method == "GET":
        isf = InboxSearchForm(request.GET)

        if isf.is_valid():
            is_marked = isf.cleaned_data['is_marked']
            is_unread = isf.cleaned_data['is_unread']
            content = isf.cleaned_data['content']

            msg_list = Message.objects.filter(subject__icontains=content,unread=is_unread,important=is_marked).order_by("-date_sent")
            paginator = Paginator(msg_list,10)

            page = request.GET.get("page")
            try:
                msgs = paginator.page(page)
            except PageNotAnInteger,EmptyPage:
                msgs = paginator.page(1)
            
            GET_data = request.GET.copy()

            if GET_data.has_key('page'):
                del GET_data['page']

            return render(request,'xadmin/inbox.html',{
                'msgs':msgs,
                'GET_data':GET_data
            })
        else:
            messages.error(request,"Error : Invalid search!")
        return HttpResponseRedirect(reverse("xadmin:inbox"))

    return HttpRepsonse("")


def _inbox_mark_one_flag(request,flag):
    if request.method == 'GET':
        msg_id = int(request.GET.get("msg_id"))
        m = Message.objects.get(id = msg_id)
        m.important = flag
        m.save()
    return HttpResponse("")

@login_required
def inbox_mark_one(request):
    return _inbox_mark_one_flag(request,True)

@login_required
def inbox_unmark_one(request):
    return _inbox_mark_one_flag(request,False)


from django.core.mail import send_mail,EmailMultiAlternatives
from hashlib import sha1
from network.models import EmailHash
import random
import time
import urllib

def _chpsw_sendmail(request,user,rurl):
    user_email = user.email
    chpsw_url = "http://"
    chpsw_url += request.META['HTTP_HOST']
    chpsw_url += reverse("xadmin:chpsw_ckhash")
    
    old_hash_list = EmailHash.objects.filter(holder = user)
    if old_hash_list:
        old_hash_list.delete()

    random.seed(time.time())
    hash_str = ""
    for i in range(0,100):
        c = random.randint(0,25)
        c = chr(ord('a') + c)
        hash_str += c
    hash_str = sha1(hash_str).hexdigest()
    
    es = EmailHash(holder = user,hash_str = hash_str)
    es.save()

    chpsw_url += "?"
    chpsw_url += urllib.urlencode({
        "key" : hash_str,
        "usr" : user.username,
    })

    subject = "Change Password"
    html_content = """
        <p>Click the URL to change the password:</p>
        <a href="%s">%s</a>
    """ % (chpsw_url,chpsw_url)
    
    msg = EmailMultiAlternatives(subject,html_content,settings.EMAIL_HOST_USER,[user_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    messages.success(request,"A Email has been sent to %s" % user.email)
    return HttpResponseRedirect(rurl)

@login_required
def chpsw_sendmail(request):
    return _chpsw_sendmail(request,request.user,reverse("xadmin:inbox"))


from django.contrib.auth.models import User
from datetime import datetime

def chpsw_ckhash(request):
    if request.method == "GET":
        usr = request.GET.get("usr")
        key = request.GET.get("key")
        es = EmailHash.objects.get(holder = User.objects.get(username = usr))
        
        time_dt = datetime.now() - es.gen_date
        if es and es.hash_str == key and time_dt.total_seconds() <= 60.0:
            return render(request,"xadmin/change_password.html",{
                "usr" : usr,
                "key" : key,
            })
    return HttpResponse("")



from forms import ChangePasswordForm
from django.contrib.auth import login,authenticate

def chpsw_doupdate(request):
    if request.method == "POST":
        cpf = ChangePasswordForm(request.POST)
        if cpf.is_valid():
            username = cpf.cleaned_data['username']
            hash_key = cpf.cleaned_data['hash_key']
            newpswrd = cpf.cleaned_data['password']

            user = User.objects.get(username = username)
            es = EmailHash.objects.get(holder = user)

            if es and es.hash_str == hash_key:
                user.set_password(newpswrd)
                user.save()

                user = authenticate(username = username,password = newpswrd)
                login(request,user)

                messages.success(request,"Change password succesfully!")
                return HttpResponseRedirect(reverse("xadmin:inbox"))
    return HttpResponse("Failed!")
