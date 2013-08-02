from django.shortcuts import render
from forum.models import *
from pages.models import *
from network.models import RelationList, Message

def dashboard(request):
    user = request.user

    stat = {
        'topic_cnt' : Topic.objects.filter(author=user).count(),
            'post_cnt' : Post.objects.filter(author=user).count(),
            'reply_cnt': Reply.objects.filter(author=user).count(),
            'article_cnt': Article.objects.filter(author=user).count(),
            'comment_cnt': Comment.objects.filter(author=user).count(),
            'tag_cnt': Tag.objects.filter(author=user).count(),
            'friend_cnt': user.relationlist.friends.count(),
            'following_cnt': user.relationlist.followings.count(),
            'follower_cnt': RelationList.objects.filter(followings=user).count(),
    }

    attention = {
        'unread_msg': Message.objects.filter(receiver=user,unread=True,type="MSG").count(),
        'unread_ntf': Message.objects.filter(receiver=user,unread=True,type="NTF").count(),
        'unread_inv': Message.objects.filter(receiver=user,unread=True,type="INV").count(),
    }

    ntf_list = user.notification_set.filter(unread=True)

    return render(request, 'xadmin/dashboard.html',
        {
            'stat': stat, 'attention': attention,
            'ntf_list': ntf_list,
        })