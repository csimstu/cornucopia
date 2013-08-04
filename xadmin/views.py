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


from forms import NewMessageForm
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
